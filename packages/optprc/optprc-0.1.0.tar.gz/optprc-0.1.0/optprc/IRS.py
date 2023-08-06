# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:37:39 2017

@author: Yongguang Gong
"""

from __future__ import division, print_function

from . import iDate
import numpy as np
import copy
from . import iMath


class discount_class(object):
    def __init__(self,Curve,SpotDate,CurveSettings):
        if CurveSettings[0]=="T":
            if CurveSettings[1]=="Act365":
                Curve[:,0]=(Curve[:,0]-SpotDate)/365.
            elif CurveSettings[1]=="Act360":
                Curve[:,0]=(Curve[:,0]-SpotDate)/360.
        self.Curve=Curve
        self.SpotDate=SpotDate
        self.CurveSettings=CurveSettings
    
    def to_dscnt(self,Date0):
        if self.CurveSettings[1]=="Act365":
            t0=(Date0-self.SpotDate)/365.
        elif self.CurveSettings[1]=="Act360":
            t0=(Date0-self.SpotDate)/360.
        
        rate0=iMath.interp1(self.Curve[:,0],self.Curve[:,1],t0,'linear')
        if self.CurveSettings[2]=="C":
            return np.exp(-rate0*t0)


class forwardrate_class(discount_class):
    def __init__(self,Curve,SpotDate,CurveSettings,IndexSettings):
        super(forwardrate_class,self).__init__(Curve,SpotDate,CurveSettings)
        self.IndexSettings=IndexSettings
        
    def to_fwd(self,effect,expiry):
        dscnt1=self.to_dscnt(effect)
        dscnt2=self.to_dscnt(expiry)
        
        if self.IndexSettings[0]=="Act365":
            return (dscnt1/dscnt2-1)/(expiry-effect)*365.
        elif self.IndexSettings[0]=="Act360":
            return (dscnt1/dscnt2-1)/(expiry-effect)*360.



class IRSPricer_class(object):
    
    def __init__(self,SpotDate,RefRateFlag,RefCurve,RefRate_his,DisCurve,Holiday):
        self.SpotDate=SpotDate[0]
        self.Tenor=RefRateFlag
        self.RefCurve=np.array(RefCurve)
        self.RefRate_his=np.array(RefRate_his)
        self.DisCurve=np.array(DisCurve)
        self.bzdayadj=iDate.bzdayadj_class(Holiday,1).to_wd
        self.settleday=iDate.settleday_class(Holiday,1).to_date
        self.Acc2PayFlag=1
        self.fixdatesettledays=-2
        self.IndexSettledays=2
        self.EndMonthFlag=1
        self.discount=discount_class(self.DisCurve,self.SpotDate,["D","Act365","C"]).to_dscnt
        self.forwardrate=forwardrate_class(self.RefCurve,self.SpotDate,["D","Act365","C"],["Act365"]).to_fwd
        
    
    def CFDate(self,EffectDate,ExpiryDate,Freq):
        Period=12./Freq
        N=int(np.round((ExpiryDate-EffectDate)/365.*Freq))
        CF_expiry,CF_paydate =np.zeros(N),np.zeros(N)
     
        for i in range(N):
            CF_expiry[i]=iDate.addtenor(EffectDate,[int(Period*(i+1)),3],self.EndMonthFlag)
            CF_paydate[i]=self.bzdayadj(CF_expiry[i],"F")
        CF_expiry[N-1]=ExpiryDate
        if self.Acc2PayFlag==1:
            CF_expiry=copy.deepcopy(CF_paydate)
        
        CF_effect=np.zeros(N); CF_effect[0]=EffectDate
        CF_effect[1:N]=copy.deepcopy(CF_expiry[0:N-1])
        
        return CF_effect,CF_expiry,CF_paydate
    
    
    
    def RollCFAmount(self,EffectDate,ExpiryDate,Tenor,Spread):
        
        Tenor_num,Tenor_measure=Tenor[0],Tenor[1]
        
        Rolling_expiry=iDate.addtenor(EffectDate,[Tenor_num,Tenor_measure],self.EndMonthFlag)
        Rolling_expiry=np.array([self.bzdayadj(Rolling_expiry,"F")])
        
        while Rolling_expiry[-1]<ExpiryDate:
            expiry=iDate.addtenor(Rolling_expiry[-1],[Tenor_num,Tenor_measure],self.EndMonthFlag)
            Rolling_expiry=np.hstack((Rolling_expiry,np.array([expiry])))
        
        Rolling_expiry=Rolling_expiry[Rolling_expiry<ExpiryDate]
        Rolling_expiry=np.hstack((Rolling_expiry,np.array([ExpiryDate])))
        Rolling_effect=np.hstack((np.array([EffectDate]),Rolling_expiry[0:-1]))
        
        N=len(Rolling_effect)
        Rolling_fixdate,Fwd_effect,Fwd_expiry=np.zeros(N),np.zeros(N),np.zeros(N)
        
        for i in range(N):
            Rolling_fixdate[i]=self.settleday(Rolling_effect[i],self.fixdatesettledays)
            Fwd_effect[i]=self.settleday(Rolling_fixdate[i],self.IndexSettledays)
            Fwd_expiry[i]=iDate.addtenor(Fwd_effect[i],Tenor,self.EndMonthFlag)
            Fwd_expiry[i]=self.bzdayadj(Fwd_expiry[i],"NA")
            
        RefRate=iMath.interp1(self.RefRate_his[:,0],self.RefRate_his[:,1],Rolling_fixdate,'linear')
        AccInt=np.zeros(N)
        for i in range(N):
            if Rolling_fixdate[i]>SpotDate:
                RefRate[i]=self.forwardrate(Fwd_effect[i],Fwd_expiry[i])
            AccInt[i]=(RefRate[i]+Spread)*iDate.daycount(Rolling_effect[i],Rolling_expiry[i],"Act360")
        CumAccInt=np.prod(1.+AccInt)-1
        return CumAccInt
    
    
    
    def FixLeg(self,Notional,EffectDate,ExpiryDate,Strike,Freq):
        EffectDate,ExpiryDate,Freq=EffectDate[0],ExpiryDate[0],Freq[0]
        Notional,Strike=Notional[0],Strike[0]
        
        CF_effect,CF_expiry,CF_paydate=self.CFDate(EffectDate,ExpiryDate,Freq)
        
        Term0=iDate.daycount(CF_effect,CF_expiry,"Act365")
        CF_amount=Notional*Strike*Term0
        
        CashFlow=np.transpose(np.vstack([CF_paydate,CF_amount]))
        
        CF_paydate=CF_paydate[CF_paydate>=self.SpotDate]
        CF_amount=CF_amount[CF_paydate>=self.SpotDate]
        
        if len(CF_paydate)==0: return CashFlow, 0.
        
        Dscnt=self.discount(CF_paydate)
        
        return CashFlow, np.sum(CF_amount*Dscnt)
        
        

    def FltLeg(self,Notional,EffectDate,ExpiryDate,Freq,Spread):
        EffectDate,ExpiryDate,Freq=EffectDate[0],ExpiryDate[0],Freq[0]
        Notional,Spread=Notional[0],Spread[0]
        
        CF_effect,CF_expiry,CF_paydate=self.CFDate(EffectDate,ExpiryDate,Freq)
        N=len(CF_effect)
        CF_amount=np.zeros(N)
        for i in range(N):
            CF_amount[i]=Notional*self.RollCFAmount(CF_effect[i],CF_expiry[i],[7,1],Spread)
        
        CashFlow=np.transpose(np.vstack([CF_paydate,CF_amount]))
        
        CF_paydate=CF_paydate[CF_paydate>=self.SpotDate]
        CF_amount=CF_amount[CF_paydate>=self.SpotDate]
        
        if len(CF_paydate)==0: return CashFlow, 0.
        
        Dscnt=self.discount(CF_paydate)
        
        return CashFlow, np.sum(CF_amount*Dscnt)
    
    
    
    def Swap(self,BuyFlag,Notional,EffectDate,ExpiryDate,Strike,Spread,Freq_fix,Freq_flt):
        BuyFlag=BuyFlag[0]
        CF_fix,Value_fix=self.FixLeg(Notional,EffectDate,ExpiryDate,Strike,Freq_fix)
        CF_flt,Value_flt=self.FltLeg(Notional,EffectDate,ExpiryDate,Freq_flt,Spread)
        
        return BuyFlag*(Value_fix-Value_flt)
        
 



if __name__ == "__main__":
    BuyFlag=[2]
    Notional=[100000]
    EffectDate='12-Aug-2007'
    ExpiryDate='12-Aug-2009'
    SpotDate='12-Aug-2007'
    Strike=[0.04]
    RefRate=[1]
    Freq_fix=[4]
    Freq_flt=[4]
    Spread=[0.005]
    DayCountFlag=[1]
    
    RefCurve=[[3/365.,0.0259],[7/365.,0.0328],[14/365.,0.0328],[1/12.,0.0338],[0.25,0.0432],[0.5,0.0457],[0.75,0.0464],[1.,0.0471],[2.,0.0477],[3.,0.0480],[4.,0.0486],[5.,0.0498],[6.,0.0510],[7.,0.0518],[8.,0.0522],[9.,0.0525],[10.,0.053]]
    DisCurve=[[3/365.,0.0259],[7/365.,0.0328],[14/365.,0.0328],[1/12.,0.0338],[0.25,0.0432],[0.5,0.0457],[0.75,0.0464],[1.,0.0471],[2.,0.0477],[3.,0.0480],[4.,0.0486],[5.,0.0498],[6.,0.0510],[7.,0.0518],[8.,0.0522],[9.,0.0525],[10.,0.053]]
    
    RefRate_his=list([[39927,0.0121]])
    for i in range(700):
        RefRate_his.append([39927-i,0.0121])
    
    
    EffectDate=[iDate.date2num(iDate.str2date(EffectDate))]
    ExpiryDate=[iDate.date2num(iDate.str2date(ExpiryDate))]
    SpotDate=[iDate.date2num(iDate.str2date(SpotDate))]
    
    IRSPricer1=IRSPricer_class(SpotDate,RefRate,RefCurve,RefRate_his,DisCurve,[1])
    CashFlow1,Value1=IRSPricer1.FixLeg(Notional,EffectDate,ExpiryDate,Strike,Freq_fix)
    
    CashFlow2,Value2=IRSPricer1.FltLeg(Notional,EffectDate,ExpiryDate,Freq_flt,Spread)
    