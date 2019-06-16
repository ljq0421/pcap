import binascii
import subprocess
import time
import os
import MySQLdb
import sys
ch3 = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
db_hyper=MySQLdb.connect(host='10.10.87.24',user='root',db='ca_center',passwd='123',port=3306,charset='utf8')
cursor_hyper=db_hyper.cursor()
dev=sys.argv[1]
flag=1
fp=open(dev+'out.txt','w')
while True:
	while os.path.getsize(str(flag)+'-'+dev+'.txt')==0:time.sleep(0.001)
	p=subprocess.Popen('tail -f '+str(flag)+'-'+dev+'.txt -n +2',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
	line=p.stdout.readline()
	print line
	ssh_pre=''
	ftp_pre=''
	numg=1
	nump=1
	inform=[('0.0.0.0','0','0.0.0.0','0','0','0')]
	num_inform=0
	num_icmp=0
	num_udp=0
	num_syn=0
	num_nmap=0
	while True:
		if line=="/********************************************************/\n":
			line1=p.stdout.readline()
			ls=line1.split(" ")
			print ls
			fp.write(str(ls))
			LINE=''
			info=''
			type=''
			line=p.stdout.readline()
			while line!="/********************************************************/\n" and line!="end here":
				LINE+=line
				line=p.stdout.readline()
			#print binascii.hexlify(LINE)
			try:
			  if ls[5]=='ICMP':
				#print binascii.hexlify(LINE[34])
				if binascii.hexlify(LINE[34])=='00':
					#print 'reply'
					inform.append((ls[1],ls[2],ls[3],ls[4],'ICMP reply',ls[0][16:-1]))
				elif binascii.hexlify(LINE[34])=='08':
					#print 'request'
					inform.append((ls[1],ls[2],ls[3],ls[4],'ICMP request',ls[0][16:-1]))
				num_inform+=1
				#print '%.9f' % float(inform[num_inform][5])
				#print '%.9f' % float(inform[num_inform-1][5])
				#print '%.9f' % (float(inform[num_inform][5])-float(inform[num_inform-1][5]))
				if float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.001 and inform[num_inform][0]==inform[num_inform-1][0] and inform[num_inform][2]==inform[num_inform-1][2] or inform[num_inform][2]==inform[num_inform-1][0] and inform[num_inform][0]==inform[num_inform-1][2]:
					num_icmp+=1
				elif num_icmp>1000 and float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.1 :num_icmp+=1
				else:num_icmp=0
				if num_icmp>10000 and binascii.hexlify(LINE[34])=='08':
					#print "python mysqlq.py 5 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))
					fp.write("python mysqlq.py 5 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					os.system("python mysqlq.py 5 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					num_icmp=0
			  elif ls[5]=='UDP':
				inform.append((ls[1],ls[2],ls[3],ls[4],'UDP',ls[0][16:-1]))
				num_inform+=1
				if float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.001 and inform[num_inform][0]==inform[num_inform-1][0] and inform[num_inform][2]==inform[num_inform-1][2] or inform[num_inform][2]==inform[num_inform-1][0] and inform[num_inform][0]==inform[num_inform-1][2]:
					num_udp+=1
				elif num_udp>1000 and float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.1:
					num_udp+=1
				else:num_udp=0
				if num_udp>10000:
					print "python mysqlq.py 6 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))
					fp.write("python mysqlq.py 6 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					os.system("python mysqlq.py 6 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					num_udp=0
			  elif ls[5]=='TCP':
				inform.append((ls[1],ls[2],ls[3],ls[4],'TCP',ls[0][16:-1]))
				num_inform+=1
				#print binascii.hexlify(LINE[46])+" "+binascii.hexlify(LINE[47])+" "+binascii.hexlify(LINE[48])
				if binascii.hexlify(LINE[47])=='02' and float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.001 and inform[num_inform][0]==inform[num_inform-1][0] and inform[num_inform][2]==inform[num_inform-1][2] or inform[num_inform][2]==inform[num_inform-1][0] and inform[num_inform][0]==inform[num_inform-1][2]:
					num_syn+=1
				elif num_syn>1000 and float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.1 :num_syn+=1
				else:num_syn=0
				if num_syn>10000 and ls[1]!=ls[3]:
					print "python mysqlq.py 7 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))
					fp.write("python mysqlq.py 7 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					os.system("python mysqlq.py 7 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					num_syn=0
				elif num_syn>10000 and ls[1]==ls[3]:
					#print "python mysqlq.py 8 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))
					fp.write("python mysqlq.py 8 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					os.system("python mysqlq.py 8 "+str(ch3(ls[1]))+" "+str(ch3(ls[3])))
					num_syn=0
				if float(inform[num_inform][5])-float(inform[num_inform-1][5])<0.001 and inform[num_inform][0]==inform[num_inform-1][0] and inform[num_inform][2]==inform[num_inform-1][2] or inform[num_inform][2]==inform[num_inform-1][0] and inform[num_inform][0]==inform[num_inform-1][2] and inform[num_inform][1]==inform[num_inform-1][3] and inform[num_inform][3]!=inform[num_inform-1][1]:
					num_nmap+=1
					if num_nmap>1000:
						#print "python mysqlq.py 9 "+str(ch3(ls[3]))
						fp.write("python mysqlq.py 9 "+str(ch3(ls[3])))
						os.system("python mysqlq.py 9 "+str(ch3(ls[3])))
						num_nmap=0
				else:num_nmap=0
				if float(inform[num_inform][5])-float(inform[num_inform-1][5]<0.001 and inform[num_inform][0]==inform[num_inform-1][0] and inform[num_inform][2]==inform[num_inform-1][2] or inform[num_inform][2]==inform[num_inform-1][0] and inform[num_inform][0]==inform[num_inform-1][2] and inform[num_inform][1]!=inform[num_inform-1][3] and inform[num_inform][3]==inform[num_inform-1][1]):
					num_nmap+=1
					if num_nmap>1000:
						#print "python mysqlq.py 9 "+str(ch3(ls[1]))
						fp.write("python mysqlq.py 9 "+str(ch3(ls[1])))
						os.system("python mysqlq.py 9 "+str(ch3(ls[1])))
						num_nmap=0
					else:num_nmap=0
			except:continue
			try:

			  if ls[2]=='80' or ls[4]=='80' or ls[2]=='443' or ls[4]=='443':#http
				if LINE.count('Host')!=0:
					info=LINE[LINE.find('Host: ')+6:LINE.find('Connection:')]
					info=info.split('\r\n')[0]
					#print '3',info
					fp.write('3'+info)
					type='HTTP'
					#print "python mysqlq.py 3 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info
					fp.write("python mysqlq.py 3 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info)
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
				#print 'LINE:',LINE
				info=LINE[66:-1]
				type='FTP'
				ftp_num=LINE[42:46]
				#print '4',info
				info=info.split('\r\n')[0]
				#print '5',info
				if (info[0:4]=='DELE' or info[0:3]=='RMD') and ftp_pre!=ftp_num:
					#print "python mysqlq.py 2 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info
					fp.write("python mysqlq.py 2 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info)
					os.system("python mysqlq.py 2 "+str(ch3(ls[1]))+" "+str(ch3(ls[3]))+" "+info)
				ftp_pre=ftp_num
			  if ls[1].count(".")==3:
				strr='curl -XPOST \'10.10.87.21:9200/general/external/'+str(int(time.time()*1000000))+'?pretty\' -d\' {"timestamp":"'+ls[0]+'","protocol":"'+ls[5]+'","src_ip":"'+ls[1]+'","src_port":"'+ls[2]+'","dst_ip":"'+ls[3]+'","dst_port":"'+ls[4]+'"}\''
				#print strr
				fp.write(strr)
				os.system(strr)
				numg+=1
				#print "insert into general(timestamp,protocol,src_ip,src_port,dst_ip,dst_port)values("+ls[0]+","+ls[5]+","+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+")"
				#cursor_hyper.execute("insert into general(timestamp,protocol,src_ip,src_port,dst_ip,dst_port)values("+ls[0]+",'"+ls[5]+"',"+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+")")
				#db_hyper.commit()
			  if len(info)!=0:
				strr='curl -XPOST \'10.10.87.21:9200/protocol/external/'+str(int(time.time()*1000000))+'?pretty\' -d\' {"timestamp":"'+ls[0]+'","proto":"'+ls[5]+'","type":"'+type+'","src_ip":"'+ls[1]+'","src_port":"'+ls[2]+'","dst_ip":"'+ls[3]+'","dst_port":"'+ls[4]+'","info":"'+info+'"}\''
				#print strr
				fp.write(strr)
				os.system(strr)
				nump+=1
				#cursor_hyper.execute("insert into protocol(timestamp,type,proto,src_ip,src_port,dst_ip,dst_port,info)values("+ls[0]+",'"+type+"','"+ls[5]+"',"+str(ch3(ls[1]))+","+ls[2]+","+str(ch3(ls[3]))+","+ls[4]+",'"+info+"')")
				#db_hyper.commit()
			except:continue

			if line=="end here":
				if flag==1:
					flag=2
					os.system("truncate -s 0 1-"+dev+".txt")
				else:
					flag=1
					os.system("truncate -s 0 2-"+dev+".txt")
