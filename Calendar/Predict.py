#coding=utf-8
'''
Created on 2016年11月28日

@author: 58
'''
import MySQLdb
from PredictTest import *

DatabaseInfo = {
    'host': '10.126.89.68',
    'user': 'system',
    'passwd': 'ecdata_system@0914',
    'port': 3306,
    'charset': 'utf8'
}

TODAY="2016-12-01"

def get_ts(taskid,data_info):
    ts=[]
    conn = MySQLdb.connect(**data_info)
    conn.select_db("task")
    cur=conn.cursor()
    fetech_sql="SELECT result_count,run_date FROM jobs_run_log WHERE task_id=%s ORDER BY run_date"%taskid # and run_date<'2016-11-30'
    #print fetech_sql
    cur.execute(fetech_sql)
    r=cur.fetchall()
    for i in r:
        ts.append([i[0],i[1]])
    cur.close()
    conn.close()
    return ts
   
def get_test_pred(ts,today):
    ts_len=len(ts)
    if ts_len<35:
        print "the len(ts) is less than 35"
        pass
    else:
        ts=connect_today(ts, today)
        if ts is None:
            print "the latest day from today is more than 7 days"
            pass
        else:
            ts=date_completion(ts)
            stable=is_stable(ts)
            if stable:
                print "the ts likes constance seqence"
                pass
            else:       #只对对满足以上条件的时间序列进行预测
                ts=exceptionDetection(ts)
                #print ts
                n=len(ts)
                pred_train,pred_test=getTrainTest(ts,7)
                #print "pred_test",pred_train,pred_test
                if len(pred_test)==0:
                    print ts[-7:]
                    print "the pred_test is empty"
                    pass
                else:
                    test_excep=[]
                    test_est=[]
                    for i in range(n-28,n):
                        ts_sub=ts[:i]
                        #print ts_sub[-1]
                        if ts_sub[-1][2]=="except":
                            test_excep.append([ts_sub[-1][1],"except"])
                        else:
                            train_data,test_data=getTrainTest(ts_sub,7)
                            if len(test_data)==0:
                                test_excep.append([ts_sub[-1][1],"no_test"])
                            elif len(train_data)==0:
                                test_excep.append([ts_sub[-1][1],"no_train"])
                            else:
                                test_value,pred_value,test_mean=KNNRegression(train_data,test_data,1)
                                if pred_value==None:
                                    test_excep.append([ts_sub[-1][1],"no_similar"])
                                else:
                                    est_value=abs(pred_value-test_value)/float(test_value)
                                    test_est.append(est_value)
    #                                 test_est.append([est_value,test_data[2]])
                    #print test_excep,test_est
                    if len(test_est)<5:
                        print "len(test_est) is less than 5"
                        pass
                    else:
                        est_avg=np.mean(test_est)
                        est_max=max(test_est)
                        #print est_avg,est_max
                        if est_avg>=0.3 or est_max>=0.8:
                            #print test_excep,test_est
                            print "don't fit (est_avg<0.3 and est_max<0.8)"
                        else:
                            pred_value=KNNRegression(pred_train, pred_test, 1)
                            if pred_value[1] is None:
                                print "the pred has no similar"
                            else:
                                vary_range=max([est_avg*3,est_max])
                                #print "pred_value is ",[pred_value[1]*(1-vary_range),pred_value[1]*(1+vary_range)]
                                return [pred_value[1]*(1-vary_range),pred_value[1]*(1+vary_range)]
                            
def get_vary_range(taskid,today):
    ts=get_ts(str(taskid), DatabaseInfo)
    value_range=get_test_pred(ts,"2016-12-14")
    return value_range
    
        
def pred_test():
    for i in range(100,1000):
        ts=get_ts(str(i), DatabaseInfo)
        if len(ts)>0:
            value_range=get_test_pred(ts,"2016-12-13")
            print str(i),value_range
    
pred_test()


        
    