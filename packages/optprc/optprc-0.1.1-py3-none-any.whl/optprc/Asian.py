# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:34:10 2015

@author: Yongguang Gong
"""
from __future__ import division, print_function
import numpy as np
from scipy.stats import norm, lognorm
from scipy.integrate import quad
from . import iMath


class AsianPricer_class(object):
    def __init__(self,L,K,phi,s0,repo,div,vol,T):
        self.L = L; self.K = K; self.phi = phi
        self.s0 = s0; self.repo = repo; self.div= div
        self.vol = vol; self.T = T
    
    def GeometricAverage(self):
        L = self.L; s0=self.s0; r = self.repo
        q = self.div; K = self.K; Sigma = self.vol
        T = self.T; phi = self.phi
        
        SigmaA=Sigma/np.sqrt(3.0)
        ba=0.5*(r-q-Sigma*Sigma/6.0)
        d1=(np.log(s0/K)+(ba+0.5*SigmaA*SigmaA)*T)/SigmaA/np.sqrt(T)
        d2=d1-SigmaA*np.sqrt(T)
        OptVal=phi*L*(s0*np.exp((ba-r)*T)*norm.cdf(phi*d1,0.0,1.0)-K*np.exp(-r*T)*norm.cdf(phi*d2,0.0,1.0))
        
        return OptVal
    
    
    def CurranApprox(self):
        L = self.L; s0=self.s0; r = self.repo
        q = self.div; K = self.K; Sigma = self.vol
        T = self.T; phi = self.phi
        #dt=T/N
        dt = 1/252; N = round(T/dt)
        
        iy=np.array(range(1,N+1,1),ndmin=2)
        ix=np.transpose(iy)
        Mu_lnS=np.log(s0)+(r-q-0.5*Sigma**2.)*ix*dt
        Var_lnS=Sigma**2*ix*dt
        Corr_lnS=np.sqrt(iMath.Min(ix*np.ones((1,N)),iy*np.ones((N,1)))/iMath.Max(ix*np.ones((1,N)),iy*np.ones((N,1))))
        CoVar_lnS=np.sqrt(np.dot(Var_lnS,np.transpose(Var_lnS)))*Corr_lnS
        Mu_lnG=np.mean(Mu_lnS)
        Var_lnG=np.dot(np.sqrt(np.transpose(Var_lnS)),np.dot(Corr_lnS,np.sqrt(Var_lnS)))/N**2.
        Var_lnSG=np.sqrt(Var_lnS)*np.dot(Corr_lnS,np.sqrt(Var_lnS))/N
        
        Part21=np.exp(Mu_lnS+0.5*Var_lnS)*norm.cdf((Mu_lnG-np.log(K))/np.sqrt(Var_lnG)+Var_lnSG/np.sqrt(Var_lnG),0.,1.)
        Part21=np.mean(Part21)
        Part22=K*norm.cdf((Mu_lnG-np.log(K))/np.sqrt(Var_lnG))
        Part2=Part21-Part22
    
        CoVar_lnSonlnG=CoVar_lnS-np.dot(np.dot(CoVar_lnS,np.ones((N,1))),np.transpose(np.dot(CoVar_lnS,np.ones((N,1)))))/np.sum(np.sum(CoVar_lnS))
        Mu_lnSonlnG=Mu_lnS+Var_lnSG/Var_lnG*(np.log(K)-Mu_lnG)
        Mu_AonlnG=np.mean(np.exp(Mu_lnSonlnG+0.5*np.reshape(np.diag(CoVar_lnSonlnG),(-1,1))))
        Var_SonlnG=np.exp(Mu_lnSonlnG+0.5*np.reshape(np.diag(CoVar_lnSonlnG),(-1,1)))
        CoVar_SonlnG=(Var_SonlnG*np.ones((1,N)))*np.transpose(Var_SonlnG*np.ones((1,N)))*(np.exp(CoVar_lnSonlnG)-1.0)
        Var_AonlnG=np.sum(np.sum(CoVar_SonlnG))/N**2.
    
        Mu_Diff=Mu_AonlnG-K
        Var_Diff=np.copy(Var_AonlnG)
        Var_lnDiff=np.log(Var_Diff/Mu_Diff**2.+1.)
        Diff0=np.copy(Mu_Diff)
        es=0.000000000001
        K=K-es
    
        func=lambda x:iBSOption(Diff0,Var_lnDiff,K,x,Mu_lnG,Var_lnG)
        Part1,IntError=quad(func,es,K)
        callV = float(L*(Part1+Part2)*np.exp(-r*T))
        putV = callV-L*(s0*np.exp(-q*T)-K* np.exp(-r*T))
        
        return callV if phi==1 else putV


def iBSOption(Diff0,Var_lnDiff,K,G,Mu_lnG,Var_lnG):
    d1=(np.log(Diff0/(K-G)))/np.sqrt(Var_lnDiff)+0.5*np.sqrt(Var_lnDiff)
    d2=d1-np.sqrt(Var_lnDiff)
    OptVal=Diff0*norm.cdf(d1,0.,1.)-(K-G)*norm.cdf(d2,0.,1.)
    return OptVal*lognorm.pdf(G,np.sqrt(Var_lnG),0,np.exp(Mu_lnG))



if __name__ == "__main__":
    L=1.0
    s0=200.0
    r=0.04
    q=0.02
    K=200.0
    Sigma=0.4
    T=1.0
    phi=1.0
    
    import time
    time0=time.time()
    Call=AsianPricer_class(L,K,phi,s0,r,q,Sigma,T).GeometricAverage()
    print(Call, time.time()-time0)
    