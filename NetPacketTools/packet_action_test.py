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
    
    def CalcuProxyMessageAuthenticator(self,pcapfilepath:str,packetidx:int,secrectkey:bytes) -> None:
        radiusProxyPacketPayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        radiusOringPacketPayload = rdpcap(pcapfilepath)[packetidx-1]['Radius']
        radiusProxyPacketPayload.authenticator = bytes.fromhex('00'*16)
        radiusProxyPacketPayload['RadiusAttr_Message_Authenticator'].value = radiusOringPacketPayload['RadiusAttr_Message_Authenticator'].value
        print('authenticator Before : ' + radiusProxyPacketPayload.authenticator.hex())
        print('Message-Authen Before : ' + radiusProxyPacketPayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiusProxyPacketPayload),hashlib.md5).hexdigest())
        radiusProxyPacketPayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('00'*16)
        print('authenticator Before : ' + radiusProxyPacketPayload.authenticator.hex())
        print('Message-Authen Before : ' + radiusProxyPacketPayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiusProxyPacketPayload),hashlib.md5).hexdigest())

    def CalcuRespondAuthenticator(self,pcapfilepath:str,packetidx:int,secrectkey:bytes) -> None:
        radiusRespondPacketPayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        radiusRequestPacketPayload = rdpcap(pcapfilepath)[packetidx-1]['Radius']
        radiusRespondPacketPayload.authenticator = radiusRequestPacketPayload.authenticator
        print('authenticator Before : ' + radiusRespondPacketPayload.authenticator.hex())
        print('authenticator : '+hashlib.md5(bytes(radiusRespondPacketPayload)+secrectkey).hexdigest())

    def CalculateHashFromPacket(self,pcapfilepath:str,packetidx:int,secrectkey:bytes): #計算封包的 Hash key 
        # pcapfilepath = 'D:/test.pcap'
        # secrectkey = b'pixis'

        # 原檔計算
        radiuspacketpayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        print('-------------------------A = 原始、M = 原始-----------------------------------------')
        print('authenticator Before : ' + radiuspacketpayload.authenticator.hex())
        print('Message-Authen Before : ' + radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())
        print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())

        #只將 Request Authenticator 變 0 計算
        radiuspacketpayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        radiuspacketpayload.authenticator = bytes.fromhex('0'*32)
        print('-------------------------A = 0、M = 原始-----------------------------------------')
        print('authenticator Before : ' + radiuspacketpayload.authenticator.hex())
        print('Message-Authen Before : ' + radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
        print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())
        print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())

        #只將 Message-Authenticator 變 0 計算
        radiuspacketpayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        try:
            radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
            print('-------------------------A = 原始、M = 0-----------------------------------------')
            print('authenticator Before : ' + radiuspacketpayload.authenticator.hex())
            print('Message-Authen Before : ' + radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
            print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())
            print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())
        except Exception as e:
            print(e)

        #將 Request Authenticator 和 Message Authenticator 變 0 計算
        radiuspacketpayload = rdpcap(pcapfilepath)[packetidx]['Radius']
        try:
            radiuspacketpayload.authenticator = bytes.fromhex('0'*32)
            radiuspacketpayload['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
            print('-------------------------A = 0、M = 0-----------------------------------------')
            print('authenticator Before : ' + radiuspacketpayload.authenticator.hex())
            print('Message-Authen Before : ' + radiuspacketpayload['RadiusAttr_Message_Authenticator'].value.hex())
            print('authenticator : '+hashlib.md5(bytes(radiuspacketpayload)+secrectkey).hexdigest())
            print('Message-Authen : ' +hmac.new(secrectkey,bytes(radiuspacketpayload),hashlib.md5).hexdigest())
        except Exception as e:
            print(e)

    def CreateCISCOExampleRadiusPacp(self,outputpath:str)->None:
        '''Secrect Key is "cisco" '''
        packetbyte =bytes.fromhex('0116 0167 bed9 5259 5783 02c0 f918 4df6 \
            2b85 9d6b 0107 6369 7363 6f06 0600 0000 \
            020c 0600 0005 dc1e 1341 412d 4242 2d43 \
            432d 3030 2d36 342d 3030 1f13 3038 2d30 \
            302d 3237 2d36 452d 4335 2d35 304f ca02 \
            4100 c819 8000 0000 be16 0301 0086 1000 \
            0082 0080 880d 0fe6 8421 562e bcf3 75a7 \
            fbf4 9c20 e114 a19d 1282 96d7 45b8 9c26 \
            86c5 9935 1b2c ca98 1b60 5e91 1c63 d123 \
            f019 1ab6 7e2d 0497 1e02 0768 0ac3 aa84 \
            80d5 cd14 92a9 ae31 e9e2 121e 28e8 5f21 \
            5c1a 4e20 013f a55b 7b1d 0eb7 1d17 a565 \
            626b 2bb4 f756 da05 b51b 043b 346a c51f \
            98a7 007e ed55 e24b 1cab ec06 799b aed5 \
            72c5 451b 1403 0100 0101 1603 0100 28e2 \
            d25f 2deb 0f0c baf5 570d d3f6 05df 6534 \
            48d8 0853 00ae 3230 73a9 afb7 ac87 0834 \
            f7e9 bb57 8ac1 1750 1201 418d 3b18 6555 \
            6918 269d 3cf7 3608 b03d 0600 0000 0f05 \
            0600 00c3 5057 0d45 7468 6572 6e65 7430 \
            2f30 181f 3236 5365 7373 696f 6e49 443d \
            6163 732f 3134 3531 3136 3739 372f 3132 \
            3b04 06c0 a80a 0a')
        radiuspecket = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /IP(src='192.168.10.10',dst='192.168.10.150')\
            /UDP(sport =51818,dport=1812)\
                /packetbyte
        wrpcap(outputpath,radiuspecket)

    def Createradiusexample(self,outputpath:str)->None:
        packetbytes = bytes.fromhex('28 00 00 35 00 00 00 00 \
        00 00 00 00 00 00 00 00 \
        00 00 00 00 01 0d 31 38 \
        36 31 30 34 37 36 33 30 \
        30 1f 0e 38 34 37 61 38 \
        38 65 37 37 33 30 64 04 \
        06 c0 a8 01 fa 74 65 73 \
        74 69 6e 67 31 32 33')
        radiuspecket = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /IP(src='192.168.10.10',dst='192.168.10.150')\
            /UDP(sport =51818,dport=1812)\
                /packetbytes
        wrpcap(outputpath,radiuspecket)


    def Encrypt_Pass(self,password, authenticator, secret):
        m = hashlib.md5()
        m.update(secret+authenticator)
        return "".join(chr(ord(x) ^ ord(str(y))) for x, y in zip(password.ljust(16,'\0')[:16], m.digest()[:16]))