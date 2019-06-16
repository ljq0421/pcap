# -*- coding: UTF-8 -*-
import sys
import os
import MySQLdb
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor=db_test.cursor()

ruleid=sys.argv[1]
try:
   # 执行SQL语句
   cursor.execute("delete from rules where ruleid='"+ruleid+"'")
   # 向数据库提交
   db_test.commit()
except:
   # 发生错误时回滚
   db_test.rollback()
db_test.close()
os.system("ps x | grep '"+ruleid + "' | grep -v grep | awk '{print $1}' | xargs kill -9")


