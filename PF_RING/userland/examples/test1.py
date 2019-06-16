# -*- coding:UTF-8 -*-
import os
import time
import MySQLdb
db_insuser=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor1=db_insuser.cursor()
devs1=[]
names1=[]
p=os.popen('ifconfig|grep tap')
strr1=p.read()
strr=strr1.split('\n')
devnum=len(strr)-1
num=0
for i in range(devnum):
       	dev=strr[i][0:14]
       	devs1.append(dev)
	cursor1.execute("select project_id from ins_user where tap='"+dev+"'")
	namee=cursor1.fetchone()
	namee=str(namee)[3:-3]
	p=os.popen('nohup ./pfcount -i '+dev+' -v 2 -H 5 -U '+namee+' -Q '+str(num)+' &')
	p=os.popen('nohup ./client2 -Q '+str(num)+' &')
	print dev
	num+=1
	#p=os.popen('nohup python trans_elk.py '+dev+' 1>myout'+dev+'.file &')
	#print 'nohup python trans_elk.py '+dev+' 1>myout'+dev+'.file &'
while True:	
	while os.popen('ifconfig|grep tap').read()==strr1:
		time.sleep(0.01)	
	devs2=[]
	strr2=os.popen('ifconfig|grep tap').read()
	strr=strr2.split('\n')
	devnum=len(strr)-1
	for i in range(devnum):
                dev=strr[i][0:14]
		if devs1.count(dev)==0:
			cursor1.execute("select name where tap='"+dev+"'")
        		namee=cursor1.fetchone()
			p=os.popen('nohup ./pfcount -i '+dev+' -v 2 -H 5 -U '+namee+' -Q '+str(num)+' &')
			p=os.popen('nohup ./client2 -Q '+str(num)+' &')
			num+=1
			print 'add',dev
                devs2.append(dev)
        for i in range(len(devs1)):
		if devs2.count(devs1[i])==0:
			dev=devs1[i]
			p=os.popen('pkill -f "./pfcount -i '+dev+' -v 2 -H 5"')
			print 'remove',dev
	devs1=devs2
	strr1=strr2
