import time
from scapy.all import get_working_if,get_working_ifaces,srp,sendp,conf,Ether,ARP,IP,UDP,BOOTP,DHCP,IPv6,DHCP6_Solicit,DHCP6OptElapsedTime,DHCP6OptClientId\
   ,DHCP6OptIA_NA,DHCP6OptOptReq,DHCP6_Request,DHCP6OptServerId,DHCP6OptIAAddress,ICMPv6NDOptDstLLAddr,DHCP6_Advertise,ICMPv6ND_NS,ICMPv6NDOptSrcLLAddr\
      ,ICMPv6ND_RA,ICMPv6NDOptMTU,ICMPv6NDOptPrefixInfo,ICMPv6ND_NA,Radius,RadiusAttr_NAS_IP_Address,RadiusAttribute

class PacketAction:

   def __init__(self,nicname:str=get_working_if().name) -> None:
      conf.checkIPaddr = False
      self.nicname = nicname
      self.nic = [x for x in get_working_ifaces() if nicname == x.name][0]
      self.Ip= self.nic.ip
      self.mac = self.nic.mac
      self.linklocalIp = [x for x in self.nic.ips[6] if 'fe80::' in x]
      self.globalIp = [x for x in self.nic.ips[6] if '2001:' in x]
      self.gatewayIp = conf.route.route('0.0.0.0')[2] 
      self.gatewatIpv6 = conf.route6.route('::')[2]
      
   def DHCPv4ClientTest(self,count:int=70)-> str:
      logStr = ''
      yIP,tranId = '',0
      fakeMACNum =186916976721920
      for i in range(count):
         fakeMAC= bytearray.fromhex(hex(fakeMACNum)[2::])
         DHCPDiscover = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
            /IP(src='0.0.0.0',dst='255.255.255.255')\
               /UDP(sport=68,dport=67)\
                  /BOOTP(xid=tranId,chaddr=fakeMAC)\
                     /DHCP(options=[('message-type','discover'),'end'])
         resultoffer ,numsoffer = srp(DHCPDiscover,timeout=5,iface=self.nicname)
         if not resultoffer:
            logStr+='No receive DHCP Offer ID: %s \n' %(tranId)
         else:
            yIP = resultoffer[0][1][BOOTP].yiaddr
            tranId = resultoffer[0][1][BOOTP].xid
            DHCPRequest = Ether(src=self.mac,dst='ff:ff:ff:ff:ff:ff')\
               /IP(src='0.0.0.0',dst='255.255.255.255')\
                  /UDP(sport=68,dport=67)\
                     /BOOTP(xid=tranId,chaddr=fakeMAC)\
                        /DHCP(options=[('message-type','request'),('requested_addr',yIP),'end'])
            resultACK,numsACK=srp(DHCPRequest,timeout=5,iface=self.nicname)
            if not resultACK: logStr +='no Receive DHCP ACK %s | IP: %s \n'%(tranId,yIP)
         tranId+=1
         fakeMACNum+=1
      return logStr

   def DHCPv6ClientTest(self,count:int=700)-> str:
      logStr = ''
      tranId,Iana,ClientId,ServerId = 0,'','',''
      fakeMACNum =186916976721920
      for i in range(count):
         DHCPv6Solicit = Ether(src =self.mac,dst='33:33:00:01:00:02')\
            /IPv6(src=self.linklocalIp,dst='ff02::1:2')\
               /UDP(sport=546,dport=547)\
                  /DHCP6_Solicit(trid=tranId)\
                     /DHCP6OptElapsedTime()\
                        /DHCP6OptClientId(duid=bytearray.fromhex('000100012796d07c'+hex(fakeMACNum)[2::]))\
                           /DHCP6OptIA_NA(iaid=0x08aa0000)\
                              /DHCP6OptOptReq()
         resultAdvertise ,numAdvertise = srp(DHCPv6Solicit,timeout=20,iface=self.nicname)
         if not resultAdvertise:
            logStr +='No receive DHCPv6 Advertise ID: %s \n' %(tranId)
         else:
            Iana = resultAdvertise[0][1][DHCP6OptIA_NA]
            ClientId = resultAdvertise[0][1][DHCP6OptClientId]
            ServerId = resultAdvertise[0][1][DHCP6OptServerId]
            DHCPv6Request =Ether(src =self.mac,dst='33:33:00:01:00:02')\
               /IPv6(src=self.linklocalIp,dst='ff02::1:2')\
                  /UDP(sport=546,dport=547)\
                     /DHCP6_Request(trid=tranId)\
                        /DHCP6OptElapsedTime()\
                           /ClientId\
                              /ServerId\
                                 /Iana\
                                    /DHCP6OptOptReq()
            resultACK6 ,numACK6 = srp(DHCPv6Request,timeout=20,iface=self.nicname)
            if not resultACK6:
               logStr+='No receive DHCPv6 ACK ID: %s | IP: %s \n' %(tranId,Iana[0][1][DHCP6OptIAAddress].addr)
         tranId+=1
         fakeMACNum+=1
      return logStr

   def ARPBlockCheck(self,srcIP:str,dstIP:str,ProbeMAC:str)->bool:
      ARPRequest = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /ARP(op=1,hwsrc=self.mac, hwdst="00:00:00:00:00:00",psrc=srcIP, pdst=dstIP)
      result ,nums = srp(ARPRequest, retry=2,timeout=5,iface=self.nicname,multi=True)
      if not result : return
      for s, r in result:
         if r[ARP].hwsrc == ProbeMAC:
            return True
      return False

   def NDPBlockCheck(self,srcIP:str,dstIP:str,ProbeMAC:str)->bool:
      NDPSolic = Ether(src =self.mac,dst='33:33:ff:00:00:01')\
         /IPv6(src=srcIP,dst='ff02::1')\
            /ICMPv6ND_NS(tgt=dstIP)
      result ,nums = srp(NDPSolic,retry=2,timeout=5,iface=self.nicname,multi=True)
      if not result: return
      for s, r in result:
         if r[ICMPv6NDOptDstLLAddr].lladdr == ProbeMAC:
            return True
      return False

   def SendDHCPv4Offer(self)->None:
      DHCPv4Offer = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /IP(src=self.Ip,dst='255.255.255.255')\
            /UDP(sport=67,dport=68)\
               /BOOTP(xid=1,chaddr=bytearray.fromhex('aa0000000000'),yiaddr ='192.168.1.87')\
                  /DHCP(options=[('message-type','offer'),'end'])
      sendp(DHCPv4Offer,iface=self.nicname)
   
   def SendDHCPv6Advertise(self)->None:
      DHCPv6Advertise = Ether(src =self.mac,dst='33:33:ff:00:00:01')\
         /IPv6(src=self.linklocalIp,dst='ff02::1')\
            /UDP(sport=547,dport=546)\
               /DHCP6_Advertise(trid=1)
      sendp(DHCPv6Advertise,iface=self.nicname)
   
   def SendRA(self)->None:
      RouteAdvertise = Ether(src =self.mac,dst='33:33:ff:00:00:01')\
         /IPv6(src=self.globalIp,dst='ff02::1')\
            /ICMPv6ND_RA(prf=0)\
               /ICMPv6NDOptSrcLLAddr(lladdr=self.mac)\
                  /ICMPv6NDOptMTU()\
                     /ICMPv6NDOptPrefixInfo(prefix='2001:b030:2133:99::')
      sendp(RouteAdvertise,iface=self.nicname)

   def SendARPReply(self,IP:str,Count:int=1,WaitSec:int=0)->None:
      for i in range(Count):
         ARPReply = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
            /ARP(op=2, hwsrc=self.mac, psrc=IP)
         sendp(ARPReply,iface=self.nicname)
         time.sleep(WaitSec)

   def SendNA(self,IP:str,Count:int=1,WaitSec:int=0)->None:
      for i in range(Count):
         NDPAdver = Ether(src =self.mac,dst='33:33:ff:00:00:01')\
            /IPv6(src=IP,dst='ff02::1')\
               /ICMPv6ND_NA(tgt=IP,R=0,S=1)\
                  /ICMPv6NDOptSrcLLAddr(type=2,lladdr=self.mac)
         sendp(NDPAdver,iface=self.nicname)
         time.sleep(WaitSec)

   def GetIPv4MAC(self,dstip:str)->str:
      arprequest = Ether(src=self.mac,dst = 'ff:ff:ff:ff:ff:ff')\
         /ARP(op=1,hwsrc=self.mac, hwdst="00:00:00:00:00:00",psrc=self.Ip, pdst=dstip)
      result ,nums = srp(arprequest, retry=2,timeout=5,iface=self.nicname)
      return result[0][1][ARP].hwsrc if result else None
      
   def GetRadiusReply(self,serverip:str,nasip)->dict:
      dstmac = self.GetIPv4MAC(serverip)
      if not dstmac: return
      RadiusReq =Ether(src =self.mac,dst=dstmac)\
         /IP(src=self.Ip,dst=serverip)\
            /UDP(sport =51818,dport=1812)\
               /Radius(authenticator=b'pixis',attributes=[RadiusAttr_NAS_IP_Address(value=nasip.encode('utf-8')),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))])
      result ,nums =srp(RadiusReq,retry=3,timeout=5,iface=self.nicname)
      if not result : return
      if len(result[0][1][Radius].attributes) > 1 :
         return {'RadiusCode':result[0][1][Radius].code,'VLANId':result[0][1][Radius].attributes[1].value.decode('utf-8')}
      else : 
         return {'RadiusCode':result[0][1][Radius].code}
      #Radius Code : Accept =2 , Reject =3