import time
from scapy.all import get_working_if,get_working_ifaces,srp,conf,Ether,IP,UDP,BOOTP,DHCP,IPv6,DHCP6_Solicit,DHCP6OptElapsedTime,DHCP6OptClientId\
   ,DHCP6OptIA_NA,DHCP6OptOptReq,DHCP6_Request,DHCP6OptServerId,DHCP6OptIAAddress

class DHCPTestData:
    def __init__(self) -> None:
        self.DiscoverTime:float
        self.OfferTime:float|None = None
        self.RequestTime:float|None = None
        self.ACKTime:float|None = None

class PacketActionDHCPasync:
    def __init__(self,nicname:str=get_working_if().name) -> None: 
        conf.checkIPaddr = False
        self.nicname = nicname
        self.nic = [x for x in get_working_ifaces() if nicname == x.name][0]
        self.mac = self.nic.mac
        self.linklocalIp = [x for x in self.nic.ips[6] if 'fe80::' in x][0]
        self.testresultforDHCP = {}

    def GetIPfromDHCPv4(self,tranId:int,mac:str,logfile:str)-> None:   #取得新DHCPv4
        '''給一個 ID 和 MAC 後會從 DHCP 協定取一個 IPv4'''
        DHCPData = DHCPTestData()
        self.testresultforDHCP[str(hex(tranId))] = {}
        macformat = bytearray.fromhex(''.join(mac.split(':')))
        DHCPDiscover = Ether(src =self.mac,dst='ff:ff:ff:ff:ff:ff')\
            /IP(src='0.0.0.0',dst='255.255.255.255')\
                /UDP(sport=68,dport=67)\
                /BOOTP(xid=tranId,chaddr=macformat)\
                    /DHCP(options=[('message-type','discover'),'end'])
        DHCPData.DiscoverTime = time.time()
        self.testresultforDHCP[str(hex(tranId))]['Discover'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.DiscoverTime))
        resultoffer ,numsoffer = srp(DHCPDiscover,timeout=30,iface=self.nicname)
        if resultoffer:
            DHCPData.OfferTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['Offer'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.OfferTime))
            self.testresultforDHCP[str(hex(tranId))]['Dis_to_Offer'] = int(DHCPData.OfferTime - DHCPData.DiscoverTime)
            yIP = resultoffer[0][1][BOOTP].yiaddr
            tranId = resultoffer[0][1][BOOTP].xid
            DHCPRequest = Ether(src=self.mac,dst='ff:ff:ff:ff:ff:ff')\
                /IP(src='0.0.0.0',dst='255.255.255.255')\
                /UDP(sport=68,dport=67)\
                    /BOOTP(xid=tranId,chaddr=macformat)\
                        /DHCP(options=[('message-type','request'),('requested_addr',yIP),'end'])
            DHCPData.RequestTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['Request'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.RequestTime))
            resultACK,numsACK=srp(DHCPRequest,timeout = 30,iface=self.nicname)
        else:
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)},No Offer Packet \n')
            return 
        if resultACK :
            DHCPData.ACKTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['ACK'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.ACKTime))
            self.testresultforDHCP[str(hex(tranId))]['Req_to_ACK'] = int(DHCPData.ACKTime - DHCPData.RequestTime)
            self.testresultforDHCP[str(hex(tranId))]['YourIP'] = yIP
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)},{int(DHCPData.OfferTime - DHCPData.DiscoverTime)},{int(DHCPData.ACKTime - DHCPData.RequestTime)},{yIP} \n')
        else:
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)}, No ACK Packet \n')
            return
        
    def GetIPfromDHCPv6(self,tranId:int,mac:str,logfile:str)->str | None:  #取得新DHCPv6
        DHCPData = DHCPTestData()
        self.testresultforDHCP[str(hex(tranId))] = {}
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
        DHCPData.DiscoverTime = time.time()
        self.testresultforDHCP[str(hex(tranId))]['Discover'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.DiscoverTime))
        resultAdvertise ,numAdvertise = srp(DHCPv6Solicit,timeout=30,iface=self.nicname)
        if resultAdvertise:
            DHCPData.OfferTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['Offer'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.OfferTime))
            self.testresultforDHCP[str(hex(tranId))]['Dis_to_Offer'] = int(DHCPData.OfferTime - DHCPData.DiscoverTime)
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
            DHCPData.RequestTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['Request'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.RequestTime))
            resultACK6 ,numACK6 = srp(DHCPv6Request,timeout=30,iface=self.nicname)
        else:
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)},No Offer Packet \n')
            return 
        if resultACK6:
            DHCPData.ACKTime = time.time()
            self.testresultforDHCP[str(hex(tranId))]['ACK'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( DHCPData.ACKTime))
            self.testresultforDHCP[str(hex(tranId))]['Req_to_ACK'] = int(DHCPData.ACKTime - DHCPData.RequestTime)
            self.testresultforDHCP[str(hex(tranId))]['YourIP'] = resultAdvertise[0][1][DHCP6OptIAAddress].addr
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)},{int(DHCPData.OfferTime - DHCPData.DiscoverTime) },{int(DHCPData.ACKTime - DHCPData.RequestTime)},{resultAdvertise[0][1][DHCP6OptIAAddress].addr} \n')
        else:
            with open(logfile,'a') as f:
                f.write(f'{hex(tranId)}, No ACK Packet \n')
            return