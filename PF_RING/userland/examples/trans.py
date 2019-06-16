import subprocess
import time
import os
import MySQLdb
ch3 = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
db_hyper=MySQLdb.connect(host='10.10.87.24',user='root',db='ca_center',passwd='123',port=3306,charset='utf8')
cursor_hyper=db_hyper.cursor()

p=subprocess.Popen('tail -f packets.txt -n +2',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
line=p.stdout.readline()
print line
ssh_pre=''
ftp_pre=''
while True:
	if line=="/********************************************************/\n":
		line1=p.stdout.readline()
		ls=line1.split(" ")
		print ls
		LINE=''
		info=''
		type=''
		line=p.stdout.readline()
		while line!="/********************************************************/\n":
			LINE+=line
			line=p.stdout.readline()
		try:
		  if ls[2]=='80' or ls[4]=='80' or ls[2]=='443' or ls[4]=='443':#http
			if LINE.count('Host')!=0:
				info=LINE[LINE.find('Host: ')+6:LINE.find('Connection:')]
				type='HTTP'
				print "python mysqlq.py 3 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info
				os.system("python mysqlq.py 3 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info)
		  elif ls[2]=='22' or ls[4]=='22':
			info=' '
			type='SSH'
			ssh_num=LINE[42:46]
			if str(ord(LINE[51]))=='2' and ssh_pre!=ssh_num:
				os.system("python mysqlq.py 1 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
			ssh_pre=ssh_num
		  elif ls[2]=='161' or ls[4]=='161':
			info=' '
			type='SNMP'
		  elif ls[2]=='20' or ls[4]=='21' or ls[2]=='20' or ls[4]=='21':
			info=LINE[70:-1]
			type='FTP'
			ftp_num=LINE[42:46]
			if (info[0:4]=='DELE' or info[0:3]=='RMD') and ftp_pre!=ftp_num:
				print "python mysqlq.py 2 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info
				os.system("python mysqlq.py 2 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info)
			ftp_pre=ftp_num
		  if ls[1].count(".")==3:
			#print "insert into general(timestamp,protocol,src_ip,src_port,dst_ip,dst_port)values("+ls[0]+","+ls[5]+","+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+")"
			cursor_hyper.execute("insert into general(timestamp,protocol,src_ip,src_port,dst_ip,dst_port)values("+ls[0]+",'"+ls[5]+"',"+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+")")
			db_hyper.commit() 	
		  if len(info)!=0:
			cursor_hyper.execute("insert into protocol(timestamp,type,proto,src_ip,src_port,dst_ip,dst_port,info)values("+ls[0]+",'"+type+"','"+ls[5]+"',"+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+",'"+info+"')")
			db_hyper.commit()
		except:continue	
				

			
			

			
		
		

	
		

