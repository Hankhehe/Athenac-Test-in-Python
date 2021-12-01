from scapy import packet
from scapy.all import conf,get_working_ifaces,get_working_if,sniff,TCP,UDP,ICMP,Ether,IP,Radius
import datetime
class PacketListenFromFilter:
    def __init__(self,NicName:str=get_working_if().name) -> None:
        conf.checkIPaddr = False
        self.nicName = NicName
        self.nic = [x for x in get_working_ifaces() if NicName == x.name][0]
        self.Ip= self.nic.ip
        self.mac = self.nic.mac
        self.linklocalIP = [x for x in self.nic.ips[6] if 'fe80::' in x]
        self.globallIP = [x for x in self.nic.ips[6] if '2001:' in x]
        self.radiuspackets:list[dict] = []
        # self.other = []
        
    def Sniffer(self,Filter:str,time:int)->None:
        if not Filter and not str : return
        sniff(filter = f'(ether dst {self.mac} or ether dst ff:ff:ff:ff:ff:ff) and {Filter}', store = 0,prn=self.CheckPacketType ,timeout =time ,iface=self.nicName)

    def CheckPacketType(self,Packet):
        if TCP in Packet:  self.CheckTCPPacket(Packet['TCP'])
        elif UDP in Packet: self.CheckUDPPacket(Packet['UDP'])
        elif ICMP in Packet: self.CheckICMPPacket(Packet['ICMP'])
        else: pass

    def CheckTCPPacket(self,Packet):
        pass

    def CheckUDPPacket(self,Packet):
        if Radius in Packet:self.GetRadiusPacket(Packet['Radius'])
        else:pass

    
    def CheckICMPPacket(self,Packet):
        pass

    
    def CheckOtherPacket(self,Packet):
        pass
        # print(f'{str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} Other Packet : {Packet.summary()}')
    
    def GetRadiusPacket(self,Packet)->None:
        self.radiuspackets.append({'time':datetime.datetime.now(),'packet':Packet})
