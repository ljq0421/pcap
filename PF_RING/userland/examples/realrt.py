import os
fp=open('/proc/net/dev','r')
for i in range(6):
    content=fp.readline()
#print(content)
num=0
rp=0
tp=0
f1=0
f2=0
for i in range(len(content)-1):
    if content[i]==' ' and content[i+1]!=' ':
        num+=1
        #print(content[i+1])
    if num==3 and f1==0:
        next=content[i+1:-1].find(' ')
        #print('%c next1=%d\n' % (content[i+1],next))
        rp_str=content[i+1:i+1+next]
        rp=int(rp_str)
        f1=1
 #       print(rp_str)
    if num==11 and f2==0:
        next = content[i + 1:-1].find(' ')
        tp_str = content[i + 1:i+1+next]
        f2=1
        tp=int(tp_str)
  #      print(tp_str)
print(rp+tp)
fp.close()
