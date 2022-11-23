import time,re
from CreateData import macrelated,iprelated
from scapy.all import get_working_if,get_working_ifaces,srp,sendp,conf,Ether,ARP,IP,UDP,BOOTP,DHCP,IPv6,DHCP6_Solicit,DHCP6OptElapsedTime,DHCP6OptClientId\
   ,DHCP6OptIA_NA,DHCP6OptOptReq,DHCP6_Request,DHCP6OptServerId,DHCP6OptIAAddress,ICMPv6NDOptDstLLAddr,DHCP6_Advertise,ICMPv6ND_NS,ICMPv6NDOptSrcLLAddr\
      ,ICMPv6ND_RA,ICMPv6NDOptMTU,ICMPv6NDOptPrefixInfo,ICMPv6ND_NA,Radius,RadiusAttr_NAS_IP_Address,RadiusAttribute,NBNSRequest

class PacketAction:

   def __init__(self,nicname:str=get_working_if().name) -> None: 
      conf.checkIPaddr = False
      self.nicname = nicname
      self.nic = [x for x in get_working_ifaces() if nicname == x.name][0]
      self.Ip= self.nic.ip
      self.mac = self.nic.mac
      self.linklocalIp = [x for x in self.nic.ips[6] if 'fe80::' in x][0]
      self.globalIp = [x for x in self.nic.ips[6] if '2001:' in x][0]
      self.gatewayIp = conf.route.route('0.0.0.0')[2] 
      self.gatewatIpv6 = conf.route6.route('::')[2]
   
   def GetIPfromDHCPv4(self,tranId:int,mac:str)->str | None:   #取得新DHCPv4
      '''給一個 ID 和 MAC 後會從 DHCP 協定取一個 IPv4'''
      macformat = bytearray.fromhex(''.join(mac.split(':')))
      DHCPDiscover = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /IP(src='0.0.0.0',dst='255.255.255.255')\
            /UDP(sport=68,dport=67)\
               /BOOTP(xid=tranId,chaddr=macformat)\
                  /DHCP(options=[('message-type','discover'),'end'])
      resultoffer ,numsoffer = srp(DHCPDiscover,timeout=5,iface=self.nicname)
      if resultoffer:
         yIP = resultoffer[0][1][BOOTP].yiaddr
         tranId = resultoffer[0][1][BOOTP].xid
         DHCPRequest = Ether(src=self.mac,dst='ff:ff:ff:ff:ff:ff')\
            /IP(src='0.0.0.0',dst='255.255.255.255')\
               /UDP(sport=68,dport=67)\
                  /BOOTP(xid=tranId,chaddr=macformat)\
                     /DHCP(options=[('message-type','request'),('requested_addr',yIP),'end'])
         resultACK,numsACK=srp(DHCPRequest,timeout=5,iface=self.nicname)
      else: return 
      if resultACK :
         return yIP
      
      
   def GetIPfromDHCPv6(self,tranId:int,mac:str)->str | None:  #取得新DHCPv6
      duidformat = bytearray.fromhex('000100012796d07c'+''.join(mac.split(':')))
      iaidformat = int('08' + ''.join(mac.split(':'))[0:6],16)
      DHCPv6Solicit = Ether(src =self.mac,dst='33:33:00:01:00:02')\
         /IPv6(src=self.linklocalIp,dst='ff02::1:2')\
            /UDP(sport=546,dport=547)\
               /DHCP6_Solicit(trid=tranId)\
                  /DHCP6OptElapsedTime()\
                     /DHCP6OptClientId(duid=duidformat)\
                        /DHCP6OptIA_NA(iaid=iaidformat)\
                           /DHCP6OptOptReq()
      resultAdvertise ,numAdvertise = srp(DHCPv6Solicit,timeout=20,iface=self.nicname)
      if resultAdvertise:
         DHCPv6Request =Ether(src =self.mac,dst='33:33:00:01:00:02')\
            /IPv6(src=self.linklocalIp,dst='ff02::1:2')\
               /UDP(sport=546,dport=547)\
                  /DHCP6_Request(trid=tranId)\
                     /DHCP6OptElapsedTime()\
                        /DHCP6OptClientId(duid=resultAdvertise[0][1][DHCP6OptClientId].duid)\
                           /DHCP6OptServerId(duid= resultAdvertise[0][1][DHCP6OptServerId].duid)\
                              /DHCP6OptIA_NA(iaid=resultAdvertise[0][1][DHCP6OptIA_NA].iaid,T1=resultAdvertise[0][1][DHCP6OptIA_NA].T1
                              ,T2=resultAdvertise[0][1][DHCP6OptIA_NA].T2,ianaopts=resultAdvertise[0][1][DHCP6OptIA_NA].ianaopts)\
                                 /DHCP6OptOptReq()
         resultACK6 ,numACK6 = srp(DHCPv6Request,timeout=20,iface=self.nicname)
      else:
         return 
      if resultACK6:
         return resultAdvertise[0][1][DHCP6OptIAAddress].addr

   def ARPBlockCheck(self,srcIP:str,dstIP:str,ProbeMAC:str)->bool:  #ARP 封鎖確認
      ARPRequest = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /ARP(op=1,hwsrc=self.mac, hwdst="00:00:00:00:00:00",psrc=srcIP, pdst=dstIP)
      result ,nums = srp(ARPRequest, retry=2,timeout=5,iface=self.nicname,multi=True)
      if not result : return False
      for s, r in result:
         if r[ARP].psrc == dstIP and r[ARP].hwsrc == ProbeMAC and r[ARP].hwdst == self.mac and r[ARP].pdst == srcIP:
            return True
      return False
   
   def ARPBlockCheckforProtect(self,srcIP:str,dstIP:str,ProbeMAC:str)->bool:
      '''ARP 封鎖確認 for 固定 IP 且使用 0.0.0.0 詢問時'''
      ARPRequest = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /ARP(op=1,hwsrc=self.mac, hwdst="00:00:00:00:00:00",psrc=srcIP, pdst=dstIP)
      result ,nums = srp(ARPRequest, retry=2,timeout=5,iface=self.nicname,multi=True)
      if not result : return False
      for s, r in result:
         if r[ARP].psrc == dstIP and r[ARP].hwsrc == ProbeMAC and r[ARP].hwdst == self.mac:
            return True
      return False

   def NDPBlockCheck(self,srcIP:str,dstIP:str,ProbeMAC:str)->bool:
      IPv6IPfull = iprelated.ConvertIPv6ShortToIPv6Full(dstIP)
      dstMACformulti = ':'.join( re.findall(r'.{2}','3333ff'+ IPv6IPfull[-7:].replace(':','')))
      dipformulti = 'ff02::1:ff'+IPv6IPfull[-7:]
      NDPSolic = Ether(src =self.mac,dst=dstMACformulti)\
         /IPv6(src=srcIP,dst=dipformulti)\
            /ICMPv6ND_NS(tgt=dstIP)
      result ,nums = srp(NDPSolic,retry=2,timeout=5,iface=self.nicname,multi=True)
      if not result: return False
      for s, r in result:
         if r[ICMPv6ND_NA].tgt == dstIP and r[ICMPv6NDOptDstLLAddr].lladdr == ProbeMAC and r[IPv6].dst == srcIP and r[Ether].dst == self.mac:
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
      DHCPv6Advertise = Ether(src =self.mac,dst='33:33:00:00:00:01')\
         /IPv6(src=self.linklocalIp,dst='ff02::1')\
            /UDP(sport=547,dport=546)\
               /DHCP6_Advertise(trid=1)
      sendp(DHCPv6Advertise,iface=self.nicname)
   
   def SendRA(self,flagM:int=0,flagO:int=0)->None:
      RouteAdvertise = Ether(src =self.mac,dst='33:33:00:00:00:01')\
         /IPv6(src=self.globalIp,dst='ff02::1')\
            /ICMPv6ND_RA(prf=0,M=flagM,O=flagO)\
               /ICMPv6NDOptSrcLLAddr(lladdr=self.mac)\
                  /ICMPv6NDOptMTU()\
                     /ICMPv6NDOptPrefixInfo(prefix='2001:b030:2133:99::')
      sendp(RouteAdvertise,iface=self.nicname)

   def SendARPReply(self,IP:str,MAC:str|None=None,Count:int=1,WaitSec:int=0)->None:
      if MAC :
         MAC = macrelated.FormatMACbyPunctuation(mac=MAC,Punctuation=':')
      else: MAC = self.mac 
      for i in range(Count):
         ARPReply = Ether(src = MAC,dst='ff:ff:ff:ff:ff:ff')\
            /ARP(op=2, hwsrc=MAC, psrc=IP)
         sendp(ARPReply,iface=self.nicname)
         time.sleep(WaitSec)

   def SendNA(self,IP:str,MAC:str|None=None,Count:int=1,WaitSec:int=0)->None:
      if MAC :
         MAC = macrelated.FormatMACbyPunctuation(mac=MAC,Punctuation=':')
      else : MAC =self.mac
      for i in range(Count):
         NDPAdver = Ether(src =MAC,dst='33:33:00:00:00:01')\
            /IPv6(src=IP,dst='ff02::1')\
               /ICMPv6ND_NA(tgt=IP,R=0)\
                  /ICMPv6NDOptSrcLLAddr(type=2,lladdr=MAC)
         sendp(NDPAdver,iface=self.nicname)
         time.sleep(WaitSec)

   def GetIPv4MAC(self,dstip:str)->str | None:
      arprequest = Ether(src=self.mac,dst = 'ff:ff:ff:ff:ff:ff')\
         /ARP(op=1,hwsrc=self.mac, hwdst="00:00:00:00:00:00",psrc=self.Ip, pdst=dstip)
      result ,nums = srp(arprequest, retry=2,timeout=5,iface=self.nicname)
      return result[0][1][ARP].hwsrc if result else None
      
   def GetRadiusReply(self,serverip:str,nasip:str)->dict | None:
      '''Radius Code : Accept =2 , Reject =3'''
      dstmac = self.GetIPv4MAC(self.gatewayIp)
      if not dstmac: return
      RadiusReq =Ether(src =self.mac,dst=dstmac)\
         /IP(src=self.Ip,dst=serverip)\
            /UDP(sport =51818,dport=1812)\
               /Radius(authenticator=b'pixis',attributes=[RadiusAttr_NAS_IP_Address(value=nasip.encode('utf-8')),RadiusAttribute(type=31,len=19,value=self.mac.encode('utf-8'))])
      result ,nums =srp(RadiusReq,retry=3,timeout=5,iface=self.nicname)
      if not result : return
      ReplyData = {}
      ReplyData['RadiusCode'] = result[0][1][Radius].code
      for resultdata in result[0][1][Radius].attributes:
         if resultdata.type == 81:
            ReplyData['VLANId'] = resultdata.value.decode('utf-8')
            break
      return ReplyData
   
   def SendNBNSResponse(self,name:str,workgroup:bool) -> None:
      NBNSResponsepacket = Ether(src=self.mac,dst='ff:ff:ff:ff:ff:ff')\
         /IP(src=self.Ip,dst='255.255.255.255')\
            /UDP(sport=137,dport=137)\
               /NBNSRequest(NB_ADDRESS=self.Ip,QUESTION_NAME=name,G=workgroup)
      sendp(NBNSResponsepacket,iface=self.nicname)