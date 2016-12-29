#coding=utf-8
'''
Created on 2016年11月30日

@author: 58
'''

import numpy as np

def cosSimilarity(x,y):
    a=np.sum(x[i]*y[i] for i in range(len(x)))
    xx=np.sqrt(np.sum(x[i]*x[i] for i in range(len(x))))
    yy=np.sqrt(np.sum(y[i]*y[i] for i in range(len(y))))
    #print "xx,yy",xx,yy
    if xx==0 and yy==0:
        return 1
    elif xx*yy==0:
        return 0
    else:
        return a/(xx*yy)

def correlation(x,y):
    x_mean=np.mean(x)
    y_mean=np.mean(y)
    #print x_mean,y_mean
    x=[x[i]-x_mean for i in range(len(x))]
    y=[y[i]-y_mean for i in range(len(y))]
    #print x,y
    return cosSimilarity(x,y)


x=[11740,29551,26753,24186,26215,23346,15022]
y=[[13566,29562,27596,24602,26383,24144,14002],[29562,27596,24602,26383,24144,14002,14235],[27596,24602,26383,24144,14002,14235,30598],[24602,26383,24144,14002,14235,30598,23405],[26383,24144,14002,14235,30598,23405,23932],[24144,14002,14235,30598,23405,23932,23724]]
'''
print correlation([1,2,3],[-1,-2,-3])
for i in range(len(y)):
    print "2: ",correlation(x,y[i])
'''  

