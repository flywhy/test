#encoding=utf-8
'''
Created on 2016年12月23日

@author: 58
'''

import MySQLdb
import random

DataBase130=['test','data_chpcl','data_ershouche','data_ershouchuangxin','data_ershoutuiguang','data_fangchan','data_huangye','data_test','data_tmp','data_zhaopin','dm_bi']
DataBase133=['data_app','data_bi','data_chinahr','data_ershou','data_ganji','data_open','data_open_config','data_project','data_supin','dm_app','dm_bi','dm_dales','dm_efficacy','dm_ganji','dm_sales','dm_temp']

Info130={
        'host': '10.126.84.130',
        'user': 'wangheying',
        'passwd': 'MUewGYw&MIwVTw%$',
        'port': 5029,
        'charset': 'utf8'}
Info133={
        'host': '10.126.84.133',
        'user': 'wangheying',
        'passwd': 'MUewGYw&MIwVTw%$',
        'port': 5029,
        'charset': 'utf8'}

def get_conn(data_info):
    try:
        conn = MySQLdb.connect(**data_info)
        return conn
    except:
        print("Can't connect to the database")
        return None

def is_exist(user,DataInfo):
    conn=get_conn(DataInfo)
    conn.select_db("mysql")
    cur=conn.cursor()
    sql="select User from user where User='%s'"%user
    #print sql
    cur.execute(sql)
    r=cur.fetchone()
    if r:
        return True
    else:
        return False

#is_exist("zhangwenjiae",Info130)

def user_judge(users):
    user_rr=[]
    for user in users:
        exist1=is_exist(user,Info130)
        exist2=is_exist(user,Info133)
        if exist1 and exist2:
            user_rr.append([user,"normal"])
        elif not exist1 and not exist2:
            user_rr.append([user,"new"])
        elif exist1 and not exist2:
            user_rr.append([user,"in 130"])
        else:
            user_rr.append([user,"in 133"])
    for i in range(len(user_rr)):
        if user_rr[i][1]!="normal":
            print user_rr[i]
        else:
            print user_rr[i]


def create_users(users_new):
    user_pass=[]
    create_sql=""
    for user in users_new:
        n=len(user)
        rand_index1=random.randint(1,n-1)
        rand_num=random.randint(100,999)
        pwd=user[:rand_index1]+str(rand_num)+random.choice("!@#$%^&*~")+user[rand_index1:]
        #print rand_index1,rand_num,pwd
        user_pass.append([user,pwd])
        create_sql+="CREATE USER %s IDENTIFIED by '%s';\n"%(user,pwd)
    print create_sql
    conn=get_conn(Info130)
    cur=conn.cursor()
    cur.execute(create_sql)
    cur.close()
    conn.close()
    
    conn1=get_conn(Info133)
    cur1=conn1.cursor()
    cur1.execute(create_sql)
    cur1.close()
    conn1.close()
    for i in user_pass:
        print "嗨,数据库权限已开通 以下为连接所需信息：\nip：10.126.84.133|10.126.84.130 \npassport：5029 \nusername：%s \npassword：%s" %(i[0],i[1])
    #print user_pass

def exe_one_item(TestData):
    [database,user0,table0]=TestData.split("#")
    users=user0.split(",")
    tables=table0.split(",")
    #print database,users,tables
    database_info=None
    if database in DataBase130:
        #print 130
        database_info=Info130
    elif database in DataBase133:
        #print 133
        database_info=Info133
    if database_info:
        conn=get_conn(database_info)
        conn.select_db(database)
        cur=conn.cursor()
        if table0=="*":
            grant_sql="grant select on %s.%s to %s;"%(database,table0,user0)
            cur.execute(grant_sql)
        else:
            for table in tables:
                table=table+"%"
                get_table_list="show tables like '%s'"%table
                #print get_table_list
                cur.execute(get_table_list)
                r=cur.fetchall()
                table_list=[i[0] for i in r]
                #print table_list
                for k in table_list:
                    grant_sql="grant select on %s.%s to %s;"%(database,k,user0)
                    print grant_sql
                    cur.execute(grant_sql)
        cur.close()
        conn.close()

def grant(grant_items):
    items=grant_items.split("\n")
    print len(items)
    for i in items:
        print i
    for i in items:
        exe_one_item(i)
    

test_users=["liuzhujie"]
print test_users
user_judge(test_users)
new_users=["liuzhujie"]#,"wuyuan","huangchuan","chenhaihua","dingyuou","wanruijie"]
#create_users(new_users)
grant_items="""data_app#cuichen#t_common_creative_info,t_huangye_other_click_show_sum"""
#grant(grant_items)

