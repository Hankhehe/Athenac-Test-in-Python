from packet_action import PacketAction
#from scapy.all import sendp,Ether,IP,UDP,RadiusAttr_NAS_IP_Address,RadiusAttribute,Radius,RadiusAttr_Vendor_Specific,rdpcap 
from scapy.all import *
import hashlib
import hmac
import base64


class PacketActionTest(PacketAction):
    def SendRadiusRequest(self):
        authenticator = hashlib.md5(bytes(Radius(authenticator=bytes.fromhex('00000000000000000000000000000000'),attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))]))+b'pixis').hexdigest()
        radiusrequestpacket = Ether(src =self.mac,dst='00:00:0c:9f:f0:0b')\
         /IP(src=self.Ip,dst='192.168.10.180')\
            /UDP(sport =51818,dport=1812)\
               /Radius(authenticator=bytes.fromhex(authenticator),attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))])
        sendp(radiusrequestpacket)
    
    def SendRadiusCoARequest(self):
        hashdata = bytes(Radius(code=40,id=15,len=39,attributes=[RadiusAttribute(type=31,len=19,value=b'AA:AA:AA:AA:AA:AA')]))
        hashobj = hashlib.md5()
        hashobj.update(hashdata+b'pixis')
        auth = hashobj.hexdigest()
        readiusCoArequestpacket = Ether(src =self.mac,dst='00:00:0c:9f:f0:15')\
         /IP(src=self.Ip,dst='192.168.10.249')\
            /UDP(sport =51818,dport=3799)\
               /Radius(id =15,code = 40,len=39,authenticator=auth
               ,attributes=[#RadiusAttr_NAS_IP_Address(value=b'192.168.10.249')
               RadiusAttribute(type=31,len=19,value=b'AA:AA:AA:AA:AA:AA')
               #,RadiusAttribute(type=80,value=bytearray.fromhex('AABB11'))
               #,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
               ])
        sendp(readiusCoArequestpacket)
    
    def TestCoAMessageAuthenHash(self): #Test CoA Message-Authenticator Calculate
        packet = rdpcap('D:/CoA.pcap')
        oringinalpacket = bytes(packet[0].payload).hex()
        fakebytes = bytes.fromhex('2b05009fb14e7e3b8b584188997afe5851057a1e0406ac1e64f51f1338432d31362d34352d33412d44312d37323706619648da5012000000000000000000000000000000001a29000000090123737562736372696265723a636f6d6d616e643d726561757468656e7469636174651a3100000009012b61756469742d73657373696f6e2d69643d414331453634463530303030303134374331314445313344')
        h= hmac.new(b'pixis',fakebytes,hashlib.md5).hexdigest()
        print(h)
        pass

    def TestRadiusAuthenHash(self): #測試 Radius Authenticator Calculate
        packet = rdpcap('D:/CoA.pcap')
        oringinalpacket = bytes.fromhex('2b020028000000000000000000000000000000000406ffffffff1f0e303035303536414541364336') # Radius Potocol 全部，但 Authenticator 要補 16 byte 的 0 
        h = hashlib.md5(oringinalpacket+b'pixis').hexdigest()
        print(h)
        pass