import csv,time,json,base64
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from NetPacketTools.packet_listen_RadiusProxy import PacketListenRadiusProxy
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action_DHCPasync import PacketActionDHCPasync
from multiprocessing import Pool

#計算 Radius 封包的 Message Auth 和 Authenticator
# Calculate8021X().CalculateHashFromPacket(pcapfilepath='NetPacketTools/packet_calculator/RadiusPacket.pcap',RespounseIdx=2,RequestIdx=1,secrectkey=b'pixis')
# pass


#region memo
class CreateAlotOfEnvironment:
    def CreateProbe(self,Count:int)-> None:
        iplist = iprelated.CreateIPDataByCIDROrPrifix('10.0.0.0/22')
        maclist = macrelated.CreateMACData(mac='AB0000000000',count=Count+1)
        for i in range(1,Count+1):
            CoreAPI = AthenacCoreAPILibry(f'http://{serverIP_}:18000','20000000'+str(i),'10000000'+str(i))
            CoreAPI.LoginProbeToServer(daemonip=str(iplist[i]),mac=maclist[i])
        
    def CreateIPRange(self,ImportFile) -> None:
        FileDatas = list()
        with open(ImportFile,newline='') as f :
            Rows = csv.reader(f)
            for Row in Rows:
                FileDatas.append(Row)
        del FileDatas[0]
        for FileData in FileDatas:
            AthenacWebAPI_.EnablePortWorker(isTrunk=True,VLANId=int(FileData[2]),Enable=True,PortWorkerID=FileData[0],ManageIPCIDR=FileData[3],Gateway=FileData[4])
        for FileData in FileDatas :
            AthenacWebAPI_.AddNetwork(ProbeID=FileData[0],NetworkName=FileData[1],VLANID=FileData[2])
            AthenacWebAPI_.AddRange(mIP=FileData[3],gwIP=FileData[4],NetworkName=FileData[1])

def RunRadiusProxy() -> None:
    '''啟用 Radius Proxy'''
    listen1 = PacketListenRadiusProxy(RadiusServerIP='192.168.10.1',gatewayMAC='00:00:0c:9f:f0:11',RadiusPort= 1812,NicName= 'Ethernet1',secrectkey=b'pixis')
    listen1.Sniffer('udp and port 1812',60*60*24)

def SendIPConflict(IP:str,MAClist:list[str])->None:
    '''發送 IP 衝突'''
    while True:
        for i in MAClist :
            lan2_.SendARPReply(IP=IP,MAC=i)
        time.sleep(2)

def SendOnline() ->None:
    '''發送大量的 IPv4 和 IPv6 d上線'''
    ipv4list = iprelated.CreateIPDataByCIDROrPrifix(cidr='172.17.0.0/17')
    ipv6list = iprelated.CreateIPDataByCIDROrPrifix(cidr='2001:b030:2133:811::/112')
    maclist = macrelated.CreateMACData(mac='AA0000000000',count=32768)
    while True :
        for i in range(1,5001):
            lan2_.SendARPReply(IP=str(ipv4list[i]),MAC=maclist[i])
            lan2_.SendNA(IP=str(ipv6list[i]),MAC=maclist[i])


#region config
with open('settingconfig_ReleaseTest.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = base64.b64encode(settingconfig_['APIpwd'].encode('UTF-8'))
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
# AthenacCoreAPI_ = AthenacCoreAPILibry(f'http://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
# AthenacProbeAPI_ = AthenacProbeAPILibry(f'http://{AthenacWebAPI_.GetPortWorerkIPbyID(settingconfig_["probeID"])}:18002')
TestIPv4_ = settingconfig_['TestIPv4']
TestIPv6_ = settingconfig_['TestIPv6']
ProbeMAC_ = settingconfig_['ProbeMAC']
# VLANIDMapping_ = settingconfig_['VLANIDMapping']
# SiteID_ = settingconfig_['SiteId']
# DynamicAVPID_ = settingconfig_['DynamicAVPID']
# AuthAVPID_ = settingconfig_['AuthAVPID']
lan1_ = PacketActionDHCPasync(nicname=settingconfig_['lan1'])
lan1MACUpper_ = ''.join(lan1_.mac.upper().split(':'))
lan2_ = PacketAction(settingconfig_['lan2'])
lan2MACUpper_ = ''.join(lan2_.mac.upper().split(':'))
#endregion config

# lan1_.SendNBNSResponse(name='Hank',workgroup=False) #發送主機名稱 by NBNS
# lan1_.SendNBNSResponse(name='WORKGROUP',workgroup=True) #發送網域群組 by NBNS
# SendOnline()
# SendIPConflict(IP='172.17.0.5',MAClist=['AA0000000000','AA1111111111','AA2222222222'])
# lan2_.GetIPfromDHCPv4(tranId=1,mac=)
# RunRadiusProxy()
# t = CreateAlotOfEnvironment()
# t.CreateProbe(Count=1023)
# t.CreateIPRange('IPRange.csv')