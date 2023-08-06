# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 17:42:17 2017

@author: Yongguang Gong
"""

from __future__ import division,print_function
import calendar
import dateutil.parser
import numpy as np
import copy
import datetime
from functools import wraps
import time


def str2date(x):
    if isinstance(x,(str,np.str_,np.string_)):
        return dateutil.parser.parse(x)
    
    xtypes=isinstance(x,np.ndarray)
    if xtypes: x=x.tolist()
    
    y=copy.deepcopy(x)
    for i in range(len(x)):
        if isinstance(x[i],str):
            y[i]=dateutil.parser.parse(x[i])
            
        elif isinstance(x[i],list):
            for j in range(len(x[i])):
                y[i][j]=dateutil.parser.parse(x[i][j])
            
    if xtypes: y=np.array(y)
    return y



def date2str(x,format_flag):
    
    def __date2str(x,format_flag):
        if format_flag==1:
            return x.strftime('%Y-%m-%d')
        elif format_flag==0:
            return x.strftime('%Y-%m-%d %H:%M')
    
    if isinstance(x,datetime.datetime):
        return __date2str(x,format_flag)
    
    xtypes=isinstance(x,np.ndarray)
    if xtypes: x=x.tolist()
    
    y=copy.deepcopy(x)
    for i in range(len(x)):
        if isinstance(x[i],datetime.datetime):
            y[i]=__date2str(x[i],format_flag)
            
        elif isinstance(x[i],list):
            for j in range(len(x[i])):
                y[i][j]=__date2str(x[i][j],format_flag)
            
    if xtypes: y=np.array(y)
    return y



def date2num(x):
    date0=datetime.datetime(1900,3,1,0,0,0)
    
    def __date2num(x):
        tmp=x-date0
        return float(tmp.days)+tmp.seconds/24./3600.+61.
    
    if isinstance(x,datetime.datetime):
        return __date2num(x)
    
    xtypes=isinstance(x,np.ndarray)
    if xtypes: x=x.tolist()
    
    y=copy.deepcopy(x)
    for i in range(len(x)):
        if isinstance(x[i],datetime.datetime):
            y[i]=__date2num(x[i])
            
        elif isinstance(x[i],list):
            for j in range(len(x[i])):
                y[i][j]=__date2num(x[i][j])
            
    if xtypes: y=np.array(y)
    return y



def num2date(x):
    date0=datetime.datetime(1900,3,1,0,0,0)
    
    def __num2date(x):
        return date0+datetime.timedelta(x-61.)
    
    if isinstance(x,(int,float,np.int32,np.float64)):
        return __num2date(x)
    
    xtypes=isinstance(x,np.ndarray)
    if xtypes: x=x.tolist()
    
    y=copy.deepcopy(x)
    for i in range(len(x)):
        if isinstance(x[i],(int,float,np.int32,np.float64)):
            y[i]=__num2date(x[i])
            
        elif isinstance(x[i],list):
            for j in range(len(x[i])):
                y[i][j]=__num2date(x[i][j])
            
    if xtypes: y=np.array(y)
    return y
    



def addtenor(x,tenor,endmonth_flag=0):
    
    def __addmonth(x,tenor_num,endmonth_flag):
        x1=x+dateutil.relativedelta.relativedelta(months=tenor_num)
        if endmonth_flag==1:
            _,lastdaynum=calendar.monthrange(x.year,x.month)
            _,tmplastdaynum=calendar.monthrange(x1.year,x1.month)
            if (x.day==lastdaynum)&(x1.day!=tmplastdaynum) :
                x1=datetime.datetime(x1.year,x1.month,tmplastdaynum,x1.hour,x1.minute,x1.second)
        return x1
    
    if isinstance(x,(int,float,np.int32,np.float64)):
        x_date,x_num=num2date(x),copy.deepcopy(x)
    elif isinstance(x,datetime.datetime):
        x_date,x_num=copy.deepcopy(x),date2num(x)
    
    tenor_num,tenor_measure=tenor[0],tenor[1]
    if tenor_measure==1:
        y_num=x_num+tenor_num
        y_date=num2date(y_num)
    elif tenor_measure==2:
        y_num=x_num+tenor_num*7
        y_date=num2date(y_num)
    elif tenor_measure==3:
        y_date=__addmonth(x_date,int(tenor_num),endmonth_flag)
        y_num=date2num(y_date)
    elif tenor_measure==4:
        y_date=__addmonth(x_date,int(tenor_num*12),endmonth_flag)
        y_num=date2num(y_date)
    
    if isinstance(x,datetime.datetime):
        return y_date
    elif isinstance(x,(int,float,np.int32,np.float64)):
        return y_num
    


class bzdayadj_class(object):
    def __init__(self,Holiday,Weekend=1):
        self.Holiday=np.array(Holiday)
        self.Weekend=Weekend
    
    def to_wd(self,date0,methods):
        if (methods==0)|(methods=="NA"):
            return date0
        elif (methods==1)|(methods=="F"):
            return self.following(date0)
        elif (methods==-1)|(methods=="P"):
            return self.preceding(date0)
        elif (methods==2)|(methods=="MF"):
            return self.modifyfollowing(date0)
    
    def following(self,date0):
        while 1==1:
            tmp1=all(self.Holiday!=date0)
            date1=num2date(date0)
            tmp2=(date1.weekday()!=5)&(date1.weekday()!=6)
            if (tmp1&(self.Weekend==0))|(tmp1&(self.Weekend==1)&tmp2): 
                break
            date0=date0+1
        return date0
    
    def preceding(self,date0):
        while 1==1:
            tmp1=all(self.Holiday!=date0)
            date1=num2date(date0)
            tmp2=(date1.weekday()!=5)&(date1.weekday()!=6)
            if (tmp1&(self.Weekend==0))|(tmp1&(self.Weekend==1)&tmp2): 
                break
            date0=date0-1
        return date0
    
    def modifyfollowing(self,date0):
        date1=self.following(date0)
        tmp0,tmp1=num2date(date0),num2date(date1)
        if tmp0.month!=tmp1.month:
            date1=self.preceding(date0)
        return date1



def daycount(x1,x2,methods):
    
    def __daycount(date1,date2,methods):
        if (methods==1)|(methods=="Act365"):
            return (date2-date1)/365.
        elif (methods==2)|(methods=="Act360"):
            return (date2-date1)/360.
        elif (methods==3)|(methods=="30I360"):
            date1,date2=num2date(date1),num2date(date2)
            Y1=date1.year; M1=date1.month; D1=date1.day
            Y2=date2.year; M2=date2.month; D2=date2.day
            _,lastdaynum1=calendar.monthrange(Y1,M1)
            _,lastdaynum2=calendar.monthrange(Y2,M2)
            if (M1==2)&(D1==lastdaynum1)&(M2==2)&(D2==lastdaynum2): D2=30
            if (M1==2)&(D1==lastdaynum1): D1=30
            if (D2==31)&((D1==30)|(D1==31)):D2=30
            if D1==31:D1=30
            return ((Y2-Y1)*360+(M2-M1)*30+(D2-D1))/360.
    
    
    if isinstance(x1,(int,float,np.int32,np.float64)):
        return __daycount(x1,x2,methods)
    
    xtypes=isinstance(x1,np.ndarray)
    if xtypes: x1=x1.tolist(); x2=x2.tolist()
    
    y=copy.deepcopy(x1)
    for i in range(len(x1)):
        if isinstance(x1[i],(int,float)):
            y[i]=__daycount(x1[i],x2[i],methods)
            
        elif isinstance(x1[i],list):
            for j in range(len(x1[i])):
                y[i][j]=__daycount(x1[i][j],x2[i][j],methods)
            
    if xtypes: y=np.array(y)
    return y



class settleday_class(bzdayadj_class):
    def to_date(self,date0,days):
        signs=np.sign(days)
        if signs==0:
            methods="NA"
        elif signs==1:
            methods="F"
        elif signs==-1:
            methods="P"
        
        for i in range(abs(int(days))):
            date0=date0+signs
            date0=self.to_wd(date0,methods)
        return date0




def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1=time.time()
        result=fn(*args,**kwargs)
        t2=time.time()
        print ("@timefn:"+fn.__name__+" took "+str(round(t2-t1,4))+" seconds")
        return result
    return measure_time




if __name__ == "__main__":
    x1=['2012-7-5','2012-7-6']
    y1=str2date(x1)
    x2=[['2012-7-5'],['2012-7-6']]
    y2=str2date(x2)
    x3=np.array(x1)
    y3=str2date(x3)
    x4=np.array(x1,ndmin=2)
    y4=str2date(x4)
    x5=np.array(x2)
    y5=str2date(x5)
    x6='2012-7-5'
    y6=str2date(x6)
    x7=x3[0]
    y7=str2date(x7)    
    
    z1=date2str(y1,1)
    z2=date2str(y2,1)
    z3=date2str(y3,1)
    z4=date2str(y4,1)
    z5=date2str(y5,1)
    z6=date2str(y6,1)
    print(type(y4[0,0]))
    
    
    U1=date2num(y1)
    U2=date2num(y2)
    U3=date2num(y3)
    U4=date2num(y4)
    U5=date2num(y5)
    U6=date2num(y6)
    
    V1=num2date(U1)
    V2=num2date(U2)
    V3=num2date(U3)
    V4=num2date(U4)
    V5=num2date(U5)
    V6=num2date(U6)
    V7=num2date(U3[0])
    
    print(addtenor(V1[0],[3,1],1))
    
    Holiday=['2017-9-15','2017-9-18','2017-9-29']
    date0='2017-9-29'
    Holiday=date2num(str2date(Holiday))
    date0=date2num(str2date(date0))
    bzdayadj=bzdayadj_class(Holiday,0).to_wd
    
    print(num2date(bzdayadj(date0,"F")),num2date(bzdayadj(date0,"P")),num2date(bzdayadj(date0,"MF")))
    
    date1=date2num(str2date('2017-2-28'))
    date2=date2num(str2date('2017-3-31'))
    print(daycount(date1,date2,3))
    
    date3=date2num(str2date('2017-9-14'))
    settleday=settleday_class(Holiday,1).to_date
    print (num2date(settleday(date3,2)))
    