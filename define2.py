# -*- coding: UTF-8 -*-
#python /root/pcap/define2.py 06328 object1:src_ip:10.10.22.9#object2:src_ip:10.10.89.20#object3:dst_ip:10.10.22.3dst_mac:ff:ff:ff:ff:ff:ff#dst_port:123# rulestate:warn%apptype:Telnet#transtype:TCP#nettype:RARP#fieldtype:timestamp#src_ip#src_mac#src_port#dst_ip#dst_mac#dst_port#Network-Layer-Protocol#Transport-Layer-Protocol#Application-Layer-protocol#Payload#TIME:Monthly,Day3,Starttime2,Endtime2% open
import os
import sys
import MySQLdb
import time
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='test',passwd='MyNewPass@123',port=3306,charset='utf8')
db_ins=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursort=db_test.cursor()
cursori=db_ins.cursor()

ruleid=sys.argv[1]
rulename=sys.argv[2]
ruleobject=sys.argv[3]
ruleinfo=sys.argv[4]
rulestate=sys.argv[5]

cursori.execute("update rules set rulestate='"+rulestate+"' where ruleid=" + ruleid)
db_ins.commit()

object=ruleobject.split("object")

olen=len(object)
OBJ=[]
for i in range(olen):
    obj = []
    spname = object[i].find("spname")
    dpname = object[i].find("dpname")
    svname = object[i].find("svname")
    dvname = object[i].find("dvname")
    sip=object[i].find("src_ip")
    smac = object[i].find("src_mac")
    sport = object[i].find("src_port")
    dip = object[i].find("dst_ip")
    dmac = object[i].find("dst_mac")
    dport = object[i].find("dst_port")
    if sip!=-1:
        #obj.append(object[i][sip:object[i].find("#",sip)])
        obj.append({"src_ip":object[i][sip+7:object[i].find("#", sip)]})
    if smac!=-1:
        obj.append({"src_mac":object[i][smac+8:object[i].find("#", smac)]})
    if sport!=-1:
        obj.append({"src_port":object[i][sport+9:object[i].find("#", sport)]})
    if dip != -1:
        obj.append({"dst_ip":object[i][dip+7:object[i].find("#", dip)]})
    if dmac != -1:
        obj.append({"dst_mac":object[i][dmac+8:object[i].find("#", dmac)]})
    if dport != -1:
        obj.append({"dst_port":object[i][dport+9:object[i].find("#", dport)]})
    if spname!=-1:
        obj.append({"spname":object[i][spname+7:object[i].find("#", spname)]})
    if svname!=-1:
        obj.append({"svname":object[i][svname+7:object[i].find("#", svname)]})
    if dpname != -1:
        obj.append({"dpname": object[i][dpname + 7:object[i].find("#", dpname)]})
    if dvname != -1:
        obj.append({"dvname": object[i][dvname + 7:object[i].find("#", dvname)]})

    print "obj",obj
    if len(obj)!=0:OBJ.append(obj)
print "OBJ",OBJ

if ruleinfo.count("TIME")!=0:TIME=ruleinfo.index("TIME")
else:TIME=-1
if ruleinfo.count("fieldtype")!=0:field=ruleinfo.index("fieldtype")
else:field=TIME
if ruleinfo.count("nettype")!=0:net=ruleinfo.index("nettype")
else:net=field
if ruleinfo.count("transtype")!=0:trans=ruleinfo.index("transtype")
else:trans=net
if ruleinfo.count("apptype")!=0:app=ruleinfo.index("apptype")
else:app=trans
if ruleinfo.count("record")!=0:state="record"
elif ruleinfo.count("warn")!=0:state="warn"
else:state="true"#记录/告警：state

typee=[[],[],[],[]]

apptype=ruleinfo[app:trans]
transtype=ruleinfo[trans:net]
nettype=ruleinfo[net:field]
fieldtype=ruleinfo[field:TIME]
TIMEtype=ruleinfo[TIME:-1]

