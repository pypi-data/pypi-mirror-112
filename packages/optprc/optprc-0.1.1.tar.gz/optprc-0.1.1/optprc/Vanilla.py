# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:10:57 2017

@author: Yongguang Gong
"""

from __future__ import division, print_function

import numpy as np
import scipy.stats as stats


class VanillaPricer_Class():
    
    def __init__(self,L,K,phi,s0,repo,div,r,vol,td,tv):
        self.L=L; self.K=K; self.phi=phi
        self.s0=s0; self.repo=repo; self.div=div
        self.r=r; self.vol=vol; self.td=td; self.tv=tv
        
    def AnalyticFormula(self):
        L=self.L; K=self.K; phi=self.phi
        s0=self.s0; repo=self.repo; div=self.div
        r=self.r; vol=self.vol; td=self.td; tv=self.tv
        
        forward=s0*np.exp((repo-div)*td)
        d1=np.log(forward/K)/vol/np.sqrt(tv)+0.5*vol*np.sqrt(tv)
        d2=d1-vol*np.sqrt(tv)
        OptPrice=phi*L*(forward*stats.norm.cdf(phi*d1)-K*stats.norm.cdf(phi*d2))*np.exp(-r*td)
        return OptPrice
        
        
    def MonteCarlo(self,PathNum,StepNum):
        L=self.L; K=self.K; phi=self.phi
        s0=self.s0; repo=self.repo; div=self.div
        r=self.r; vol=self.vol; td=self.td; tv=self.tv
        
        repo=repo*td/tv
        div=div*td/tv
        dt=tv/StepNum
        RandNum=np.random.normal(0.,1.,[StepNum,PathNum])
        RandNum=np.hstack((RandNum,-RandNum))
        SPath=s0*np.exp(np.cumsum((repo-div-0.5*vol**2)*dt+vol*RandNum*np.sqrt(dt),axis=0))
        OptPrice=L*np.mean(np.maximum(phi*(SPath[-1,:]-K),0))*np.exp(-r*td)
        return OptPrice
    
    
    def FiniteDifference(self,ns,nt):
        # by Crank-nicolson scheme
        L=self.L; K=self.K; phi=self.phi
        s0=self.s0; repo=self.repo; div=self.div
        r=self.r; vol=self.vol; td=self.td; tv=self.tv
        
        Smax=K*5.
        repo=repo*td/tv
        div=div*td/tv    
        r=r*td/tv
        
        s_grid=np.linspace(0,Smax,ns+1)
        dt=tv/nt
        i=np.array(range(ns+1))
        a1=0.25*(repo-div)*i*dt-0.25*vol**2*i**2*dt
        b1=1+0.5*vol**2*i**2*dt
        c1=-0.25*(repo-div)*i*dt-0.25*vol**2*i**2*dt
    
        a2=-0.25*(repo-div)*i*dt+0.25*vol**2*i**2*dt
        b2=1-0.5*vol**2*i**2*dt
        c2=0.25*(repo-div)*i*dt+0.25*vol**2*i**2*dt
    
        B1=np.diag(a1[2:-1],-1)+np.diag(b1[1:-1])+np.diag(c1[1:-2],1)
        B1_inverse=np.linalg.inv(B1)
        B2=np.diag(a2[2:-1],-1)+np.diag(b2[1:-1])+np.diag(c2[1:-2],1)
    
        BD_t=np.maximum(phi*(s_grid-K),0)
        j=np.array(range(nt+1))
        if phi==1:
            BD_Smin=np.zeros(nt+1)
            BD_Smax=np.maximum(Smax*np.exp((repo-div)*j*dt)-K,0)
        else:
            BD_Smax=np.zeros(nt+1)
            BD_Smin=K*np.ones(nt+1)
    
        u=BD_t
        for tj in range(1,nt+1):
            u=np.reshape(u,(len(u),1))
            g1=np.hstack((a1[1]*BD_Smin[tj],np.zeros(ns-3),c1[-2]*BD_Smax[tj]))
            g2=np.hstack((a2[1]*u[0],np.zeros(ns-3),c2[-2]*u[-1]))
            g1=np.reshape(g1,(len(g1),1))
            g2=np.reshape(g2,(len(g2),1))
        
            u[1:-1]=np.dot(B1_inverse,np.dot(B2,u[1:-1])+g2-g1)
            u[0]=BD_Smin[tj]
            u[-1]=BD_Smax[tj]
            u=u*np.exp(-r*dt)
            
        u=np.reshape(u,(len(u,)))    
        OptPrice=L*np.interp(s0,s_grid,u)
        return OptPrice



if __name__ == "__main__":
    L=10000.
    K=100. 
    phi=1.
    s0=105
    repo=0.04
    div=0.01
    r=0.03
    vol=0.5
    td=1.0
    tv=1.03
    PathNum=20000
    StepNum=100
    ns=100
    nt=80
    
    Pricer1=VanillaPricer_Class(L,K,phi,s0,repo,div,r,vol,td,tv)
    
    Price0=Pricer1.AnalyticFormula()
    Price1=Pricer1.MonteCarlo(PathNum,StepNum)
    Price2=Pricer1.FiniteDifference(ns,nt)
    
    print('Analytical Formula:',Price0)
    print('Monte Carlo:',Price1)
    print('Finite Difference:',Price2)
    