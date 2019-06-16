import os
import MySQLdb
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='test',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor_test=db_test.cursor()
cursor_test.execute("select count(*) from protocol")
db_test.commit()
idmax0 = cursor_test.fetchone()
idmax1 = int(str(idmax0)[1:-3])
while True:
	cursor_test.execute("select * from protocol where id>"+str(idmax1))
	db_test.commit()
	data=cursor_test.fetchall()
	for row in data:
		idnum=row[0]
		timestamp=row[1]
		protocol=row[2]
		src_ip=row[3]
		src_port=row[4]
		dst_ip=row[5]
		dst_port=row[6]
		src_mac=row[7]
		dst_mac=row[8]
		UID=row[9]
		typee=row[10]
		info=row[11]
		print info.count("\"")
		if info.count("\"")!=0:
			info=info.replace('"',' ',100)
			print info

		state=row[12]
		print idnum,timestamp,protocol,src_ip,src_port,dst_ip,dst_port,src_mac,dst_mac,UID
		strr='curl -H "Content-Type: application/json" -XPOST \'10.10.87.23:9200/protocol/external/'+str(idnum)+'?pretty\' -d\' {"timestamp":"'+timestamp+'","protocol":"'+protocol+'","src_ip":"'+src_ip+'","src_port":"'+src_port+'","dst_ip":"'+dst_ip+'","dst_port":"'+dst_port+'","src_mac":"'+src_mac+'","dst_mac":"'+dst_mac+'","UID":"'+UID+'","typee":"'+typee+'","info":"'+info+'","state":"'+state+'"}\''
		print strr
		os.system(strr)
	cursor_test.execute("select count(*) from protocol")
	db_test.commit()
	idmax0 = cursor_test.fetchone()
	idmax1 = int(str(idmax0)[1:-3])
db_test.close()
