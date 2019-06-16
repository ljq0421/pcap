# -*- coding:UTF-8 -*-
import os
devs=[]
p=os.popen('ifconfig|grep tap')
strr=p.read()
strr=strr.split('\n')
devnum=len(strr)-1
for i in range(devnum):
        dev=strr[i][0:14]
        devs.append(dev)
	p=os.popen('nohup ./pfcount -i '+dev+' -v 2 -H 5 &')


