from scapy.all import *
import datetime

class PacketListen:

    def __init__(self,ProbeMAC:str,NicName:str=get_working_if().name) -> None:
        conf.checkIPaddr = False
        self.probeMAC = ProbeMAC
        self.nicName = NicName
        self.nic = [x for x in get_working_ifaces() if NicName == x.name][0]
        self.Ip= self.nic.ip
        self.mac = self.nic.mac
        self.linklocalIP = [x for x in self.nic.ips[6] if 'fe80::' in x]
        self.globallIP = [x for x in self.nic.ips[6] if '2001:' in x]
        self.checklist ={'WinodwsOS':False,'Linux':False,'iOS':False,'Clock':False,'Printer':False}
# 'ether src {ProbeMAC} and ((udp and src port 45231 and dst port 45231) or (tcp and src port 18005 and dst port 445)\
#             or (tcp and src port 18006 and dst port 62078) or (tcp and src port 18009 and (dst port 1621 or dst port 515 or dst port 9100 or dst port 631)) or arp)'
        #if filte then need setting that, exsample : fillter = 'arp or udp or tcp' for sniff() etc.....
        sniff(filter =f'ether src {self.probeMAC} and ((udp and src port 45231 and dst port 45231) or (tcp and src port 18005 and dst port 445)\
             or (tcp and src port 18006 and dst port 62078) or (tcp and src port 18009 and (dst port 1621 or dst port 515 or dst port 9100 or dst port 631)))'
        ,store = 0,prn=self.CheckPacket ,timeout =1900 ,iface=self.nicName)

    def CheckPacket(self,Packet):
        
        if '45231' in Packet: self.checklist['Linux'] = True;return
        elif '18005' and '445'in Packet: self.checklist['WinodwsOS'] = True;return
        elif '18006' and '62078' in Packet : self.checklist['iOS']=True;return
        elif '18009' and ('4660' or '1621') in Packet : self.checklist['Clock'] = True;return
        elif '18009' and ('515' or '9100' or '631') in Packet: self.checklist['Printer'] = True;return
        
        print(self.checklist)

    def printPacket(self,Packet):
        print(Packet.summary())


pcapfile = rdpcap('D:/SMB.pcap')
PacketListen('b8:27:eb:63:9b:01')