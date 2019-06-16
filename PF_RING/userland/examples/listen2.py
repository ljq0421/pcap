# -*- coding: UTF-8 -*-
import os
import time
import sys
devs=[]
p=os.popen('ifconfig|grep tap')
strr=p.read()
strr=strr.split('\n')
devnum=len(strr)-1
for i in range(devnum):
        dev=strr[i][0:14]
        devs.append(dev)
print devs
print("请输入报警类型：")
print("1.超过阈值  2.波动超过阈值  3.某时刻超过阈值  4.某时间内超过阈值")
typ=input()#警报类型
if typ==1:#超过阈值
        maxx=input("请输入设定的阈值：")
elif typ==2:#波动超过阈值
        maxx=input("请输入设定的阈值：")
elif typ==3:#某时刻查过阈值
        maxx=input("请输入设定的阈值：")
        tim=input("请输入报警时刻：hh:mm")

while True:
	if typ==1:#超过阈值
		for i in range(devnum):
			p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
			p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
			rxpre=p1.read()
			txpre=p2.read()
			time.sleep(1)
			p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
        		p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
			rxnext=p1.read()
			txnext=p2.read()
			rx=int(rxnext)-int(rxpre)
			tx=int(txnext)-int(txpre)
			print devs[i],str(rx),str(tx)
			if rx>maxx*1024*1024 or tx>maxx*1024*1024:#maxx MB/s	
				print 'python mysqlq.py 4 '+devs[i]	
				os.system('python mysqlq.py 4 '+devs[i])
	elif typ==2:#波动超过阈值
		maxx=input("请输入设定的阈值：")
		rx1=0
		tx1=0
                for i in range(devnum):
                        p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
                        p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
                        rxpre=p1.read()
                        txpre=p2.read()
                        time.sleep(1)
                        p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
                        p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
                        rxnext=p1.read()
                        txnext=p2.read()
                        rx2=int(rxnext)-int(rxpre)
                        tx2=int(txnext)-int(txpre)
                        print devs[i],str(rx),str(tx)
			if rx1!=0 or tx1!=0:
                        	if (rx2-rx1)>int(maxx)*1024*1024 or (tx2-tx1)>int(maxx)*1024*1024:#maxx MB/s
                                	print 'python mysqlq.py 4 '+devs[i]
                                	os.system('python mysqlq.py 4 '+devs[i])
			rx1=rx2
			tx1=tx2
	elif typ==3:#某时刻查过阈值
		#print("请输入设定的阈值：")
                #maxx=sys.argv[2]
		#print("请输入报警时刻：hh:mm")
		#tim=sys.argv[3]
		t=time.strftime("%H:%M")
                for i in range(devnum):
                        p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
                        p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
                        rxpre=p1.read()
                        txpre=p2.read()
                        time.sleep(1)
                        p1=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $2}'")
                        p2=os.popen("cat /proc/net/dev | grep "+devs[i]+"| sed 's/:/ /g' | awk '{print $10}'")
                        rxnext=p1.read()
                        txnext=p2.read()
                        rx=int(rxnext)-int(rxpre)
                        tx=int(txnext)-int(txpre)
                        print devs[i],str(rx),str(tx)
                        if tim==t:
                                if rx>maxx*1024*1024 or tx>maxx*1024*1024:#maxx MB/s
                                        print 'python mysqlq.py 4 '+devs[i]
                                        os.system('python mysqlq.py 4 '+devs[i])
	
				
