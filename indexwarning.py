# -*- coding: UTF-8 -*-
import os
import sys
import time
import MySQLdb
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor=db_test.cursor()
rulename=sys.argv[1]
ruleobject=sys.argv[2]#虚拟机名，要与端口名对应
indextype=sys.argv[3]
indexsymbol=sys.argv[4]
indexnum=sys.argv[5]
cursor.execute("select tap from ins_user where display_name='"+ruleobject+"'")
db_test.commit()
ruleobject=str(cursor.fetchone())[3:-3]
print ruleobject
if indextype=="index-rxnum":#入包量
    while True:
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $3}'")
        rxpre=p1.read()
        time.sleep(1)
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $3}'")
        rxnext=p1.read()
        print rxpre,rxnext
	rx=int(rxnext)-int(rxpre)
        if indexsymbol=="index-dy":
            if rx==int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入包量("+str(rx)+")=阈值("+indexnum+")"
        elif indexsymbol=="index-d":
            if rx>int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入包量("+str(rx)+")＞阈值("+indexnum+")"
        elif indexsymbol=="index-x":
            if rx<int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入包量("+str(rx)+")＜阈值("+indexnum+")"
        elif indexsymbol=="index-dd":
            if rx>=int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入包量("+str(rx)+")≥阈值("+indexnum+")"
        elif indexsymbol=="index-xd":
            if rx<=int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入包量("+str(rx)+")≤阈值("+indexnum+")"
        sys.stdout.flush()

elif indextype=="index-txnum":#出包量
    while True:
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $11}'")
        txpre = p1.read()
        time.sleep(1)
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $11}'")
        txnext = p1.read()
        tx = int(txnext) - int(txpre)
        if indexsymbol == "index-dy":
            if tx == int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出包量("+str(tx)+")=阈值("+indexnum+")"
        elif indexsymbol == "index-d":
            if tx > int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出包量("+str(tx)+")＞阈值("+indexnum+")"
        elif indexsymbol == "index-x":
            if tx < int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出包量("+str(tx)+")＜阈值("+indexnum+")"
        elif indexsymbol == "index-dd":
            if tx >= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出包量("+str(tx)+")≥阈值("+indexnum+")"
        elif indexsymbol == "index-xd":
            if tx <= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出包量("+str(tx)+")≤阈值("+indexnum+")"
        sys.stdout.flush()

elif indextype=="index-rxbw":#入带宽
    while True:
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $2}'")
        rxpre = p1.read()
        time.sleep(1)
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $2}'")
        rxnext = p1.read()
        rx = int(rxnext) - int(rxpre)
        if indexsymbol == "index-dy":
            if rx == int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入带宽("+str(rx)+")=阈值("+indexnum+")"
        elif indexsymbol == "index-d":
            if rx > int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入带宽("+str(rx)+")＞阈值("+indexnum+")"
        elif indexsymbol == "index-x":
            if rx < int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入带宽("+str(rx)+")＜阈值("+indexnum+")"
        elif indexsymbol == "index-dd":
            if rx >= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入带宽("+str(rx)+")≥阈值("+indexnum+")"
        elif indexsymbol == "index-xd":
            if rx <= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  入带宽("+str(rx)+")≤阈值("+indexnum+")"
        sys.stdout.flush()

elif indextype=="index-txbw":#出带宽
    while True:
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $10}'")
        txpre = p1.read()
        time.sleep(1)
        p1 = os.popen("cat /proc/net/dev |grep " + ruleobject + "| sed 's/:/ /g' |awk '{print $10}'")
        txnext = p1.read()
        tx = int(txnext) - int(txpre)
        if indexsymbol == "index-dy":
            if tx == int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出带宽("+str(tx)+")=阈值("+indexnum+")"
        elif indexsymbol == "index-d":
            if tx > int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出带宽("+str(tx)+")＞阈值("+indexnum+")"
        elif indexsymbol == "index-x":
            if tx < int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出带宽("+str(tx)+")＜阈值("+indexnum+")"
        elif indexsymbol == "index-dd":
            if tx >= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出带宽("+str(tx)+")≥阈值("+indexnum+")"
        elif indexsymbol == "index-xd":
            if tx <= int(indexnum):
                print time.asctime( time.localtime(time.time()) )+"  出带宽("+str(tx)+")≤阈值("+indexnum+")"
        sys.stdout.flush()

elif indextype=="index-tcpnum":#TCP连接数
    while True:
        p1=os.popen("netstat -an|grep tcp")
        tcpnum=p1.read().count('tcp')
        if indexsymbol == "index-dy":
            if tcpnum == int(indexnum):
                print time.asctime(time.localtime(time.time())) + "  TCP连接数("+str(tcpnum)+")=阈值(" + indexnum + ")"
        elif indexsymbol == "index-d":
            if tcpnum > int(indexnum):
                print time.asctime(time.localtime(time.time())) + "  TCP连接数("+str(tcpnum)+")＞阈值(" + indexnum + ")"
        elif indexsymbol == "index-x":
            if tcpnum < int(indexnum):
                print time.asctime(time.localtime(time.time())) + "  TCP连接数("+str(tcpnum)+")＜阈值(" + indexnum + ")"
        elif indexsymbol == "index-dd":
            if tcpnum >= int(indexnum):
                print time.asctime(time.localtime(time.time())) + "  TCP连接数("+str(tcpnum)+")≥阈值(" + indexnum + ")"
        elif indexsymbol == "index-xd":
            if tcpnum <= int(indexnum):
                print time.asctime(time.localtime(time.time())) + "  TCP连接数("+str(tcpnum)+")≤阈值(" + indexnum + ")"
        sys.stdout.flush()
        time.sleep(1)





