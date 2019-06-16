# -*- coding: UTF-8 -*-
import sys
import MySQLdb
import time
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor=db_test.cursor()
ruleid=sys.argv[1]
rulename=sys.argv[2]
ruleobject=sys.argv[3]
ruleinfo=sys.argv[4]
rulestate=sys.argv[5]
print ruleid,rulename,ruleobject,ruleinfo,rulestate
print "insert into rules (rulename,ruleobject,ruleinfo,rulestate,ruleid) values ('"+rulename+"','"+ruleobject+"','"+ruleinfo+"','"+rulestate+"','"+ruleid+"')"
cursor.execute("insert into rules (rulename,ruleobject,ruleinfo,rulestate,ruleid) values ('"+rulename+"','"+ruleobject+"','"+ruleinfo+"','"+rulestate+"','"+ruleid+"')")
db_test.commit()
db_test.close()
