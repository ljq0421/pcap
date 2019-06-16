import MySQLdb
import time
import os
import sys
ch3 = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])

db_nova=MySQLdb.connect(host='10.10.87.250',user='nova',db='nova',passwd='pdy8QjiuwFdThBuZViRSZM5qOADgmdCobn7XqMQr',port=3306,charset='utf8')
db_keystone=MySQLdb.connect(host='10.10.87.250',user='keystone',db='keystone',passwd='igNaYNsjirbVTElgiGUI5iTYf15rbcN1h4olqgXJ',port=3306,charset='utf8')
db_ins=MySQLdb.connect(host='10.10.87.22',user='root',db='ins_user',passwd='MyNewPass@123',port=3306,charset='utf8')
cursor1=db_nova.cursor()
cursor2=db_keystone.cursor()
cursor3=db_ins.cursor()
cursor1.execute("select display_name,uuid,user_id from instances where vm_state='active'")
cds1=cursor1.fetchall()
cursor3.execute('truncate table ins_user')
db_ins.commit()
display_name=[]
uuid=[]
user_id=[]
ip1=[]
ip2=[]
dev=[]
mail=[]
for i in range(len(cds1)):
	ddisplay_name=cds1[i][0]
	uuidd=cds1[i][1]
	user_idd=cds1[i][2]
	display_name.append(str(ddisplay_name))
	uuid.append(str(uuidd))
	user_id.append(str(user_idd))
	cursor1.execute('select substring_index(substring_index(network_info,\'"\',40),\'"\',-1) from instance_info_caches where instance_uuid="'+uuidd+'"')
	ip11=cursor1.fetchall()
	if len(str(ip11))>15:
		#ip1.append(str(ip11)[3:-5])
		ip1.append(str(ch3(str(ip11)[3:-5])))
		#print(ch3(str(ip11)[3:-5]))
	else:ip1.append(' ');
	cursor1.execute('select substring_index(substring_index(network_info,\'"\',44),\'"\',-1) from instance_info_caches where instance_uuid="'+uuidd+'"')
	ip22=cursor1.fetchall()
	if len(str(ip22))>15:
		#ip2.append(str(ip22)[3:-5])
		ip2.append(str(ch3(str(ip22)[3:-5])))
		#print(ch3(str(ip22)[3:-5]))
	else:ip2.append(' ')
	cursor3.execute('select substring_index(substring_index(network_info,\'devname": "\',-1),\'"\',1) from ins_use_3 where instance_uuid="'+uuidd+'"')
	devs=cursor3.fetchall()
	dev.append(str(devs)[3:-5])	
	cursor2.execute('select substring_index(substring_index(extra,\'"\',4),\'"\',-1) from user where id="'+user_idd+'"')
	maill=cursor2.fetchall()
	if len(str(maill))>8:mail.append(str(maill)[3:-5])
	else:mail.append(' ')
#print ip1
#print ip2
#print uuid
#print user_id             
#print mail
for i in range(len(cds1)):
	cursor3.execute('insert into ins_user (display_name,user_id,uuid,float_ip,ip,mail,tap) values("'+display_name[i]+'","'+user_id[i]+'","'+uuid[i]+'","'+ip1[i]+'","'+ip2[i]+'","'+mail[i]+'","'+dev[i]+'")')
	#cursor3.execute('insert into ins_user (user_id,uuid,float_ip,ip,mail) values('123','123','123','123')
	db_ins.commit()  
