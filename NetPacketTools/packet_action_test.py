from packet_action import PacketAction
from scapy.all import sendp,Ether,IP,UDP,RadiusAttr_NAS_IP_Address,RadiusAttribute,Radius,RadiusAttr_Vendor_Specific,rdpcap 
from scapy.all import *
import hashlib
import hmac
import base64


class PacketActionTest(PacketAction):
    def SendRadiusRequest(self):
        dstmac = self.GetIPv4MAC('192.168.11.254')
        authenticator = hashlib.md5(bytes(Radius(authenticator=bytes.fromhex('0'*32),attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))]))+b'pixis').hexdigest()
        radiusrequestpacket = Ether(src =self.mac,dst=dstmac)\
         /IP(src=self.Ip,dst='192.168.10.180')\
            /UDP(sport =51818,dport=1812)\
               /Radius(authenticator=bytes.fromhex(authenticator),attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))])
        sendp(radiusrequestpacket)
    
    def SendRadiusCoARequest(self):
        hexnowtime = hex(int(time.time()))
        nomessagepacket = bytes(Radius(code=40,authenticator=bytes.fromhex('0'*32)
        ,attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249')
        ,RadiusAttribute(type=31,len=19,value=b'AA:AA:AA:AA:AA:AA')
        ,RadiusAttribute(type=55,len=19,value=bytes.fromhex(hexnowtime[2::]))
        ,RadiusAttribute(type=80,value=bytearray.fromhex('0'*32))
        ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
        ]))

        MessageAuth = hmac.new(b'pixis',nomessagepacket,hashlib.md5).hexdigest()
        hasmessagepacket = bytes(Radius(code=40,authenticator=bytes.fromhex('0'*32)
        ,attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249')
        ,RadiusAttribute(type=31,len=19,value=b'AA:AA:AA:AA:AA:AA')
        ,RadiusAttribute(type=55,len=19,value=bytes.fromhex(hexnowtime[2::]))
        ,RadiusAttribute(type=80,value=bytearray.fromhex(MessageAuth))
        ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
        ]))
        authenticator = hashlib.md5(hasmessagepacket+b'pixis').hexdigest()

        readiusCoArequestpacket = Ether(src =self.mac,dst=self.GetIPv4MAC('192.168.11.254'))\
         /IP(src=self.Ip,dst='192.168.10.249')\
            /UDP(sport =51818,dport=3799)\
               /Radius(code = 40,authenticator=bytes.fromhex(authenticator)
               ,attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249')
               ,RadiusAttribute(type=31,len=19,value=b'AA:AA:AA:AA:AA:AA')
               ,RadiusAttribute(type=80,value=bytearray.fromhex(MessageAuth))
               ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
               ])
        sendp(readiusCoArequestpacket)
    
    def TestCoAMessageAuthenHash(self): #Test CoA Message-Authenticator Calculate
        packet = rdpcap('D:/CoA.pcap')
        oringinalpacket = bytes(packet[0].payload).hex()
        fakebytes = bytes.fromhex('2b05009f000000000000000000000000000000000406ac1e64f51f1338432d31362d34352d33412d44312d37323706619648da5012000000000000000000000000000000001a29000000090123737562736372696265723a636f6d6d616e643d726561757468656e7469636174651a3100000009012b61756469742d73657373696f6e2d69643d414331453634463530303030303134374331314445313344')
        h= hmac.new(b'cisco',fakebytes,hashlib.md5).hexdigest() # Message-Authenticator
        print(h)

        hasmessagebytes = bytes.fromhex('2b05009f000000000000000000000000000000000406ac1e64f51f1338432d31362d34352d33412d44312d37323706619648da5012'+h+'1a29000000090123737562736372696265723a636f6d6d616e643d726561757468656e7469636174651a3100000009012b61756469742d73657373696f6e2d69643d414331453634463530303030303134374331314445313344')
        authenticator = hashlib.md5(hasmessagebytes+b'cisco').hexdigest()
        print(authenticator)
        pass

    def TestRadiusAuthenHash(self): #測試 Radius Authenticator Calculate
        packet = rdpcap('D:/CoA.pcap')
        oringinalpacket = bytes.fromhex('2b020028000000000000000000000000000000000406ffffffff1f0e303035303536414541364336') # Radius Potocol 全部，但 Authenticator 要補 16 byte 的 0 
        h = hashlib.md5(oringinalpacket+b'pixis').hexdigest()
        print(h)
        pass