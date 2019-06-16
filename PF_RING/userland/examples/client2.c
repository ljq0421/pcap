#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/msg.h>
#include<sys/ipc.h>
#include<mysql/mysql.h>

extern char *optarg;

struct mymesg{
	long int mtype;
	char mtext[10240];
};
int main(int argc, char* argv[])
{
	int id = 0;
	struct mymesg pfmsg;

	MYSQL *conn;
	MYSQL_RES *res;
	MYSQL_ROW row;
	char* server="10.10.87.22";
	char* user="root";
	char* password="MyNewPass@123";
	char* database="test";
	conn=mysql_init(NULL);
	if(!mysql_real_connect(conn,server,user,password,database,0,NULL,0)){
		printf("Error connecting to database:%s\n",mysql_error(conn));
	}else{
		printf("Connected...\n");
	}

	char c;
	int QUEUE;

	while((c = getopt(argc,argv,"Q:")) != '?') {
		if((c == 255) || (c == -1)) break;
		switch(c) {
			case 'Q':
				QUEUE=atoi(optarg);
				break;
		}
	}

	key_t key = ftok("/tmp",QUEUE);
	id = msgget(key,0666|IPC_CREAT);
	if(id == -1)
	{
		printf("open msg error \n");
		return 0;
	}
	while(1)
	{
		char dump_str[10240];
		char *name,*element,*tmp,*timestamp,*proto,*type,*src_ip,*src_port,*dst_ip,*dst_port,*info,*src_mac,*dst_mac;
		info="NULL";
		int num=0;
		char query1[10240],query2[10240];
		memset(dump_str,0,10240);

		if(msgrcv(id,(void *)&pfmsg,10240,1,0) < 0)
		{
			printf("receive msg error \n");
			return 0;
		}

		strcpy(dump_str,pfmsg.mtext);
		tmp=dump_str;
		element=strsep(&tmp,"|");
		while(element!=NULL){
			if(num==0){
				name=element;
			}
			else if(num==1){
				timestamp=element;
			}
			else if(num==2){
				src_mac=strsep(&element,">");
				dst_mac=strsep(&element,">");
			}
			else if(num==3){
				if(strcmp(element,"ARP")==0){
					proto="ARP";
					info="";
				}
				else{
					proto="NULL";
					src_port=strsep(&element,">");
					src_ip=strsep(&src_port,"*");
					dst_port=strsep(&element,">");
					dst_ip=strsep(&dst_port,"*");
				}
			}
			else if(num==4 && strcmp(proto,"ARP")==0){
				src_ip=strsep(&element,">");
				dst_ip=strsep(&element,">");
				src_port="NULL";
				dst_port="NULL";
 				break;
			}
			else if(num==4){	
				char infoo[10240]={0};
				int j=0,k=0;
				printf("element:%s\n",element);
				for(j=0;j<strlen(element);j++){
					if(element[j]=='\''){
						infoo[k++]='"';
					}
					else if(element[j]=='\\'){
						infoo[k++]=' ';
					}
					else infoo[k++]=element[j];
				}
				printf("infoo:%s\n",infoo);
				info=infoo;
				break;
			}
			num++;
			element=strsep(&tmp,"|");
		}
		type="NULL";
		if(strcmp(src_port,"22")==0||strcmp(dst_port,"22")==0){
			proto="TCP";
			type="SSH";
		}
		else if(strcmp(src_port,"23")==0||strcmp(dst_port,"23")==0){
			proto="TCP";
			type="Telnet";
		}
		else if(strcmp(src_port,"25")==0||strcmp(dst_port,"25")==0){
			proto="TCP";
			type="SMTP";
		}
		else if(strcmp(src_port,"110")==0||strcmp(dst_port,"110")==0){
			proto="TCP";
			type="POP3";
		}
		else if(strcmp(src_port,"143")==0||strcmp(dst_port,"143")==0){
			proto="TCP";
			type="IMAP";
		}
		else if(strcmp(src_port,"67")==0||strcmp(dst_port,"67")==0||strcmp(src_port,"68")==0||strcmp(dst_port,"68")==0){
			proto="UDP";
			type="DHCP";
		}
		else if(strcmp(src_port,"69")==0||strcmp(dst_port,"69")==0){
			proto="UDP";
			type="TFTP";
		}
		else if(strcmp(src_port,"1812")==0||strcmp(dst_port,"1812")==0){
			proto="UDP";
			type="RADIUS";
		}
		else if(strcmp(src_port,"123")==0||strcmp(dst_port,"123")==0){
			proto="TCP";
			type="NTP";
		}
		else if(strcmp(src_port,"427")==0||strcmp(dst_port,"427")==0){
			proto="TCP";
			type="SLP";
		}
		else if(strcmp(src_port,"80")==0||strcmp(dst_port,"80")==0){
			proto="TCP";
			type="HTTP";
		}
		else if(strcmp(src_port,"53")==0||strcmp(dst_port,"53")==0){
			proto="UDP";
			type="DNS";
		}
		else if(strcmp(src_port,"443")==0||strcmp(dst_port,"443")==0){
			proto="TCP";
			type="HTTPs";
		}
		else if(strcmp(src_port,"161")==0||strcmp(dst_port,"161")==0){
			proto="TCP";
			type="SNMP";
		}
		else if(strcmp(src_port,"179")==0||strcmp(dst_port,"179")==0){
			proto="TCP";
			type="BGP";
		}
		else if(strcmp(src_port,"520")==0||strcmp(dst_port,"520")==0){
			proto="UDP";
			type="RIP";
		}
		else if(strcmp(src_port,"1985")==0||strcmp(dst_port,"1985")==0){
			proto="UDP";
			type="HSRP";
		}
		else if(strcmp(src_port,"20")==0||strcmp(dst_port,"20")==0||strcmp(src_port,"21")==0||strcmp(dst_port,"21")==0){
			proto="TCP";
			type="FTP";
		}
		else if(strcmp(src_port,"3306")==0||strcmp(dst_port,"3306")==0){
			proto="TCP";
			type="mysql";
		}
		else if(strcmp(src_port,"1433")==0||strcmp(dst_port,"1433")==0){
			proto="TCP";
			type="sqlserver";
		}
		else if(strcmp(src_port,"1521")==0||strcmp(dst_port,"1521")==0){
			proto="TCP";
			type="oracle";
		}
		char infoo[10240];
		if(info[0]=='I' && info[1]=='C' && info[2]=='M' && info[3]=='P'){
			proto="ICMP";
			strncpy(infoo,info+5,strlen(info)-4);
		}
		else if(info[0]=='T' && info[1]=='C' && info[2]=='P'){
			proto="TCP";
			strncpy(infoo,info+4,strlen(info)-3);
		}
		else if(info[0]=='U' && info[1]=='D' && info[2]=='P'){
			proto="UDP";
			strncpy(infoo,info+4,strlen(info)-3);
		}
		else if (info[0]=='I' && info[1]=='G' && info[2]=='M' && info[3]=='P'){
			proto="IGMP";
			strncpy(infoo,info+5,strlen(info)-4);
		}
		else if (info[0]=='O' && info[1]=='S' && info[2]=='P' && info[3]=='F'){
			proto="OSPF";
			strncpy(infoo,info+5,strlen(info)-4);
		}
        if(strcmp("ARP",proto)==0) strcpy(infoo,"");
        if(strcmp("NULL",type)==0) strcpy(infoo,"");

		sprintf(query2,"insert into protocol(name,timestamp,proto,src_ip,src_port,dst_ip,dst_port,src_mac,dst_mac,type,info) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')",name,timestamp,proto,src_ip,src_port,dst_ip,dst_port,src_mac,dst_mac,type,infoo);
		printf("query2=%s\n",query2);
		int t2=mysql_query(conn,query2); 
		if(t2)
		{
			printf("Error making query:%s\n",mysql_error(conn));
			break;
		}
		if(strncmp(pfmsg.mtext,"QUIT",4) ==0)
			break;
	}
	return 0;
}


