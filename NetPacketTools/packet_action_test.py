from packet_action import PacketAction
from scapy.all import sendp,Ether,IP,UDP,RadiusAttr_NAS_IP_Address,RadiusAttribute,Radius,RadiusAttr_Vendor_Specific,rdpcap,wrpcap 
import hashlib
import hmac
import base64
import time


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
        nasip =b'192.168.21.180'
        callmac=b'B8-27-EB-A3-5F-14'
        hexnowtime = hex(int(time.time()))
        radiuspacket = Radius(id=1,code=40,authenticator=bytes.fromhex('0'*32)
        ,attributes=[RadiusAttr_NAS_IP_Address(value=nasip)
        ,RadiusAttribute(type=31,len=19,value=callmac)
        ,RadiusAttribute(type=49,value=bytes.fromhex('00000006'))
        ,RadiusAttribute(type=55,value=bytes.fromhex(hexnowtime[2::]))
        ,RadiusAttribute(type=80,value=bytearray.fromhex('0'*32))
        # ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
        ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'audit-session-id=AC11FFE90000025B5B1329D4')
        ])

        MessageAuth = hmac.new(b'pixis',bytes(radiuspacket),hashlib.md5).hexdigest()
        radiuspacket.attributes[4].value = bytes.fromhex(MessageAuth)

        authenticator = hashlib.md5(bytes(radiuspacket)+b'pixis').hexdigest()
        radiuspacket.authenticator = bytes.fromhex(authenticator)
        readiusCoArequestpacket = Ether(src =self.mac,dst=self.GetIPv4MAC('192.168.21.254'))\
         /IP(src=self.Ip,dst='192.168.10.233')\
            /UDP(sport =51818,dport=3799)\
               /radiuspacket
        wrpcap('C:/Users/Public/CoA.pcap',readiusCoArequestpacket)
        sendp(readiusCoArequestpacket)

    def CalculateHashFromCustomerPacket(self): #計算客戶封包的 Hash key
        packetpcap = rdpcap('C:/Users/Public/CoACustomer.pcap')
        presharkey = b'cisco'
        radiuspacket = Radius(packetpcap[0]['Raw'].load)
        radiuspacket.authenticator = bytes.fromhex('0'*32)
        print('authenticator : '+hashlib.md5(bytes(radiuspacket)+presharkey).hexdigest())
        radiuspacket['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
        print('Message-Authen : ' +hmac.new(presharkey,bytes(radiuspacket),hashlib.md5).hexdigest())

    def CalculateHashFromPacket(self): #計算封包的 Hash key
        packetpcap = rdpcap('C:/Users/Public/CoA.pcap')
        presharkey = b'pixis'
        radiuspacket = packetpcap[0]['Radius']
        radiuspacket.authenticator = bytes.fromhex('0'*32)
        print('authenticator : '+hashlib.md5(bytes(radiuspacket)+presharkey).hexdigest())
        radiuspacket['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
        print('Message-Authen : ' +hmac.new(presharkey,bytes(radiuspacket),hashlib.md5).hexdigest())