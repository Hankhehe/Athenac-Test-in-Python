from NetPacketTools.packet_action import PacketAction
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
        nasip =b'192.168.21.10'
        callmac=b'00-E0-4C-68-07-A0'
        presharkey = b'pixis'
        hexnowtime = hex(int(time.time()))
        serverIP ='192.168.11.250'
        radiuspacket = Radius(id=90,code=43,authenticator=bytes.fromhex('0'*32)
        ,attributes=[RadiusAttr_NAS_IP_Address(value=nasip)
        ,RadiusAttribute(type=31,len=2+len(callmac),value=callmac)
        # ,RadiusAttribute(type=49,value=bytes.fromhex('00000006'))
        ,RadiusAttribute(type=55,value=bytes.fromhex(hexnowtime[2::]))
        ,RadiusAttribute(type=80,value=bytearray.fromhex('0'*32))
        ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'subscriber:command=reauthenticate')
        ,RadiusAttr_Vendor_Specific(vendor_id=9,vendor_type=1,value=b'audit-session-id=C0A80BFA0000002200095192')
        # ,RadiusAttribute(type=44,value=b'AC11FFE90000027A5FA080B6')
        ])

        MessageAuth = hmac.new(presharkey,bytes(radiuspacket),hashlib.md5).hexdigest()
        radiuspacket.attributes[3].value = bytes.fromhex(MessageAuth)

        authenticator = hashlib.md5(bytes(radiuspacket)+presharkey).hexdigest()
        radiuspacket.authenticator = bytes.fromhex(authenticator)
        readiusCoArequestpacket = Ether(src =self.mac,dst=self.GetIPv4MAC('192.168.21.254'))\
         /IP(src=self.Ip,dst=serverIP)\
            /UDP(sport =51818,dport=3799)\
               /radiuspacket
        wrpcap('C:/Users/Public/CoA.pcap',readiusCoArequestpacket)
        sendp(readiusCoArequestpacket)

    def CalculateHashFromCustomerPacket(self): #計算客戶封包的 Hash key
        try:
            packetpcap = rdpcap('C:/Users/Public/CoACustomer.pcap')
            presharkey = b'cisco'
            radiuspacket = Radius(packetpcap[0]['Raw'].load)
            radiuspacket.authenticator = bytes.fromhex('0'*32)
            print('authenticator : '+hashlib.md5(bytes(radiuspacket)+presharkey).hexdigest())
            radiuspacket['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
            print('Message-Authen : ' +hmac.new(presharkey,bytes(radiuspacket),hashlib.md5).hexdigest())
        except:
            print('Error Packet')

    def CalculateHashFromPacket(self): #計算封包的 Hash key
        try:
            packetpcap = rdpcap('C:/Users/Public/CoA.pcap')
            presharkey = b'pixis'
            radiuspacket = packetpcap[0]['Radius']
            radiuspacket.authenticator = bytes.fromhex('0'*32)
            print('authenticator : '+hashlib.md5(bytes(radiuspacket)+presharkey).hexdigest())
            radiuspacket['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
            print('Message-Authen : ' +hmac.new(presharkey,bytes(radiuspacket),hashlib.md5).hexdigest())
        except:
            print('Error Packet')