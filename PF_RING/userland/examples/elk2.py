import os
import MySQLdb
db_hyper=MySQLdb.connect(host='10.10.87.22',user='root',db='test',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor_hyper=db_hyper.cursor()
cursor_hyper.execute("select * from general")
data=cursor_hyper.fetchall()
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
	print "%s %s %s %s %s %s %s %s %s" % (idnum,timestamp,protocol,src_ip,src_port,dst_ip,dst_port,src_mac,dst_mac)
	strr='curl -XPOST \'10.10.87.21:9200/general2/external/'+str(idnum)+'?pretty\' -d\' {"timestamp":"'+timestamp+'","protocol":"'+protocol+'","src_ip":"'+src_ip+'","src_port":"'+src_port+'","dst_ip":"'+dst_ip+'","dst_port":"'+dst_port+'","src_mac":"'+src_mac+'","dst_mac":"'+dst_mac+'","UID":"'+UID+'"}\''
	print strr
	#os.system(strr)
