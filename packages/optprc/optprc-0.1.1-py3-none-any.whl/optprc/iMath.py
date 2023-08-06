# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 14:52:02 2016

@author: Yongguang Gong
"""

from __future__ import division,print_function
from scipy.stats import norm
from scipy.interpolate import interp1d
import ast
import numpy as np


def interp1(x,y,xi,interp_method):
    if (interp_method==1)|(interp_method=='linear'):
        func=interp1d(x,y,kind='linear',bounds_error=False,fill_value=(y[0],y[-1]))
    return func(xi)


def normcdf(x):
    return norm.cdf(x,0.0,1.0)


def str2var(x):
    return ast.literal_eval(x)


def col2row(x_columns):
    x_rows=list(range(len(x_columns)))
    for i in range(len(x_columns)):
        x_rows[i]=x_columns[i][0]
    return x_rows
    
    
def Max(a,b):
    c=np.copy(a)
    if np.size(b)==1:
        c[a<b]=b
    else:
        c[a<b]=b[a<b]
    return c


def Min(a,b):
    c=np.copy(a)
    if np.size(b)==1:
        c[a>b]=b
    else:
        c[a>b]=b[a>b]
    return c



if __name__ == "__main__":
    x=[1.,2.,3.,4.,5.,6.]
    y=[0.1,0.2,0.3,0.4,0.5,0.6]
    xi=[0.5,2.5,7.5]
    yi=interp1(x,y,xi,1)
    
    print(normcdf(x))
    print(str2var('2'))
    