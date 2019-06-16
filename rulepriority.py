# -*- coding: UTF-8 -*-
#0: "rule1 demo1-4,demo1-5 SSH告警:源ip:10.10.87.22;目的ip:10.10.87.21;端口号:22;方向:出;生效时间:0:00-1:00 open close"
#96: "rule59 demo1-4,demo1-5 扫描告警:源ip:10.10.87.22%目的ip:10.10.87.22%端口号:33%方向:出%生效时间:00:00-11:00 close open"
import sys
import MySQLdb
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor=db_test.cursor()
ruleindex=sys.argv[1]
ruleid=sys.argv[2]
rulename=sys.argv[3]
ruleobject=sys.argv[4]
ruleinfo=sys.argv[5]
rulestate=sys.argv[6]
if ruleindex=='0':
    cursor.execute("truncate table rules")
    db_test.commit()
cursor.execute("insert into rules (ruleid,rulename,ruleobject,ruleinfo,rulestate) values ('"+ruleid+"','"+rulename+"','"+ruleobject+"','"+ruleinfo+"','"+rulestate+"')")
print "insert into rules (rulename,ruleobject,ruleinfo,rulestate) values ('"+ruleid+"','"+rulename+"','"+ruleobject+"','"+ruleinfo+"','"+rulestate+"')"
db_test.commit()
db_test.close()

