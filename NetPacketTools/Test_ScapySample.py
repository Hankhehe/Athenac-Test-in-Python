from ast import Bytes 
from scapy.all import *
from scapy.utils import *

nic1 = get_working_if()
nic1mac = nic1.mac
micname = nic1.name
nic = get_working_ifaces()
for i in nic:
    print(i.name)
fam,hw = get_if_raw_hwaddr(conf.iface)


pass
# import os
# import time
# from scapy.arch.windows import get_windows_if_list




# Show Protocol args require or option
# print(ls(IP))

#Send DHCPDiscover Packet and Print receive DATA 
# pcapfile = rdpcap('D:/DHCP.pcap')
# result ,nums = sr(pcapfile, retry=2, timeout=3)
# print(result.show())
# for s, r in result:
#    print(r[BOTP].hwsrc)



#get Payload Data From PCAP File and Send build L2 MAC + Payload Data 
# pcapfile = rdpcap('D:/DHCPOffer.pcap')
# print('--------------------------')
# pcapfile[0].show()
# print('---------------------------')
# pcapfile[0].payload
# print('-----------------------------')
# DHCPxid = pcapfile[0][BOOTP].xid
# print('BOOTP xid :',pcapfile[0][BOOTP].xid)
# print('BOOTP your IP:',pcapfile[0][BOOTP].yiaddr)
# print('BOOTP MAC:',pcapfile[0][BOOTP].ciaddr)


#clear ARP Cache
# os.system('arp -d')

#Build ARP Packet // Send ARP Request
# ARPRequest = Ether(src='14:f6:d8:a4:ae:f8',dst='ff:ff:ff:ff:ff:ff') / ARP(op=1,hwsrc='1e:22:3f:9f:55:79',hwdst='00:00:00:00:00:00',psrc='192.168.11.22',pdst='192.168.11.254') 
# sendp(ARPRequest)
# time.sleep(2)

#Build ICMP ping 192.168.11.29
# result ,nums = sr(IP(src='192.168.11.8',dst='192.168.11.22')/ICMP(), retry=5, timeout=3)
# print(result.show())
# if result:
#     print('Susses')
# else:
#     print('False')
# #for s, r in result:
# #   print(r[ARP].hwsrc)





