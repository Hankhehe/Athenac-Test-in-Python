from NetPacketTools.packet_action import PacketAction
from scapy.all import sendp,Ether,IP,UDP,RadiusAttr_NAS_IP_Address,RadiusAttribute,Radius,RadiusAttr_Vendor_Specific,rdpcap,wrpcap 
import hashlib,hmac,time


class PacketRelated8021X(PacketAction):
    def SendRadiusRequest(self):
        dstmac = self.GetIPv4MAC('192.168.11.254')
        authenticator = hashlib.md5(bytes(Radius(authenticator=bytes.fromhex('0'*32),attributes=[RadiusAttr_NAS_IP_Address(value=b'192.168.10.249'),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))]))+b'pixis').hexdigest()
        radiusrequestpacket = Ether(src =self.mac,dst=dstmac)\
         /IP(src=self.Ip,dst='192.168.10.12')\
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

    def CalcuRespondAuthenticator(self,pcapfilepath:str,RespounseIdx:int,RequestIdx:int,secrectkey:bytes) -> None:
        radiusRespondPacketPayload = rdpcap(pcapfilepath)[RespounseIdx-1]['Radius']
        radiusRespondPacketPayload.authenticator = rdpcap(pcapfilepath)[RequestIdx-1]['Radius'].authenticator
        print('authenticator Before : ' + radiusRespondPacketPayload.authenticator.hex())
        print('authenticator : '+hashlib.md5(bytes(radiusRespondPacketPayload)+secrectkey).hexdigest())

    def CalculateHashFromPacket(self,pcapfilepath:str,RespounseIdx:int,RequestIdx:int,secrectkey:bytes):
        '''計算 Radius Challeng 和 accept 的 message-auth 和 authencatitor'''
        
        #使用前一包 Request 的 Authenticator 並將 Message Authenticator 變 0 計算
        #先 Hash 出 message-auth 後值填進去後再把 authencatitor 的值 Hash 出來
        radiuspacketpayload = rdpcap(pcapfilepath)[RespounseIdx-1]['Radius']
        radiuspacketpayload.authenticator = rdpcap(pcapfilepath)[RequestIdx-1]['Radius'].authenticator
        radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
        print('-------------------------A = lastrequest、M = 0-----------------------------------------')
        print('Message-Authen Before : ' + radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
        radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex(hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())
        print('Message-Authen : ' +radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('authenticator Before : ' + radiuspacketpayload.authenticator.hex())
        print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())
