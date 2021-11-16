from packet_action import PacketAction
from scapy.all import sendp,Ether,IP,UDP,RadiusAttr_NAS_IP_Address,RadiusAttribute,Radius,RadiusAttr_Vendor_Specific
import hashlib

class PacketActionTest(PacketAction):
    def SendRadiusRequest(self):
        radiusrequestpacket = Ether(src =self.mac,dst='00:00:0c:9f:f0:15')\
         /IP(src=self.Ip,dst='192.168.10.180')\
            /UDP(sport =51818,dport=1812)\
               /Radius(authenticator=b'pixis',attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))])
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