warn=sys.argv[1]
#ips=sys.argv[2]
#ipd=sys.argv[3]
#print('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
#cursor3.execute('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
#maill=cursor3.fetchall()
#print str(maill[0])[3:-3]
if warn=='1':#ssh
	ips=sys.argv[2]
	ipd=sys.argv[3]
	print('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	cursor3.execute('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	maill=cursor3.fetchall()
	print str(maill[0])[3:-3]
	os.system('echo "ssh!!!!"|mail -s "warning-ssh" '+str(maill[0])[3:-3])
	print('echo "ssh!!!!"|mail -s "warning" '+str(maill[0])[3:-3])
elif warn=='2':#ftp
	ips=sys.argv[2]
	ipd=sys.argv[3]
	print('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	cursor3.execute('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	maill=cursor3.fetchall()
	print str(maill[0])[3:-3]
	info=sys.argv[4]
	os.system('echo "ftp!!!!'+info+'"|mail -s "warning-ftp" '+str(maill[0])[3:-3])
	print('echo "ftp!!!!'+info+'"|mail -s "warning-ftp" '+str(maill[0])[3:-3])
elif warn=='3':#http
	ips=sys.argv[2]
	ipd=sys.argv[3]
	print('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	cursor3.execute('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
	maill=cursor3.fetchall()
	print str(maill[0])[3:-3]
	info=sys.argv[4]
	cursor3.execute('select * from errurls where url="'+info+'"')
	exist=cursor3.fetchall()
	print exist
	if len(exist)>0:
		os.system('echo "http!!!!'+info+'"|mail -s "warning-http" '+str(maill[0])[3:-3])
		print('echo "http!!!!'+info+'"|mail -s "warning-http" '+str(maill[0])[3:-3])
elif warn=='4':#listen
	info=sys.argv[2]#tap
	cursor3.execute('select mail from ins_user where tap="'+info+'"')
	maill=cursor3.fetchall()
	print str(maill[0])[3:-3]
	os.system('echo "Excessive traffic!!!!"|mail -s "warning-flow" '+str(maill[0])[3:-3])
        print('echo "Excessive traffic!!!!"|mail -s "warning-flow" '+str(maill[0])[3:-3])
elif warn=='5':#icmp flooding
	ips=sys.argv[2]
	ipd=sys.argv[3]
	print('select mail from ins_user where ip="'+ips+'" or ip="'+ipd+'" or float_ip="'+ips+'" or float_ip="'+ipd+'"')
        cursor3.execute('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        maill=cursor3.fetchall()
        print str(maill[0])[3:-3]
        os.system('echo "icmp flooding!!!!"|mail -s "warning-icmp_flooding" '+str(maill[0])[3:-3])
        print('echo "icmp flooding!!!!"|mail -s "warning-icmp_flooding" '+str(maill[0])[3:-3])
elif warn=='6':#udp flooding
	ips=sys.argv[2]
        ipd=sys.argv[3]
        print('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        cursor3.execute('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        maill=cursor3.fetchall()
        print str(maill[0])[3:-3]
        os.system('echo "udp flooding!!!!"|mail -s "warning-udp_flooding" '+str(maill[0])[3:-3])
        print('echo "udp flooding!!!!"|mail -s "warning-udp_flooding" '+str(maill[0])[3:-3])
elif warn=='7':#syn flooding
        ips=sys.argv[2]
        ipd=sys.argv[3]
        print('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        cursor3.execute('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        maill=cursor3.fetchall()
        print str(maill[0])[3:-3]
        os.system('echo "syn flooding!!!!"|mail -s "warning-syn_flooding" '+str(maill[0])[3:-3])
        print('echo "syn flooding!!!!"|mail -s "warning-syn_flooding" '+str(maill[0])[3:-3])
elif warn=='8':#land
        ips=sys.argv[2]
        ipd=sys.argv[3]
        print('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        cursor3.execute('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        maill=cursor3.fetchall()
        print str(maill[0])[3:-3]
        os.system('echo "land!!!!"|mail -s "warning-land" '+str(maill[0])[3:-3])
        print('echo "land!!!!"|mail -s "warning-land" '+str(maill[0])[3:-3])
elif warn=='9':#nmap
        ipd=sys.argv[2]
        print('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        cursor3.execute('select mail from ins_user where ip="'+ipd+'" or float_ip="'+ipd+'"')
        maill=cursor3.fetchall()
        print str(maill[0])[3:-3]
        os.system('echo "scanning!!!!"|mail -s "warning-scanning" '+str(maill[0])[3:-3])
        print('echo "scanning!!!!"|mail -s "warning-scanning" '+str(maill[0])[3:-3])


db_nova.close()
db_keystone.close()
db_ins.close()

