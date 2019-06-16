# -*- coding: UTF-8 -*-
import os
import sys
import time
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
db_ins = MySQLdb.connect(host='10.10.87.22', user='root', db='ins_user', passwd='MyNewPass@123', port=3306,charset='utf8')
cursori = db_ins.cursor()
ruleid = sys.argv[1]
cursori.execute( "select rulestate from rules where ruleid='" +ruleid+ "'")
db_ins.commit()
state = str(cursori.fetchone())[3:-3]
print "select rulestate from rules where ruleid='" +ruleid+ "'"
print state
if state == 'open':flag = 1
else:flag = 2
if flag==1:#原来是打开的，要关掉
    print "ps x | grep '" + ruleid + "' | grep -v grep | awk '{print $1}' | xargs kill -9"
    cursori.execute("update rules set rulestate='close' where ruleid=" + ruleid)
    db_ins.commit()
    db_ins.close()
    os.system("ps x | grep '"+ruleid + "' | grep -v grep | awk '{print $1}' | xargs kill -9")
else:#原来是关的，要打开-调用define2.py，需要参数：ruleid,rulename,ruleobject,ruleinfo,rulestate(这里应该是open，要把规则打开)
    cursori.execute("select * from rules where ruleid='" + ruleid + "'")
    db_ins.commit()
    str=cursori.fetchone()
    rulename=str[1]
    ruleobject=str[2]
    ruleinfo=str[3]
    rulestate=str[4]
    print ruleid,rulename,ruleobject,ruleinfo,rulestate
    if ruleinfo.count('rulestate')!=0:
        print "python /root/pcap/define2.py "+ruleid+" "+rulename+" "+ruleobject+" "+ruleinfo+" open"
        os.system("python /root/pcap/define2.py "+ruleid+" "+rulename+" "+ruleobject+" "+ruleinfo+" open")
    else:
        print "python /root/pcap/define.py "+ruleid+" "+rulename+" "+ruleobject+" '"+ruleinfo+"' open"
        os.system("python /root/pcap/define.py "+ruleid+" "+rulename+" "+ruleobject+" '"+ruleinfo+"' open")
    cursori.execute("update rules set rulestate='open' where ruleid=" + ruleid)
    db_ins.commit()
    db_ins.close()
