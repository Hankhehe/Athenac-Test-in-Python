import socket,threading,hashlib,hmac
from scapy.all import get_working_if,get_working_ifaces,sniff,srp,conf,Ether,IP,UDP,RadiusAttr_Framed_Protocol
 
class PacketListenRadiusProxy:
    def __init__(self,RadiusClientIP:str,RadiusServerIP:str,RadiusPort:int,secrectkey:bytes,NicName:str=get_working_if().name) -> None:
        conf.checkIPaddr = False
        self.nicName = NicName
        self.nic = [x for x in get_working_ifaces() if NicName == x.name][0]
        self.Ip= self.nic.ip
        self.mac = self.nic.mac
        self.secrectkey = secrectkey
        self.RadiusClientIP = RadiusClientIP
        self.RadiusServerIP = RadiusServerIP
        self.RadiusPort = RadiusPort
        self.radiusrequestauthcode = bytes(00*16)
        thread1 = threading.Thread(target=self.CreateUDPClient)
        thread1.start()
        
    def Sniffer(self,Filter:str,time:int)->None:
        if not Filter and not str : return
        sniff(filter = f'(ether dst {self.mac} or ether dst ff:ff:ff:ff:ff:ff) and {Filter}', store = 0,prn=self.CheckPacketType ,timeout =time ,iface=self.nicName)

    def CheckPacketType(self,Packet):
        if UDP in Packet: self.CheckUDPPacket(Packet['UDP'])
        else: pass

    def CheckUDPPacket(self,Packet):
        if Packet['UDP'].dport== self.RadiusPort :
            self.radiusrequestauthcode =  bytes(Packet.authenticator)
            self.ForwardRadiusPacke(Packet=Packet['Radius'],dip=self.RadiusServerIP,srcport =Packet['UDP'].sport,dstport = self.RadiusPort)
        elif Packet['UDP'].sport == self.RadiusPort:
            if Packet['UDP'].code == 2:
                self.SendRadiusAcceptAndReplace(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport,secrectkey=self.secrectkey)
                # self.SendRadiufsAcceptAndReplaceIncMessandAuth(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport,secrectkey=self.secrectkey)
            else:
                self.ForwardRadiusPacke(Packet=Packet['Radius'],dip=self.RadiusClientIP,srcport =self.RadiusPort,dstport = Packet['UDP'].dport)
        else:pass
    
    def ForwardRadiusPacke(self,Packet,dip:str,srcport:int,dstport:int):
        RadiusReq =Ether(src =self.mac,dst='00:00:0c:9f:f0:11')\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
               /Packet
        srp(RadiusReq,timeout=5,iface=self.nicName)
    
    def SendRadiusAcceptAndReplace(self,Packet,dip:str,srcport:int,dstport:int,secrectkey:bytes):
        for i in range(len(Packet.attributes)): #如果判斷到 AVPs 裡有 Message-Auth AVP 就刪除
            print(Packet.attributes[i])
            if Packet.attributes[i].type == 80:
                del Packet.attributes[i] 
                Packet.len = Packet.len - 18 #封包長度須減掉 Message-auth 的 AVP 長度
        # Packet.attributes[1].value = b'12' #如有需要改 VLAN 時才需要這個 Code
        Packet.authenticator = self.radiusrequestauthcode
        Packet.attributes.append(RadiusAttr_Framed_Protocol(type=7,value=1)) #增加 PPP AVP 在最後面
        Packet.len = Packet.len + 6 #封包長度需增加 PPP 的 AVP 長度
        Packet.authenticator = bytes.fromhex(hashlib.md5(bytes(Packet)+secrectkey).hexdigest())
        
        RadiusReq =Ether(src =self.mac,dst='00:00:0c:9f:f0:11')\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
                /Packet
        srp(RadiusReq,timeout=5,iface=self.nicName)
    
    def SendRadiufsAcceptAndReplaceIncMessandAuth(self,Packet,dip:str,srcport:int,dstport:int,secrectkey:bytes):
        Packet.authenticator = self.radiusrequestauthcode
        Packet.attributes[1].value = b'12'
        # Packet.attributes.append(RadiusAttr_Framed_Protocol(type=7,value=1)) #增加 PPP AVP 在最後面
        # Packet.len = Packet.len + 6 #封包長度需增加 PPP 的 AVP 長度
        Packet['RadiusAttr_Message_Authenticator'].value = bytes.fromhex('0'*32)
        Packet['RadiusAttr_Message_Authenticator'].value = bytes.fromhex(hmac.new(secrectkey,bytes(Packet),hashlib.md5).hexdigest())
        Packet.authenticator = bytes.fromhex(hashlib.md5(bytes(Packet)+secrectkey).hexdigest())
        RadiusReq =Ether(src =self.mac,dst='00:00:0c:9f:f0:11')\
         /IP(src=self.Ip,dst=dip)\
            /UDP(sport =srcport,dport=dstport)\
                /Packet
        srp(RadiusReq,timeout=5,iface=self.nicName)

    def CreateUDPClient(self):
        localIP     = "0.0.0.0"
        localPort   = self.RadiusPort
        bufferSize  = 1024
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((localIP, localPort))
        while True:
            UDPServerSocket.recvfrom(bufferSize)

