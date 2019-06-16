# -*- coding: UTF-8 -*-
#python /root/pcap/makerule.py 1559898148220 06725 xhj_1,wyy 指标类型:index-cpu;大小关系:index-dy;阈值:123;生效时间:05:00-06:00 open

import os
import sys
ruleid=sys.argv[1]
rulename=sys.argv[2]
ruleobject=sys.argv[3]
ruleinfo=sys.argv[4]
rulestate=sys.argv[5]
print ruleid,rulename,ruleobject,ruleinfo,rulestate
if ruleinfo.count("index")!=0:
    #python /root/pcap/indexwarning.py rulename ruleobject indextype indexsymbol indexnum
    ruleobject=ruleobject.split(',')
    info=ruleinfo.split(';')
    indextype=info[0][13:]
    indexsymbol = info[1][13:]
    indexnum = info[2][7:]
    for object in  ruleobject:
        os.system("python /root/pcap/indexwarning.py "+rulename+" "+object+" "+indextype+" "+indexsymbol+" "+indexnum)
else:
    #python /root/pcap/indexwarning.py rulename ruleobject incidenttype
    ruleobject = ruleobject.split(',')
    info = ruleinfo.split(';')
    detail=info[0].split('%')
    if detail[0].count('SSH')!=0:
        # python /root/pcap/makerule.py 1559900070906 06726 wyy_huge,wyy 'SSH记录:源ip:10.10.89.12%目的ip:10.10.22.3%端口号:22%方向:进;生效时间:06:00-06:00' open
        incidenttype='incident-ssh'
        #sshsip,sshdip,sshport,sshdir,sshtype,startt,endt
        sshsip=detail[0][16:]
        sshdip=detail[1][9:]
        sshport=detail[2][10:]
        if detail[3].count("进")!=0:sshdir="ssh-in"
        else:sshdir="ssh-out"
        if detail[0].count('记录') != 0:sshtype="ssh-happen"
        else:sshtype="ssh-warn"
        if len(info)==2:
            startt = info[1][13:15]
            if startt[0] == '0': startt = startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
	    for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning2.py ' + ruleid+' '+rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + sshsip + ' ' + sshdip + ' ' + sshport + ' ' + sshdir + ' ' + sshtype + ' ' + startt + ' ' + endt + ' &'
                os.system('python /root/pcap/incidentwarning2.py ' + ruleid+' '+rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + sshsip + ' ' + sshdip + ' ' + sshport + ' ' + sshdir + ' ' + sshtype + ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning1.py ' + ruleid+' '+rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + sshsip + ' ' + sshdip + ' ' + sshport + ' ' + sshdir + ' ' + sshtype + ' &'
                os.system('python /root/pcap/incidentwarning1.py ' + ruleid+' '+rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + sshsip + ' ' + sshdip + ' ' + sshport + ' ' + sshdir + ' ' + sshtype + ' &')

    elif detail[0].count('数据库')!=0:
        #python /root/pcap/makerule.py 1559901642745 06732 xhj 数据库记录:源ip:10.10.89.24%目的ip:10.10.22.9%端口号:3306%方向:出%数据库语句:select%*%from%jjj;生效时间:05:00-06:00 open
        incidenttype = 'incident-db'
        # dbsip,dbdip,dbport,dbdir,dbtype,dbstate,startt,endt
        dbsip = detail[0][22:]
        dbdip = detail[1][9:]
        dbport = detail[2][10:]
        dbstate=detail[4][16:]
        for i in range(5,len(detail)):
            dbstate+="%"+detail[i]
        if detail[3].count("进") != 0:
            dbdir = "db-in"
        else:
            dbdir = "db-out"
        if detail[0].count('记录') != 0:
            dbtype = "db-happen"
        else:
            dbtype = "db-warn"
        if len(info) == 2:
            startt = info[1][13:15]
            if startt[0] == '0': startt = startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
            for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + dbsip + ' ' + dbdip + ' ' + dbport + ' ' + dbdir + ' ' + dbtype + ' '+dbstate+ ' ' + startt + ' ' + endt + ' &'
                os.system('python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + dbsip + ' ' + dbdip + ' ' + dbport + ' ' + dbdir + ' ' + dbtype + ' '+dbstate+ ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + dbsip + ' ' + dbdip + ' ' + dbport + ' ' + dbdir + ' ' + dbtype + ' '+dbstate+ ' &'
                os.system('python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + dbsip + ' ' + dbdip + ' ' + dbport + ' ' + dbdir + ' ' + dbtype + ' '+dbstate+ ' &')

    elif detail[0].count('扫描') != 0:
        incidenttype = 'incident-scan'
        #python /root/pcap/makerule.py 1559950520791 06801 wyy 扫描记录:源ip:10.10.22.10%目的ip:10.10.89.21%端口号:%方向:出;生效时间:06:00-06:00 open
        scansip = detail[0][19:]
        scandip = detail[1][9:]
        scanport = detail[2][10:]
        if detail[3].count("进") != 0:
            scandir = "scan-in"
        else:
            scandir = "scan-out"
        if detail[0].count('记录') != 0:
            scantype = "scan-happen"
        else:
            scantype = "scan-warn"
        if len(info) == 2:
            startt = info[1][13:15]
            if startt[0] == '0': startt = startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
            for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + scansip + ' ' + scandip + ' ' + scanport + ' ' + scandir + ' ' + scantype + ' ' + startt + ' ' + endt + ' &'
                os.system('python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + scansip + ' ' + scandip + ' ' + scanport + ' ' + scandir + ' ' + scantype + ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                print 'python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + scansip + ' ' + scandip + ' ' + scanport + ' ' + scandir + ' ' + scantype + ' &'
                os.system('python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + scansip + ' ' + scandip + ' ' + scanport + ' ' + scandir + ' ' + scantype + ' &')

    elif detail[0].count('FTP') != 0:
        incidenttype = 'incident-ftp'
        #python /root/pcap/makerule.py 1559950808005 06802 wyy FTP告警:源ip:10.10.22.10%目的ip:10.10.89.21%端口号:21%方向:进%禁止的ftp操作:,ACCT;生效时间:06:00-10:00 open
        #python /root/pcap/makerule.py 1559950820477 06802 wyy FTP告警:源ip:10.10.22.10%目的ip:10.10.89.21%端口号:21%方向:进%禁止的ftp操作:,ACCT,DELE;生效时间:06:00-10:00 open
        ftpsip = detail[0][16:]
        ftpdip = detail[1][9:]
        ftpport = detail[2][10:]
        if detail[3].count("进") != 0:
            ftpdir = "ftp-in"
        else:
            ftpdir = "ftp-out"
        if detail[0].count('记录') != 0:
            ftptype = "ftp-happen"
        else:
            ftptype = "ftp-warn"
        ban=detail[4].split(',')
        print ban
        if len(info) == 2:
            startt = info[1][13:15]
            if startt[0]=='0':startt=startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
            for i in range(len(ruleobject)):
                for j in range(1,len(ban)):
                    print 'python /root/pcap/incidentwarning2.py ' + ruleid +' '+ rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + ftpsip + ' ' + ftpdip + ' ' + ftpport + ' ' + ftpdir + ' ' + ftptype + ' ' + ban[j] + ' ' + startt + ' ' + endt + ' &'
                    os.system('python /root/pcap/incidentwarning2.py ' + ruleid +' '+ rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + ftpsip + ' ' + ftpdip + ' ' + ftpport + ' ' + ftpdir + ' ' + ftptype + ' ' +ban[j] + ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                for j in range(1,len(ban)):
                    print 'python /root/pcap/incidentwarning1.py '+ ruleid +' '+rulename+' '+ruleobject[i]+' '+incidenttype + ' ' + ftpsip + ' ' + ftpdip + ' ' + ftpport + ' ' + ftpdir + ' ' + ftptype + ' ' + ban[j] + ' &'
                    os.system('python /root/pcap/incidentwarning1.py '+ ruleid +' '+rulename+' '+ruleobject[i]+' ' + incidenttype + ' ' + ftpsip + ' ' + ftpdip + ' ' + ftpport + ' ' + ftpdir + ' ' + ftptype + ' ' +ban[j] + ' &')

    elif detail[0].count('HTTP') != 0:
        incidenttype = 'incident-http'
        #python /root/pcap/makerule.py 1559951363501 06802 wyy HTTP告警:源ip:10.10.89.21%目的ip:10.10.89.21%端口号:80%方向:进%禁止的http操作:,registerAdmin,registerUser,searchGoods,formGoods;生效时间:06:00-10:00 open
        httpsip = detail[0][17:]
        httpdip = detail[1][9:]
        httpport = detail[2][10:]
        if detail[3].count("进") != 0:
            httpdir = "http-in"
        else:
            httpdir = "http-out"
        if detail[0].count('记录') != 0:
            httptype = "http-happen"
        else:
            httptype = "http-warn"
        ban = detail[4].split(',')
        print ban
        if len(info) == 2:
            startt = info[1][13:15]
            if startt[0] == '0': startt = startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
            for i in range(len(ruleobject)):
                for j in range(1, len(ban)):
                    print 'python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + httpsip + ' ' + httpdip + ' ' + httpport + ' ' + httpdir + ' ' + httptype + ' ' +ban[j] + ' ' + startt + ' ' + endt + ' &'
                    os.system('python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + httpsip + ' ' + httpdip + ' ' + httpport + ' ' + httpdir + ' ' + httptype + ' ' +ban[j] + ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                for j in range(1, len(ban)):
                    print 'python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + httpsip + ' ' + httpdip + ' ' + httpport + ' ' + httpdir + ' ' + httptype + ' ' + ban[j] + ' &'
                    os.system('python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + httpsip + ' ' + httpdip + ' ' + httpport + ' ' + httpdir + ' ' + httptype + ' ' +ban[j] + ' &')

    elif detail[0].count('拒绝服务') != 0:
        incidenttype = 'incident-dos'
        #python /root/pcap/makerule.py 1559951843093 06802 xhj_1 拒绝服务攻击类型:,icmp,syn,smurf,fraggle,land;生效时间:05:00-06:00 open
        ban=detail[0].split(',')
        if len(info) == 2:
            startt = info[1][13:15]
            if startt[0] == '0': startt = startt[1]
            endt = info[1][19:-3]
            if endt[0] == '0': endt = endt[1]
            for i in range(len(ruleobject)):
                for j in range(1, len(ban)):
                    print 'python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + ban[j] + ' ' + startt + ' ' + endt + ' &'
                    os.system('python /root/pcap/incidentwarning2.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + ban[j] + ' ' + startt + ' ' + endt + ' &')
        else:
            for i in range(len(ruleobject)):
                for j in range(1, len(ban)):
                    print 'python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' +ban[j] + ' &'
                    os.system('python /root/pcap/incidentwarning1.py ' + ruleid + ' ' + rulename + ' ' + ruleobject[i] + ' ' + incidenttype + ' ' + ban[j] + ' &')


