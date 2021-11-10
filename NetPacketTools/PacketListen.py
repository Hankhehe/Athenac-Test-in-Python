from scapy.all import *
from collections import Counter
import datetime

class PacketListen:

    def __init__(self,NicName:str=get_working_if().name) -> None:
        conf.checkIPaddr = False
        self.nicName = NicName
        self.nic = [x for x in get_working_ifaces() if NicName == x.name][0]
        self.Ip= self.nic.ip
        self.mac = self.nic.mac
        self.linklocalIP = [x for x in self.nic.ips[6] if 'fe80::' in x]
        self.globallIP = [x for x in self.nic.ips[6] if '2001:' in x]

        #if filte then need setting that, exsample : fillter = 'arp or udp or tcp' for sniff() etc.....
        sniff(filter ='tcp or udp or ip',store = 0,prn=self.printPacket ,iface=self.nicName)

    def PacketTodo(self,Packet):
        if 'TCP' in Packet: self.printTCPPacket(Packet)
        elif 'UDP' in Packet: self.printUDPPacket(Packet)
        else:print(Packet.summary())

    def printTCPPacket(self,Packet):
        print('%s TCP Packet -----: %s '%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),Packet.sprintf("{IP: %IP.src% -> %IP.dst% | MAC: %Ether.src% -> MAC:%Ether.dst% | Port: %TCP.sport% -> %TCP.dport%}")))

    def printUDPPacket(self,Packet):
        print('%s UPP Packet -----: %s '%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),Packet.sprintf("{IP: %IP.src% -> %IP.dst% | MAC: %Ether.src% -> MAC:%Ether.dst% | Port: %UDP.sport% -> %UDP.dport%}")))

    def printPacket(self,Packet):
        print(Packet.summary())




# ## Create a Packet Counter
# packet_counts = Counter()

# ## Define our Custom Action function
# def custom_action(packet):
#     # Create tuple of Src/Dst in sorted order
#     key = tuple(sorted([packet[0][1].src, packet[0][1].dst]))
#     packet_counts.update([key])
#     return f"Packet #{sum(packet_counts.values())}: {packet[0][1].src} ==> {packet[0][1].dst}"

# ## Setup sniff, filtering for IP traffic
# sniff(filter="ip", prn=custom_action, count=1000,iface='Wi-Fi')

# ## Print out packet count per A <--> Z address pair
# print("\n".join(f"{f'{key[0]} <--> {key[1]}'}: {count}" for key, count in packet_counts.items()))