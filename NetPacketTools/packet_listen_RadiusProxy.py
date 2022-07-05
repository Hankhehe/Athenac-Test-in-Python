import socket,threading,hashlib,hmac
from scapy.all import get_working_if,get_working_ifaces,sniff,srp,sendp,conf,Ether,IP,UDP,RadiusAttribute,RadiusAttr_EAP_Message,Radius,RadiusAttr_Message_Authenticator
 
class PacketListenRadiusProxy:
    def __init__(self,RadiusServerIP:str,gatewayMAC:str,RadiusPort:int,secrectkey:bytes,NicName:str=get_working_if().name) -> None:
        conf.checkIPaddr = False
        self.nicName = NicName
        self.nic = [x for x in get_working_ifaces() if NicName == x.name][0]
        self.Ip= self.nic.ip
        self.mac = self.nic.mac
        self.secrectkey = secrectkey
        self.GatewayMAC = gatewayMAC
        self.RadiusClientIP = ''
        self.RadiusServerIP = RadiusServerIP
        self.RadiusPort = RadiusPort
        self.radiusrequestauthcode = bytes(00*16)
        thread1 = threading.Thread(target=self.CreateUDPClient)
        thread1.start()
        
    def Sniffer(self,Filter:str,time:int)->None:
        if not Filter and not str : return
        sniff(filter = f'(ether dst {self.mac} or ether dst ff:ff:ff:ff:ff:ff) and {Filter}', store = 0,prn=self.CheckPacketType ,timeout =time ,iface=self.nicName)

    def CheckPacketType(self,Packet):
        if UDP in Packet:
            if Packet['Radius'].code == 1:
                self.RadiusClientIP = Packet['IP'].src
            self.CheckUDPPacket(Packet['UDP'])
        else: pass

    def CheckUDPPacket(self,Packet):
        if Packet['Radius'].code == 1 :
            self.radiusrequestauthcode =  bytes(Packet.authenticator)
            self.ForwardRadiusPacke(Packet=Packet['Radius'],dip=self.RadiusServerIP,srcport =Packet['UDP'].sport,dstport = self.RadiusPort)
        elif Packet['Radius'].code == 2 :
            self.SendAcceptAndReplaceVLANID(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport,secrectkey=self.secrectkey)
        elif Packet['Radius'].code == 3 :
            self.SendReject(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport,secrectkey=self.secrectkey)
        elif Packet['Radius'].code == 11 :
            self.ForwardRadiusPacke(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport)
        else:pass
    
    def ForwardRadiusPacke(self,Packet,dip:str,srcport:int,dstport:int):
        RadiusReq =Ether(src =self.mac,dst=self.GatewayMAC)\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
               /Packet
        srp(RadiusReq,timeout=5,iface=self.nicName)
    
    def SendReject(self,Packet,dip:str,srcport:int,dstport:int,secrectkey:bytes):
        Packet['RadiusAttr_EAP_Message'].value.code = 4
        RadiusPaylod = Radius(code=3,id=Packet.id,authenticator=self.radiusrequestauthcode
        ,attributes=[RadiusAttr_EAP_Message(value=Packet['RadiusAttr_EAP_Message'].value)
                ,RadiusAttr_Message_Authenticator(type =80,value=bytes.fromhex('0'*32))])

        # 額外加入 VLAN ID 的 Attribute    
        # RadiusPaylod.attributes.append(RadiusAttribute(type=65,value=bytes.fromhex('00000006')))
        # RadiusPaylod.attributes.append(RadiusAttribute(type=81,value=b'83'))
        # RadiusPaylod.attributes.append(RadiusAttribute(type=64,value=bytes.fromhex('0000000d')))

        RadiusPaylod['RadiusAttr_Message_Authenticator'].value =bytes.fromhex(hmac.new(secrectkey,bytes(RadiusPaylod),hashlib.md5).hexdigest())
        RadiusPaylod.authenticator = bytes.fromhex(hashlib.md5(bytes(RadiusPaylod)+secrectkey).hexdigest())
        RadiusResponse =Ether(src =self.mac,dst=self.GatewayMAC)\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
                /RadiusPaylod
        sendp(RadiusResponse,iface=self.nicName)

    def SendAcceptAndReplaceVLANID(self,Packet,dip:str,srcport:int,dstport:int,secrectkey:bytes):
        Packet.len = None
        if Packet.code == 3 :
            Packet.code = 2
            Packet['RadiusAttr_EAP_Message'].value.code = 3
        
        #新增 VLAN ID 相關的 Attributes
        Packet.attributes.append(RadiusAttribute(type=65,value=bytes.fromhex('00000006')))
        Packet.attributes.append(RadiusAttribute(type=81,value=b'22'))
        Packet.attributes.append(RadiusAttribute(type=64,value=bytes.fromhex('0000000d')))

        Packet.authenticator = self.radiusrequestauthcode
        Packet['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
        Packet['RadiusAttr_Message_Authenticator'].value = bytes.fromhex(hmac.new(secrectkey,bytes(Packet),hashlib.md5).hexdigest())
        Packet.authenticator = bytes.fromhex(hashlib.md5(bytes(Packet)+secrectkey).hexdigest())
        RadiusReq =Ether(src =self.mac,dst=self.GatewayMAC)\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
                /Packet
        sendp(RadiusReq,iface=self.nicName)

    def CreateUDPClient(self):
        localIP     = "0.0.0.0"
        localPort   = self.RadiusPort
        bufferSize  = 1024
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((localIP, localPort))
        while True:
            UDPServerSocket.recvfrom(bufferSize)

