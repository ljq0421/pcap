# -*- coding: UTF-8 -*-
import os
import sys
import time
import MySQLdb
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='test',passwd='MyNewPass@123',port=3306,charset='utf8')
db_ins=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursort=db_test.cursor()
cursori=db_ins.cursor()
ruleid=sys.argv[1]
rulename=sys.argv[2]#规则名称
ruleobject=sys.argv[3]#虚拟机名，要与ip地址对应，与用户id对应
incidenttype=sys.argv[4]#事件报警的哪一种
cursori.execute("select project_id from ins_user where display_name='"+ruleobject+"'")#租户id
db_ins.commit()
project_id=str(cursori.fetchone())[3:-3]
cursori.execute("select name from ins_user where display_name='" + ruleobject + "'")#租户名
db_ins.commit()
project_name = str(cursori.fetchone())[3:-3]
cursori.execute("select ip from ins_user where display_name='"+ruleobject+"'")#该虚拟机对应的ip，暂时只是内部的ip，没有考虑浮动ip
db_ins.commit()
ip=str(cursori.fetchone())[3:-3]
if incidenttype=="incident-ssh":#ssh报警：源ip、目的ip、端口（默认22）、方向（进/出）、类型（记录/报警）
    sshsip=sys.argv[5]
    sshdip=sys.argv[6]
    sshport=sys.argv[7]
    sshdir=sys.argv[8]
    sshtype=sys.argv[9]
    startt = sys.argv[10]
    endt = sys.argv[11]
    while True:
        print startt,endt
        cursort.execute("select count(*) from protocol")
        db_test.commit()
        idmax0 = cursort.fetchone()
        idmax1 = int(str(idmax0)[1:-3])
        if(sshtype=="ssh-happen"):#发生即记录，不论方向
            query = "select * from protocol where type='SSH' and info='SYN first' and name='" + project_id + "' and id>" + str(idmax1)+"  and (src_ip='"+ip+"'"+" or dst_ip='"+ip+"') and (src_port='"+sshport+"'"+" or dst_port='"+sshport+"') and ("
            for i in range(int(startt),int(endt)):
                if i<10:
                    query+="timestamp like '____/__/__/0"+str(i)+"%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt)<10:query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:query += "timestamp like '____/__/__/" + endt + "%' )"
            print query
            cursort.execute(query)
            #sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            while len(result) == 0:
                time.sleep(0.00001)
                cursort.execute(query)
                db_test.commit()
                result = cursort.fetchall()

            query = "update protocol set state='ssh-record' where id=" + str(result[0][0])
            print query
            cursort.execute(query)
            db_test.commit()

            state = "ssh-record"
            strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                       2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                   result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][7] + '","dst_mac":"' + \
                   result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + result[0][
                       11] + '","state":"' + state + '"}\''
            print strr
            os.system(strr)

            cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
            db_ins.commit()
            mail = str(cursori.fetchone())[3:-3]
            cursori.execute(
                "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                result[0][
                    1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
            print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                  result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                  result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                  result[0][10] + "','" + result[0][11] + "')"
            db_ins.commit()
            #sys.stdout.flush()
            os.system('echo "SSH!!!!"|mail -s "warning-SSH" ' + mail)
        elif(sshtype=="ssh-warn"):#禁止，报警，需要区分方向、源/目的ip
            if(sshdir=="ssh-in"):#禁止本虚拟机作为ssh的目的地址,源地址是sshsip
                query = "select * from protocol where type='SSH' and info='SYN first' and name='" + project_id + "' and id>" + str(idmax1)+"  and dst_ip='"+ip+"'"+" and src_ip='"+sshsip+"' and (src_port='"+sshport+"'"+" or dst_port='"+sshport+"') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                print query
                cursort.execute(query)
                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='ssh-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "ssh-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                #sys.stdout.flush()
                os.system('echo "SSH!!!!"|mail -s "warning-SSH" ' + mail)
            elif (sshdir == "ssh-out"):  # 禁止本虚拟机作为ssh的源地址,目的地址是sshdip
                query = "select * from protocol where type='SSH' and info='SYN first' and name='" + project_id + "' and id>" + str(idmax1) + "  and dst_ip='" + sshdip + "'" + " and src_ip='" + ip + "' and (src_port='"+sshport+"'"+" or dst_port='"+sshport+"') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                print query
                cursort.execute(query)
                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='ssh-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "ssh-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                #sys.stdout.flush()
                os.system('echo "SSH!!!!"|mail -s "warning-SSH" ' + mail)
elif incidenttype=="incident-db":#db报警：源ip、目的ip、端口（默认22）、方向（进/出）、类型（记录/报警）、数据库语句
    dbsip=sys.argv[5]
    dbdip=sys.argv[6]
    dbport=sys.argv[7]
    dbdir=sys.argv[8]
    dbtype=sys.argv[9]
    try:
        dbstate=sys.argv[10]
        dbstate = dbstate.replace("#", " ")
    except:
        dbstate=""
    startt = sys.argv[11]
    endt = sys.argv[12]
    while True:
        cursort.execute("select count(*) from protocol")
        db_test.commit()
        idmax0 = cursort.fetchone()
        idmax1 = int(str(idmax0)[1:-3])
        if(dbtype=="db-happen"):#发生即记录，不论方向
            query = "select * from protocol where info='DB' and name='" + project_id + "' and info like '%"+dbstate+"%' and id>" + str(idmax1)+"  and (src_ip='"+ip+"'"+" or dst_ip='"+ip+"') and (src_port='"+dbport+"'"+" or dst_port='"+dbport+"') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)

            #sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            while len(result) == 0:
                time.sleep(0.00001)
                cursort.execute(query)
                db_test.commit()
                result = cursort.fetchall()

            query = "update protocol set state='db-record' where id=" + str(result[0][0])
            print query
            cursort.execute(query)
            db_test.commit()

            state = "db-record"
            strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                       2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                   result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][7] + '","dst_mac":"' + \
                   result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + result[0][
                       11] + '","state":"' + state + '"}\''
            print strr
            os.system(strr)

            cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
            db_ins.commit()
            mail = str(cursori.fetchone())[3:-3]
            cursori.execute(
                "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                result[0][
                    1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
            print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                  result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                  result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                  result[0][10] + "','" + result[0][11] + "')"
            db_ins.commit()
            #sys.stdout.flush()
            os.system('echo "DB!!!!"|mail -s "warning-DB" ' + mail)
        elif(dbtype=="db-warn"):#禁止，报警，需要区分方向、源/目的ip
            if(dbdir=="db-in"):#禁止本虚拟机作为db的目的地址,源地址是dbsip
                query = "select * from protocol where info='DB' and name='" + project_id + "' and info like '%"+dbstate+"%' and id>" + str(idmax1)+"  and dst_ip='"+ip+"'"+" and src_ip='"+dbsip+"' and (src_port='"+dbport+"'"+" or dst_port='"+dbport+"') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='db-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "db-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                #sys.stdout.flush()
                os.system('echo "DB!!!!"|mail -s "warning-DB" ' + mail)
            elif (dbdir == "db-out"):  # 禁止本虚拟机作为db的源地址,目的地址是dbdip
                query = "select * from protocol where info='DB' and name='" + project_id + "' and info like '%"+dbstate+"%' and id>" + str(idmax1) + "  and dst_ip='" + dbdip + "'" + " and src_ip='" + ip + "' and (src_port='"+dbport+"'"+" or dst_port='"+dbport+"') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='db-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "db-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                #sys.stdout.flush()
                os.system('echo "DB!!!!"|mail -s "warning-DB" ' + mail)
elif incidenttype=="incident-scan":
    scansip = sys.argv[5]
    scandip = sys.argv[6]
    scanport = sys.argv[7]
    scandir = sys.argv[8]
    scantype = sys.argv[9]
    startt = sys.argv[10]
    endt = sys.argv[11]
    while True:
        cursort.execute("select count(*) from protocol")
        db_test.commit()
        idmax0 = cursort.fetchone()
        idmax1 = int(str(idmax0)[1:-3])
        if (scantype == "scan-happen"):  # 发生即记录，不论方向
            time.sleep(30)
            query = "select distinct dst_port from protocol where name='" + project_id + "' and id>" + str(idmax1) + "  and dst_ip='" + ip + "') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)
            #sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            if len(result) > 50:
                query = "update protocol set state='scan-record' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "scan-record"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                #sys.stdout.flush()
                os.system('echo "SCAN!!!!"|mail -s "warning-SCAN" ' + mail)
        elif (scantype == "scan-warn"):  # 禁止，报警，需要区分方向、源/目的ip
            if (scandir == "scan-in"):  # 禁止本虚拟机作为scan的目的地址,源地址是scansip
                time.sleep(30)
                query = "select distinct dst_port from protocol where name='" + project_id + "' and id>" + str(idmax1) + "  and dst_ip='" + scandip + "'" + " and src_ip='" +scansip + "' and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)

                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                if len(result) > 50:
                    query = "update protocol set state='scan-warn' where id=" + str(result[0][0])
                    print query
                    cursort.execute(query)
                    db_test.commit()

                    state = "scan-warn"
                    strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                        result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                               2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                           result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                               7] + '","dst_mac":"' + \
                           result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                           result[0][
                               11] + '","state":"' + state + '"}\''
                    print strr
                    os.system(strr)

                    cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                    db_ins.commit()
                    mail = str(cursori.fetchone())[3:-3]
                    cursori.execute(
                        "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                        "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                        result[0][
                            1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                        + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                        result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                    print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                          result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                          result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                          result[0][10] + "','" + result[0][11] + "')"
                    db_ins.commit()
                    #sys.stdout.flush()
                    os.system('echo "SCAN!!!!"|mail -s "warning-SCAN" ' + mail)
            elif (scandir == "scan-out"):  # 禁止本虚拟机作为scan的源地址,目的地址是scandip
                time.sleep(30)
                query = "select distinct dst_port from protocol where name='" + project_id + "' and id>" + str(idmax1) + "  and dst_ip='" + scandip + "'" + " and src_ip='" + scansip + "' and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)

                #sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                if len(result) > 50:
                    query = "update protocol set state='scan-warn' where id=" + str(result[0][0])
                    print query
                    cursort.execute(query)
                    db_test.commit()

                    state = "scan-warn"
                    strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                        result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                               2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                           result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                               7] + '","dst_mac":"' + \
                           result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                           result[0][
                               11] + '","state":"' + state + '"}\''
                    print strr
                    os.system(strr)

                    cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                    db_ins.commit()
                    mail = str(cursori.fetchone())[3:-3]
                    cursori.execute(
                        "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                        "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                        result[0][
                            1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                        + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                        result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                    print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                          result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                          result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                          result[0][10] + "','" + result[0][11] + "')"
                    db_ins.commit()
                    #sys.stdout.flush()
                    os.system('echo "SCAN!!!!"|mail -s "warning-SCAN" ' + mail)
elif incidenttype=="incident-dos":
    dostype=sys.argv[5]
    startt = sys.argv[6]
    endt = sys.argv[7]
    if(dostype=='icmp' or dostype=='smurf' or dostype=='udp' or dostype=='fraggle' ):
        if dostype=='icmp' or dostype=='smurf':proto = "ICMP"
        else:proto = "UDP"
        lianxu = 0
        time1 = time.time()
        while True:
            cursort.execute("select count(*) from protocol")
            db_test.commit()
            idmax0 = cursort.fetchone()
            idmax1 = int(str(idmax0)[1:-3])
            query = "select * from protocol where proto='" + proto + "' and name='" + project_id + "' and id>" + str(idmax1) + "  and (src_ip='" + ip + "'" + " or dst_ip='" + ip + "') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)

            #sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            if len(result) != 0:
                time2 = time.time()
                print time2 - time1
                if time2 - time1 < 0.0001:
                    if lianxu >= 0 and lianxu < 100000:
                        lianxu = lianxu + 1
                    else:
                        lianxu = 0
                time1 = time2
                if lianxu >= 100000:
                    query = "update protocol set state='dos-"+dostype+"-warn' where id=" + str(result[0][0])
                    print query
                    cursort.execute(query)
                    db_test.commit()

                    state = "dos-"+dostype+"-warn"
                    strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                        result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                               2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                           result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                               7] + '","dst_mac":"' + \
                           result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                           result[0][
                               11] + '","state":"' + state + '"}\''
                    print strr
                    os.system(strr)

                    cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                    db_ins.commit()
                    mail = str(cursori.fetchone())[3:-3]
                    cursori.execute(
                        "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                        "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                        result[0][
                            1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                        + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                        result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                    print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                          result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                          result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                          result[0][10] + "','" + result[0][11] + "')"
                    db_ins.commit()
                    #sys.stdout.flush()
                    os.system('echo "flooding!!!!"|mail -s "warning-flooding" ' + mail)

    elif dostype=='syn' or dostype=='land':
        lianxu=0
        time1=time.time()
        while True:
            cursort.execute("select count(*) from protocol")
            db_test.commit()
            idmax0 = cursort.fetchone()
            idmax1 = int(str(idmax0)[1:-3])
            query = "select * from protocol where (info like 'SYN%' or info like 'SYN') and name='" + project_id + "' and id>" + str(idmax1)+"  and (src_ip='"+ip+"'"+" or dst_ip='"+ip+"') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)
            #sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            if len(result)!=0:
                time2=time.time()
                print time2-time1
                if time2-time1<0.0001:
                    if lianxu>=0 and lianxu<100000:
                        lianxu=lianxu+1
                    else:lianxu=0
                time1=time2
                if lianxu>=100000:
                    query = "update protocol set state='dos-" + dostype + "-warn' where id=" + str(result[0][0])
                    print query
                    cursort.execute(query)
                    db_test.commit()

                    state = "dos-" + dostype + "-warn"
                    strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                        result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                               2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                           result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                               7] + '","dst_mac":"' + \
                           result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                           result[0][
                               11] + '","state":"' + state + '"}\''
                    print strr
                    os.system(strr)

                    cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                    db_ins.commit()
                    mail = str(cursori.fetchone())[3:-3]
                    cursori.execute(
                        "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                        "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                        result[0][
                            1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                        + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                        result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                    print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                          result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                          result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                          result[0][10] + "','" + result[0][11] + "')"
                    db_ins.commit()
                    #sys.stdout.flush()
                    os.system('echo "flooding!!!!"|mail -s "warning-flooding" ' + mail)
elif incidenttype=="incident-ftp":
    ftpsip = sys.argv[5]
    ftpdip = sys.argv[6]
    ftpport = sys.argv[7]
    ftpdir = sys.argv[8]
    ftptype = sys.argv[9]
    ftptypee = sys.argv[10]
    startt = sys.argv[11]
    endt = sys.argv[12]
    while True:
        cursort.execute("select count(*) from protocol")
        db_test.commit()
        idmax0 = cursort.fetchone()
        idmax1 = int(str(idmax0)[1:-3])
        if (ftptype == "ftp-happen"):  # 发生即记录，不论方向
            query = "select * from protocol where type='FTP' and info like '%" + ftptypee + "%' and name='" + project_id + "' and id>" + str(
                idmax1) + " and (src_ip='" + ip + "'" + " or dst_ip='" + ip + "') and (src_port='" + ftpport + "'" + " or dst_port='" + ftpport + "') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)
            print query
            # sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            while len(result) == 0:
                time.sleep(0.00001)
                cursort.execute(query)
                db_test.commit()
                result = cursort.fetchall()

            query = "update protocol set state='ftp-record' where id=" + str(result[0][0])
            print query
            cursort.execute(query)
            db_test.commit()

            state ="ftp-record"
            strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                       2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                   result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                       7] + '","dst_mac":"' + \
                   result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                   result[0][
                       11] + '","state":"' + state + '"}\''
            print strr
            os.system(strr)

            cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
            db_ins.commit()
            mail = str(cursori.fetchone())[3:-3]
            cursori.execute(
                "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                result[0][
                    1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
            print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                  result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                  result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                  result[0][10] + "','" + result[0][11] + "')"
            db_ins.commit()
            # sys.stdout.flush()
            os.system('echo "FTP!!!!"|mail -s "warning-FTP" ' + mail)
        elif (ftptype == "ftp-warn"):  # 禁止，报警，需要区分方向、源/目的ip
            if (ftpdir == "ftp-in"):  # 禁止本虚拟机作为ssh的目的地址,源地址是sshsip
                query = "select * from protocol where type='FTP' and info like '%" + ftptypee + "%' and name='" + project_id + "' and id>" + str(
                    idmax1) + "  and dst_ip='" + ip + "'" + " and src_ip='" + ftpsip + "' and (src_port='" + ftpport + "'" + " or dst_port='" + ftpport + "') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                print query
                # sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='ftp-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "ftp-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                # sys.stdout.flush()
                os.system('echo "FTP!!!!"|mail -s "warning-FTP" ' + mail)
            elif (ftpdir == "ftp-out"):
                query = "select * from protocol where type='FTP' and info like '%" + ftptypee + "%' and name='" + project_id + "' and id>" + str(
                    idmax1) + "  and dst_ip='" + ftpdip + "'" + " and src_ip='" + ip + "' and (src_port='" + ftpport + "'" + " or dst_port='" + ftpport + "') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                print query
                # sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='ftp-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "ftp-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                # sys.stdout.flush()
                os.system('echo "FTP!!!!"|mail -s "warning-FTP" ' + mail)
elif incidenttype=="incident-http":
    httpsip = sys.argv[5]
    httpdip = sys.argv[6]
    httpport = sys.argv[7]
    httpdir = sys.argv[8]
    httptype = sys.argv[9]
    httptypee = sys.argv[10]
    startt = sys.argv[11]
    endt = sys.argv[12]
    while True:
        cursort.execute("select count(*) from protocol")
        db_test.commit()
        idmax0 = cursort.fetchone()
        idmax1 = int(str(idmax0)[1:-3])
        if (httptype == "http-happen"):  # 发生即记录，不论方向
            query = "select * from protocol where type='HTTP' and info like '%" + httptypee + "%' and name='" + project_id + "' and id>" + str(
                idmax1) + " and (src_ip='" + ip + "'" + " or dst_ip='" + ip + "') and (src_port='" + httpport + "'" + " or dst_port='" + httpport + "') and ("
            for i in range(int(startt), int(endt)):
                if i < 10:
                    query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                else:
                    query += "timestamp like '____/__/__/" + str(i) + "%' or "
            if int(endt) < 10:
                query += "timestamp like '____/__/__/0" + endt + "%' )"
            else:
                query += "timestamp like '____/__/__/" + endt + "%' )"
            cursort.execute(query)
            print query
            # sys.stdout.flush()
            db_test.commit()
            result = cursort.fetchall()
            while len(result) == 0:
                time.sleep(0.00001)
                cursort.execute(query)
                db_test.commit()
                result = cursort.fetchall()

            query = "update protocol set state='http-record' where id=" + str(result[0][0])
            print query
            cursort.execute(query)
            db_test.commit()

            state = "http-record"
            strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                       2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                   result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                       7] + '","dst_mac":"' + \
                   result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                   result[0][
                       11] + '","state":"' + state + '"}\''
            print strr
            os.system(strr)

            cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
            db_ins.commit()
            mail = str(cursori.fetchone())[3:-3]
            cursori.execute(
                "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                result[0][
                    1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
            print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                  result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                  result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                  result[0][10] + "','" + result[0][11] + "')"
            db_ins.commit()
            # sys.stdout.flush()
            os.system('echo "HTTP!!!!"|mail -s "warning-HTTP" ' + mail)
        elif (httptype == "http-warn"):  # 禁止，报警，需要区分方向、源/目的ip
            if (httpdir == "http-in"):  # 禁止本虚拟机作为ssh的目的地址,源地址是sshsip
                query = "select * from protocol where type='HTTP' and info like '%" + httptypee + "%' and name='" + project_id + "' and id>" + str(
                    idmax1) + "  and dst_ip='" + ip + "'" + " and src_ip='" + httpsip + "' and (src_port='" + httpport + "'" + " or dst_port='" + httpport + "') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                print query
                # sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='http-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "http-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" +
                    result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" + ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                # sys.stdout.flush()
                os.system('echo "HTTP!!!!"|mail -s "warning-HTTP" ' + mail)
            elif (httpdir == "http-out"):
                query = "select * from protocol where type='HTTP' and info like '%" + httptypee + "%' and name='" + project_id + "' and id>" + str(
                    idmax1) + "  and dst_ip='" + httpdip + "'" + " and src_ip='" + ip + "' and (src_port='" + httpport + "'" + " or dst_port='" + httpport + "') and ("
                for i in range(int(startt), int(endt)):
                    if i < 10:
                        query += "timestamp like '____/__/__/0" + str(i) + "%' or "
                    else:
                        query += "timestamp like '____/__/__/" + str(i) + "%' or "
                if int(endt) < 10:
                    query += "timestamp like '____/__/__/0" + endt + "%' )"
                else:
                    query += "timestamp like '____/__/__/" + endt + "%' )"
                cursort.execute(query)
                print query
                # sys.stdout.flush()
                db_test.commit()
                result = cursort.fetchall()
                while len(result) == 0:
                    time.sleep(0.00001)
                    cursort.execute(query)
                    db_test.commit()
                    result = cursort.fetchall()

                query = "update protocol set state='http-warn' where id=" + str(result[0][0])
                print query
                cursort.execute(query)
                db_test.commit()

                state = "http-warn"
                strr = 'curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/' + str(
                    result[0][0]) + '?pretty\' -d\' {"timestamp":"' + result[0][1] + '","protocol":"' + result[0][
                           2] + '","src_ip":"' + result[0][3] + '","src_port":"' + result[0][4] + '","dst_ip":"' + \
                       result[0][5] + '","dst_port":"' + result[0][6] + '","src_mac":"' + result[0][
                           7] + '","dst_mac":"' + \
                       result[0][8] + '","UID":"' + result[0][9] + '","typee":"' + result[0][10] + '","info":"' + \
                       result[0][
                           11] + '","state":"' + state + '"}\''
                print strr
                os.system(strr)

                cursori.execute("select mail from ins_user where project_id='" + project_id + "'")
                db_ins.commit()
                mail = str(cursori.fetchone())[3:-3]
                cursori.execute(
                    "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) "
                    "values ('" +ruleid + "','" +  project_id + "','" + project_name + "','" + ruleobject + "','" + result[0][
                        1] + "','" + result[0][2] + "','" + result[0][3] + "','"
                    + result[0][4] + "','" + result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" +
                    result[0][8] + "','" + result[0][10] + "','" + result[0][11] + "')")
                print "insert into past (ruleid,project_id,project_name,display_name,timestamp,proto,src_ip,src_port,src_mac,dst_ip,dst_port,dst_mac,type,info) values ('" +ruleid + "','" + project_id + "','" + project_name + "','" + ruleobject + "','" + \
                      result[0][1] + "','" + result[0][2] + "','" + result[0][3] + "','" + result[0][4] + "','" + \
                      result[0][7] + "','" + result[0][5] + "','" + result[0][6] + "','" + result[0][8] + "','" + \
                      result[0][10] + "','" + result[0][11] + "')"
                db_ins.commit()
                # sys.stdout.flush()
                os.system('echo "HTTP!!!!"|mail -s "warning-HTTP" ' + mail)
db_test.close()
db_ins.close()


