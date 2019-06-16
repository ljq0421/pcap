import MySQLdb
import time
import os
import sys
db_nova=MySQLdb.connect(host='10.10.87.250',user='nova',db='nova',passwd='pdy8QjiuwFdThBuZViRSZM5qOADgmdCobn7XqMQr',port=3306,charset='utf8')
db_keystone=MySQLdb.connect(host='10.10.87.250',user='keystone',db='keystone',passwd='igNaYNsjirbVTElgiGUI5iTYf15rbcN1h4olqgXJ',port=3306,charset='utf8')
db_ins=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor1=db_nova.cursor()
cursor2=db_keystone.cursor()
cursor3=db_ins.cursor()
cursor1.execute("select display_name,uuid,project_id from instances where vm_state='active'")
db_nova.commit()
cds0=cursor1.fetchall()

def MakeInsUser(cds1):
    cursor3.execute('truncate table ins_user')
    db_ins.commit()
    display_name=[]
    uuid=[]
    project_id=[]
    ip1=[]
    ip2=[]
    dev=[]
    mail=[]
    name=[]
    for i in range(len(cds1)):
        ddisplay_name = cds1[i][0]
        uuidd = cds1[i][1]
        project_idd = cds1[i][2]
        display_name.append(str(ddisplay_name))
        uuid.append(str(uuidd))
        project_id.append(str(project_idd))
        cursor1.execute('select substring_index(substring_index(network_info,\'"\',42),\'"\',-1) from instance_info_caches where instance_uuid="' + uuidd + '"')
        addr = cursor1.fetchall()
        if str(addr)[3:-5] == "address":
            cursor1.execute('select substring_index(substring_index(network_info,\'"\',40),\'"\',-1) from instance_info_caches where instance_uuid="' + uuidd + '"')
            ip11 = cursor1.fetchall()
            if len(str(ip11)) > 15:
                ip1.append(str(ip11)[3:-5])
            else:
                ip1.append(' ')
            cursor1.execute('select substring_index(substring_index(network_info,\'"\',44),\'"\',-1) from instance_info_caches where instance_uuid="' + uuidd + '"')
            ip22 = cursor1.fetchall()
            if len(str(ip22)) > 15:
                ip2.append(str(ip22)[3:-5])
            else:
                ip2.append(' ')
        else:
            ip1.append(' ')
            cursor1.execute('select substring_index(substring_index(network_info,\'"\',32),\'"\',-1) from instance_info_caches where instance_uuid="' + uuidd + '"')
            ip22 = cursor1.fetchall()
            if len(str(ip22)) > 15:
                ip2.append(str(ip22)[3:-5])
            else:
                ip2.append(' ')
        cursor3.execute('select substring_index(substring_index(network_info,\'devname": "\',-1),\'"\',1) from ins_use_3 where instance_uuid="' + uuidd + '"')
        devs = cursor3.fetchall()
        dev.append(str(devs)[3:-5])
        cursor2.execute('select substring_index(substring_index(extra,\'"\',4),\'"\',-1) from user where default_project_id="' + project_idd + '"')
        maill = cursor2.fetchall()
        if str(maill).count("@")!=0:
            mail.append(str(maill)[3:-5])
        else:
            mail.append(' ')
        cursor2.execute('select substring_index(substring_index(name,\'"\',4),\'"\',-1) from project where id="' + project_idd + '"')
        namee = cursor2.fetchall()
        if len(str(namee)) > 0:
            name.append(str(namee)[4:-5])
        else:
            name.append(' ')
    for i in range(len(cds1)):
        cursor3.execute('insert into ins_user (display_name,project_id,uuid,float_ip,ip,mail,tap,name) values("' + display_name[i] + '","' + project_id[i] + '","' + uuid[i] + '","' + ip1[i] + '","' + ip2[i] + '","' + mail[i] + '","' + dev[i] + '","' + name[i] + '")')
        db_ins.commit()
    print display_name,uuid,project_id,ip1,ip2,dev,mail,name
    
MakeInsUser(cds0)
while True:
    cursor1.execute("select display_name,uuid,project_id from instances where vm_state='active'")
    db_nova.commit()
    cds2= cursor1.fetchall()
    if cds2!=cds0:
        MakeInsUser(cds2)
        cds0=cds2

db_nova.close()
db_keystone.close()
db_ins.close()

