#coding=utf-8
'''
Created on 2016年11月30日

@author: 58
'''

import KnnRegression as kr
import numpy as np
import datetime

# 从全部的文件中获取一个 任务id对应的所有数据
def getDataFromFile(taskID,testFile):
    data=[]
    with(open(testFile,'r')) as f:
        for line in f:
            lineData=line.strip().split('\t')
            if lineData[0]==taskID:
                if len(lineData)==3:
                    data.append([int(lineData[2]),lineData[1]])
    return data


# 日期格式转换  str>>datetime.date
def datefstr(date_str):
    year=int(date_str[:4])
    month=int(date_str[5:7])
    day=int(date_str[8:10])
    date=datetime.date(year,month,day)
    return date

## 检测历史数据跟当天的距离 若果最晚的时间和当天差别>=7days 则说明改天数据不具有可预测性
def connect_today(ts,today):
    #print ts
    final_day=datefstr(ts[-1][1])
    #print final_day
    today=datefstr(today)
    gap=today-final_day
    #print today,final_day
    if gap.days==0:
        return ts
    elif gap.days>0 and gap.days<7:
        for i in range(1,gap.days+1):
            tmp_date=final_day+datetime.timedelta(days=i)
            ts.append([0,tmp_date.strftime("%Y-%m-%d")])
        return ts
    else:
        return None

# 检测时间序列缺少的天数 对缺少天的数据补全  间隔较长且天数持续较短的舍弃
def date_completion(ts):
    n=len(ts)
    date=[ts[i][1] for i in range(n)]
    gaps0=[]
    gap_index=[0]
    for i in range(1,n):
        #print int(date[i][:4]),int(date[i][5:7]),int(date[i][8:10])
        day=datefstr(date[i])
        lastday=datefstr(date[i-1])
        gap=day-lastday
        if gap.days>1:
            gaps0.append(gap.days)
            gap_index.append(i)
    gaps1=[gap_index[i]-gap_index[i-1] for i in range(1,len(gap_index))]
    gaps1.append(n-gap_index[-1])
    gaps0.append(0)
    #print gap_index,gaps1,gaps0
    if len(gap_index)<=1:
        return ts
    else:
        m=len(gap_index)
        for i in range(m):
            if gaps1[0]<9:
                gap_index=gap_index[1:]  
                gaps1=gaps1[1:]
                gaps0=gaps0[1:]
            else:
                break
        #return len(gap_index)
        
        #print gap_index,gaps1,gaps0
        for i in range(len(gap_index)-2,-1,-1):
            #print "gap_index: ",gap_index[i],gaps0[i],ts[gap_index[i+1]][1]
            for j in range(gaps0[i]-1):
                gap_day=datefstr(ts[gap_index[i+1]][1])
                tmp_day=gap_day-datetime.timedelta(days=1)
                tmp_day=tmp_day.strftime("%Y-%m-%d")
                ts.insert(gap_index[i+1], [0,tmp_day])
                #print i,gap_index[i],gap_day,tmp_day
        ts=ts[gap_index[0]:]
        return ts
        
'''   
#allData=getDataFromFile("253","run_result.txt")
ts=[ [185, '2016-10-09'], [184, '2016-10-10'], [183, '2016-10-11'], [184, '2016-10-12'], [186, '2016-10-13'], [187, '2016-10-14'], [186, '2016-10-15'], [185, '2016-10-16'], [185, '2016-10-17'], [188, '2016-10-18'],[189, '2016-10-25'], [189, '2016-10-26'], [191, '2016-10-27'], [189, '2016-10-28'], [190, '2016-10-29'], [189, '2016-10-30'], [191, '2016-10-31'], [191, '2016-11-01'], [194, '2016-11-14'], [197, '2016-11-15'], [197, '2016-11-16'], [198, '2016-11-17'], [200, '2016-11-18'], [198, '2016-11-19'], [197, '2016-11-20'], [199, '2016-11-21'], [199, '2016-11-22'], [199, '2016-11-23'], [201, '2016-11-24'], [200, '2016-11-25'], [198, '2016-11-26'], [194, '2016-11-27'], [200, '2016-11-28'], [200, '2016-11-29'], [202, '2016-11-30']]
print ts
ts0=connect_today(ts,"2016-12-01")
print ts0


ts1=date_completion(ts0)
print ts1
'''
def is_stable(dataSub):
    n=0
    for i in range(7,len(dataSub)):
        test_data=[dataSub[j][0] for j in range(i-7,i)]
        
        mean=np.mean(test_data)
        std=np.std(test_data)
        if std==0 and mean>0:
            n=n+1
            #print test_data
    if n>3:
        return True
    else:
        return False

