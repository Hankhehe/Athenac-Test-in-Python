from scapy.all import conf,get_working_ifaces,get_working_if,sniff,TCP,UDP
import datetime

class PacketListenOSCheck:

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

        #if filte then need setting that, exsample : filter = 'arp or udp or tcp' for sniff() etc.....
        sniff(filter=f'ether src {ProbeMAC} and ether dst {self.mac} and ((udp and src port 45231 and dst port 45231) or (tcp and src port 18005 and dst port 445)\
             or (tcp and src port 18006 and dst port 62078) or (tcp and src port 18009 and (dst port 4660 or dst port 1621 or dst port 515 or dst port 9100 or dst port 631)))'
        ,store = 0,prn=self.CheckTCPorUDP ,timeout =1900 ,iface=self.nicName)
        print(self.checklist)

    def CheckTCPorUDP(self,Packet):
        if TCP in Packet:  self.CheckTCPPacket(Packet)
        elif UDP in Packet: self.CheckUDPPacket(Packet)

    def CheckTCPPacket(self,Packet):
        if Packet['TCP'].sport ==  18005 and Packet['TCP'].dport == 445: self.checklist['WinodwsOS']=True
        elif Packet['TCP'].sport == 18006 and Packet['TCP'].dport == 62078: self.checklist['iOS']=True
        elif Packet['TCP'].sport == 18009 \
            and (Packet['TCP'].dport == 1621 or Packet['TCP'].dport == 515 or Packet['TCP'].dport == 9100 or Packet['TCP'].dport==631):
            self.checklist['Printer']=True 
        elif Packet['TCP'].sport == 18009 and Packet['TCP'].dport == 1621 or Packet['TCP'].dport == 4660: self.checklist['Clock']=True

    def CheckUDPPacket(self,Packet):
        if Packet['UDP'].sport ==  45231 and Packet['UDP'].dport == 45231: self.checklist['Linux']=True

    def printPacket(self,Packet):
        print(Packet.summary())