apptype=apptype[8:]
typee[0]={"apptype":apptype.split("#")}
transtype=transtype[10:]
typee[1]={"transtype":transtype.split("#")}
nettype=nettype[8:]
typee[2]={"nettype":nettype.split("#")}
fieldtype=fieldtype[10:].split("#")
ftt=[]
proto=0
for ft in fieldtype:
    if ft=="Network-Layer-Protocol":
        ftt.append("proto")
        proto=1
    elif ft=="Transport-Layer-Protocol" and proto!=1:
        ftt.append("proto")
    elif ft == "Transport-Layer-Protocol" and proto == 1:
        continue
    elif ft=="Application-Layer-protocol":ftt.append("type")
    elif ft == "Payload":ftt.append("info")
    else:ftt.append(ft)
typee[3]={"fieldtype":ftt}

print typee[0],typee[1],typee[2],typee[3]

while True:
    cursort.execute("select count(*) from protocol")
    db_test.commit()
    idmax0 = cursort.fetchone()
    idmax1 = int(str(idmax0)[1:-3])
    query="select * from protocol where id>'"+str(idmax1)+"' "
    first=0

    flag=0
    ap = 0
    for i in range(len(typee[0]["apptype"])-1):
        if typee[0]["apptype"][i]!="":
            flag=1
            if i==0:
                query+="and (type='"+typee[0]["apptype"][i]+"' "
                ap=1
            elif i==len(typee[0]["apptype"])-2 and len(typee[1]["transtype"])==1 and len(typee[2]["nettype"])==1:
                query+="or type='"+typee[0]["apptype"][i]+"') "
                ap=0
            else:query+="or type='"+typee[0]["apptype"][i]+"' "
    if ap==1:query+=")"

    tp=0
    for i in range(len(typee[1]["transtype"])):
        if typee[1]["transtype"][i]!="":
            if i==0:
                query+="and (proto='"+typee[1]["transtype"][i]+"' "
                tp=1
            else:
                query+="or proto='"+typee[1]["transtype"][i]+"' "
                tp=1
            flag=1

    np=0
    for i in range(len(typee[2]["nettype"])):
        if typee[2]["nettype"][i]!="":
            if flag==0 and i==0:
                query+="and (proto='"+typee[2]["nettype"][i]+"' "
                np=1
            elif flag==1 and i==0 and len(typee[1]["transtype"])==1:
                query+="and (proto='"+typee[2]["nettype"][i]+"' "
                np=1
            else:
                query+="or proto='"+typee[2]["nettype"][i]+"' "
                np=1
            flag=1
    if np==1 or tp==1:query+=")"

    for i in range(olen-1):
        for j in range(len(OBJ[i])):
            k =OBJ[i][j].keys()[0]
            item = OBJ[i][j].get(k)
            if k!="spname" and k!="svname" and k!="dpname" and k!="dvname":
                if flag == 0 and i == 0:
                    if j == 0:
                        query += "and (" + k + "='" + item + "' "
                    else:
                        query += "and " + k + "='" + item + "' "
                elif flag == 1 and i == 0:
                    if j == 0:
                        query += "and (" + k + "='" + item + "' "
                    else:
                        query += "and " + k + "='" + item + "' "
                elif i != 0:
                    if j == 0:
                        query += "or " + k + "='" + item + "' "
                    else:
                        query += "and " + k + "='" + item + "' "
                flag = 1

    query+=")"
    print query
    cursort.execute(query)
    db_test.commit()
    result = cursort.fetchall()
    while len(result)==0:
        time.sleep(0.00001)
        cursort.execute(query)
        db_test.commit()
        result = cursort.fetchall()

    cursort.execute("update protocol set state='"+state+"' where id=" + str(result[0][0]))
    db_test.commit()
    strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][7] + '","dst_mac":"' + result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + result[0][11] + '","state":"' + state + '"}\''
    print strr
    os.system(strr)
    
    #result[9]->pid
    pname=""
    vname=""
    for k in OBJ:
        for i in k:
            key=i.keys()[0]
            if i.get(key)==result[0][3]:
                for j in k:
                    if j.keys()[0]=="spname":pname=j.get("spname")
                    elif j.keys()[0]=="svname":vname=j.get("svname")
            elif i.get(key)==result[0][5]:
                for j in k:
                    if j.keys()[0] == "dpname":pname = j.get("dpname")
                    elif j.keys()[0] == "dvname":vname = j.get("dvname")

    query2 = "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values('"+ruleid + "','" +result[0][9] + "','"+pname + "','"+vname + "','"   +result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','"+ result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')"

    print query2
    cursori.execute(query2)
    db_ins.commit()
db_ins.close()
db_test.close()