#异常值检测 若为异常则标注为 except 否则为 normal 
def exceptionDetection(ts):  ## eg:ts=[['2016/10/24', '246737'], ['2016/10/25', '245820'], ['2016/10/26', '249504']]
    n=len(ts)
    exceptIndex=[]
    ts1=[]
    for i in range(n):
        if ts[i][0]>0:
            ts1.append([ts[i][0],ts[i][1],"normal"])
        else:
            ts1.append([ts[i][0],ts[i][1],"except"])
    for i in range(7,n):
        refer=[int(ts1[j][0]) for j in range(i-7,i)]
        test_before=int(ts1[i-1][0])
        test=int(ts1[i][0])
        mean=np.mean(refer)
        std=np.std(refer)
        
        if abs(test-mean)>std*3:
            ts1[i][2]="except"
            exceptIndex.append((ts[i][1],"except"))
#         elif abs(test-test_before)<std and ts1[i-1][2]=="except":
#             ts1[i][2]="except"
#             exceptIndex.append((ts[i][1],"except"))
            #print ts[i][0],refer,mean,test,std
    #print exceptIndex
    return ts1

## 针对每个 dateSub 获得其 train_datas 和 test_data 
## train_data features的值若为异常则抛弃不用 
def getTrainTest(dataSub,winLen):
    n=len(dataSub)
    train_data=[]
    test_data=[]
    for i in range(winLen,n-1):
        if dataSub[i][2]=="normal":
            no_except=True
            for j in range(i-winLen,i):
                if dataSub[j][2]=="except":
                    no_except=False
            if  no_except:
                train_cell=[[dataSub[j][0] for j in range(i-winLen,i)],dataSub[i][0],dataSub[i][1]]
                train_data.append(train_cell)
    test_no_except=True
    for i in range(n-winLen-1,n-1):
        #print dataSub[i]
        if dataSub[i][2]=="except":
            test_no_except=False
    if test_no_except:
        test_data=[[dataSub[j][0] for j in range(n-1-winLen,n-1)],dataSub[n-1][0],dataSub[n-1][1]]
    return train_data,test_data

## KNN 回归值
def KNNRegression(trainData,testData,K): 
    simList=[]
    means=[]
    refers=[]
    adjust_refers=[]
    #print trainData,testData
    for i in range(len(trainData)):
        sim=kr.correlation(trainData[i][0], testData[0])
        simList.append((sim,i))
        means.append(np.mean(trainData[i][0]))
        refers.append(trainData[i] [1])
        adjust_refers.append(trainData[i][1]-np.mean(trainData[i][0]))
    simList.sort(key=lambda x:x[0],reverse=True)
 
    #print testData,simList
#     print means
#     print refers
#     print adjust_refers
    
    probas=[]
    preds=[]
    testMean=np.mean(testData[0])
    for i in range(K):
        if simList[i][0]>0.7:
            probas.append(simList[i][0])
            preds.append((testMean+adjust_refers[simList[i][1]]))
    #print preds,probas
    testValue=testData[1]
    if len(probas)>0:
        predValue=sum([preds[i]*probas[i] for i in range(len(preds))])/sum(probas)
    else:
        predValue=None
    return testValue,predValue,testMean

def test():
    
    for i in range(239,240):#  range(200,300)
        taskid=str(i)
        ts=getDataFromFile(taskid,"run_result.txt")
        if len(ts)<65:
            #print taskid,"the length of ts is less than 35"
            continue
        else:
            ts=connect_today(ts, "2016-12-01")
            ts=date_completion(ts)
            stable=is_stable(ts)
            if stable:
                #print taskid,"the ts is constance"
                pass
            else:
                ts=exceptionDetection(ts)
                tsLen=len(ts)
                test_except=[]
                test_unpred=[]
                test_norefer=[]
                est_list=[]
                #print len(ts),ts
                for i in range(tsLen-60,tsLen-40):
                    dataSub=ts[:i]
                    if dataSub[-1][2]=="except":
                        test_except.append(dataSub[-1])
                    else:
                        train_data,test_data=getTrainTest(dataSub,7)
                        #print test_data
                        if len(train_data)>0 and len(test_data)>0:
                            testValue,predValue,testMean=KNNRegression(train_data,test_data,1)
                            if predValue==None:
                                test_unpred.append(dataSub[-1])
                                #print test_data[2],"can't be predict"
                            else:
                                est_value=abs(predValue-testValue)/float(testValue)
                                est_list.append((est_value,test_data[2]))
                                #est_list.append(est_value)
                        elif len(train_data)==0:
                            test_norefer.append(dataSub[-1])
                        elif len(test_data)==0:
                            test_unpred.append(dataSub[-1])
                if len(est_list)>0:
                    print taskid,len(test_except),len(test_unpred),len(test_norefer),len(est_list),est_list#,max(est_list),np.mean(est_list)
                else:
                    print taskid,len(test_except),len(test_unpred),len(test_norefer)
                #print sorted(est_list,key=lambda x:x[0],reverse=True)
                if len(test_except)>0:
                    #print taskid,len(test_except_record),test_except_record
                    pass
            
#test()




