import time
import MySQLdb
import sys
db_test=MySQLdb.connect(host='10.10.87.22',user='root',db='test',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor=db_test.cursor()
UID=sys.argv[1]
type0=sys.argv[2]
ip=sys.argv[3]
cursor.execute("select count(*) from protocol")
db_test.commit()
idmax0=cursor.fetchone()
idmax1=int(str(idmax0)[1:-3])
query="select * from protocol where type='"+type0+"' and name='"+UID+"' and id>"+str(idmax1)+" and (src_ip='"+ip+"' or dst_ip='"+ip+"')"
print query
cursor.execute(query)
db_test.commit()
result=cursor.fetchall()

while True:
	while len(result)==0:
		time.sleep(0.00001)
		cursor.execute(query)
		db_test.commit()
		result=cursor.fetchall()
	print "id:        "+str(result[0][0])
	#print "timestamp: "+result[0][1]
	#print "proto:     "+result[0][2]
	#print "src_ip:    "+result[0][3]
	#print "src_port:  "+result[0][4]
	#print "dst_ip:    "+result[0][5]
	#print "dst_port:  "+result[0][6]
	#print "src_mac:   "+result[0][7]
	#print "dst_mac:   "+result[0][8]
	#print "name:      "+result[0][9]
	#print "type:      "+result[0][10]
	#print "info:      "+result[0][11]
	cursor.execute("select count(*) from protocol")
	db_test.commit()
	idmax0=cursor.fetchone()
	idmax1=int(str(idmax0)[1:-3])
	query="select * from protocol where type='"+type0+"' and name='"+UID+"' and id>"+str(idmax1)+" and (src_ip='"+ip+"' or dst_ip='"+ip+"')"
	print query
	cursor.execute(query)
	db_test.commit()
	result=cursor.fetchall()

db_test.close()
