#define HAVE_PF_RING
#include <stdio.h>
#include <pcap.h>
#include <arpa/inet.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#define BUFSIZE 1514

int NUM=0;
struct ether_header 
{
    unsigned char mac_dhost[6];	//以太网目的地址
    unsigned char mac_shost[6];	//以太网源地址
    unsigned short mac_type;  //以太网数据包类型
};
struct ether_header_IP 	//IP数据包
{
    unsigned char mac_dhost[6];	
    unsigned char mac_shost[6];
    unsigned short mac_type;
    unsigned char ip_head[12];  //版本号-首部校验和的12字节
    unsigned char ip_shost[4];   //源IP
    unsigned char ip_dhost[4];   //目的IP
};
struct ether_header_ARP		 //ARP数据包
{
    unsigned char mac_dhost[6];
    unsigned char mac_shost[6];
    unsigned short mac_type;
    unsigned char arp_head[8];	//arp首部
    unsigned char arp_sha[6];   //源MAC
    unsigned char arp_spa[4];   //源IP
    unsigned char arp_tha[6];   //目的MAC 
    unsigned char arp_tpa[4];   //目的IP
};
/*******************************回调函数************************************/
void ethernet_protocol_callback(unsigned char *argument,const struct pcap_pkthdr *packet_heaher,const unsigned char *packet_content)
{
    NUM++;
    printf("Catch sum=%d\n",NUM);
    unsigned char *mac_string;
    unsigned short mac_t;
    unsigned char *ip_s,*ip_d; 
    struct ether_header *ethernet_protocol;
    ethernet_protocol = (struct ether_header *)packet_content;
    mac_t=ntohs(ethernet_protocol->mac_type);//数据包类型
    if (mac_t==0x0800){		//IP数据包
    	struct ether_header_IP *ethernet_protocol_IP;
    	ethernet_protocol_IP = (struct ether_header_IP *)packet_content;
        printf("----------------------------------------------------\n");
        printf("%s", ctime((time_t *)&(packet_heaher->ts.tv_sec))); //转换时间
        ip_s=(unsigned char *)ethernet_protocol_IP->ip_shost;
        ip_d=(unsigned char *)ethernet_protocol_IP->ip_dhost;
        printf("ip_s:%3d.%3d.%3d.%3d\n",*(ip_s+0),*(ip_s+1),*(ip_s+2),*(ip_s+3));
        printf("ip_d:%3d.%3d.%3d.%3d\n",*(ip_d+0),*(ip_d+1),*(ip_d+2),*(ip_d+3));
    }
    else if(mac_t==0x0806){		//ARP数据包
    	struct ether_header_ARP *ethernet_protocol_ARP;
    	ethernet_protocol_ARP = (struct ether_header_ARP *)packet_content;
        printf("----------------------------------------------------\n");
        printf("%s", ctime((time_t *)&(packet_heaher->ts.tv_sec))); //转换时间
        ip_s=(unsigned char *)ethernet_protocol_ARP->arp_spa;
        ip_d=(unsigned char *)ethernet_protocol_ARP->arp_tpa;
        printf("ip_s:%3d.%3d.%3d.%3d\n",*(ip_s+0),*(ip_s+1),*(ip_s+2),*(ip_s+3));
        printf("ip_d:%3d.%3d.%3d.%3d\n",*(ip_d+0),*(ip_d+1),*(ip_d+2),*(ip_d+3));
    }
    switch(mac_t) 
    {
        case 0x0800:printf("The network layer is IP protocol\n");break;//ip
        case 0x0806:printf("The network layer is ARP protocol\n");break;//arp
        case 0x0835:printf("The network layer is RARP protocol\n");break;//rarp
        default:break;
    }
    usleep(800*1000); 		//挂起0.8s
}

int main(int argc, char *argv[])
{
    char error_content[100];    //出错信息
    pcap_t * pcap_handle;
    unsigned char *mac_string;
    unsigned short ethernet_type;           //以太网类型
    char *net_interface = "ens33";                 //接口名字
    struct pcap_pkthdr protocol_header;
    struct ether_header *ethernet_protocol;
    pcap_handle = pcap_open_live(net_interface,BUFSIZE,1,0,error_content);//打开网络接口
    if(pcap_loop(pcap_handle,-1,ethernet_protocol_callback,NULL) < 0)
    //持续抓包，使用-1
    {
        perror("pcap_loop");	//用来将上一个函数发生错误的原因输出到stderr
    }
    pcap_close(pcap_handle);		//关闭接口
    return 0;
}

