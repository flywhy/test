#coding=utf-8;
'''
Created on 2016年11月26日

@author: 58
'''

from datetime import date
from calendar import month, week
from Solar2Lunar import *

solarHoliday1=["01-01","05-01"]
solarHoliday2=["10-01"]
lunarHoliday=["05-05","08-15"]# 端午，中秋
ChunJie=["01-01"]
QingMing="" #[Y*D+C]-L Y=年的后两位 D=0.2422 C(21世纪清明)=4.81 L(闰年数)=Y/4

def getDateAttr(dateSolar): #2016-08-09
    year=int(dateSolar[0:4])
    month=int(dateSolar[5:7])
    day=int(dateSolar[8:10])
    
    week=date(year,month,day).weekday()+1;
    dateLunar=get_lunar_date(year,month,day)
    
    
    tag="0"
    QMDay=((year%100)*0.2422+4.81)-(year%100)/4
    
    if week in [6,7]:
        tag=="1"
    
    if dateSolar[5:10]=="01-01":
        tag="YuanDan"
    elif dateSolar[5:10]=="05-01":
        tag="WuYi"
    elif dateSolar[5:10]=="10-01":
        tag="ShiYi"
    elif dateSolar[5:10]=="04-0"+str(QMDay):
        tag="QingMing"
    
    if str(dateLunar[1])+"-"+str(dateLunar[2])=="01-01":
        tag="ChunJie"
    elif str(dateLunar[1])+"-"+str(dateLunar[2])=="05-05":
        tag="DuanWu"
    elif str(dateLunar[1])+"-"+str(dateLunar[2])=="08-15":
        tag="ZhongQiu"
    
    print dateSolar,dateLunar,week,tag
    return dateSolar,dateLunar,week,tag

getDateAttr("2016-10-01")    


    