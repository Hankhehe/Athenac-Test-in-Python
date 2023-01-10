import csv,time,json,base64
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.athenac_probe_API_libry import AthenacProbeAPILibry
from NetPacketTools.packet_listen_RadiusProxy import PacketListenRadiusProxy
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action_DHCPasync import PacketActionDHCPasync
from NetPacketTools.packet_calculator.calculate_8021X import Calculate8021X
from APITools.DataModels.datamodel_apidata import SettingConfigByTest
from multiprocessing import Pool

# 計算 Radius 封包的 Message Auth 和 Authenticator
# Calculate8021X().CalculateHashFromPacket(pcapfilepath='NetPacketTools/packet_calculator/RadiusPacket.pcap',RespounseIdx=2,RequestIdx=1,secrectkey=b'pixis')
# pass

class CreateAlotOfEnvironment:
    def CreateProbe(self,Count:int)-> None:
        iplist = iprelated.CreateIPDataByCIDROrPrifix('10.0.0.0/22')
        maclist = macrelated.CreateMACData(mac='AB0000000000',count=Count+1)
        for i in range(1,Count+1):
            CoreAPI = AthenacCoreAPILibry(f'http://{Testconfig_.serverIP}:18000','20000000'+str(i),'10000000'+str(i),lan1_.Ip)
            CoreAPI.LoginProbeToServer(daemonip=str(iplist[i]),mac=maclist[i])
        
    def CreateIPRange(self,ImportFile:str) -> None:
        FileDatas = list()
        with open(ImportFile,newline='') as f :
            Rows = csv.reader(f)
            for Row in Rows:
                FileDatas.append(Row)
        del FileDatas[0]
        pool = Pool(14)
        networkDatas , rangeDatas = [],[]
        for FileData in FileDatas :
            networkDatas.append((FileData[0],FileData[1],FileData[2]))
            rangeDatas.append((FileData[3],FileData[4],FileData[1]))
        pool.starmap(AthenacWebAPI_.AddDNSByNetwork,networkDatas)
        pool.starmap(AthenacWebAPI_.AddRange,rangeDatas)

    def DelNetworkeByFile(self,ImportFile:str) -> None:
        FileDatas = list()
        with open(ImportFile,newline='') as f :
            Rows = csv.reader(f)
            for Row in Rows:
                FileDatas.append(Row)
        del FileDatas[0]
        pool = Pool(14)
        networkIDs = []
        for FileData in FileDatas :
            NetworkID = AthenacWebAPI_.GetNetworkInfoByName(FileData[1])
            if NetworkID :
                networkIDs.append(NetworkID)
        pool.map(AthenacWebAPI_.DelNetwork,networkIDs)

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



#region config
Testconfig_ = SettingConfigByTest('ConfigJson/Server_ReleaseTest.json')
lan1_ = PacketAction(Testconfig_.lan1)
lan1MACUpper_ = ''.join(lan1_.mac.upper().split(':'))
lan2_ = PacketAction(Testconfig_.lan2)
lan2MACUpper_ = ''.join(lan2_.mac.upper().split(':'))
AthenacWebAPI_ = AthenacWebAPILibry(f'https://{Testconfig_.serverIP}:8001',Testconfig_.APIaccount,base64.b64encode(Testconfig_.APIPwd.encode('UTF-8')),lan1_.Ip)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{Testconfig_.serverIP}:18000',Testconfig_.probeID,Testconfig_.daemonID,lan1_.Ip)
AthenacProbeAPI_ = AthenacProbeAPILibry(f'http://{AthenacWebAPI_.GetPortWorerkIPbyID(Testconfig_.probeID)}:18002',lan1_.Ip)

#endregion config

# lan1_.SendNBNSResponse(name='Hank',workgroup=False) #發送主機名稱 by NBNS
# lan1_.SendNBNSResponse(name='WORKGROUP',workgroup=True) #發送網域群組 by NBNS
# SendIPConflict(IP='172.17.0.5',MAClist=['AA0000000000','AA1111111111','AA2222222222'])
# RunRadiusProxy()
if __name__ == '__main__':
    t = CreateAlotOfEnvironment()
    # t.CreateProbe(Count=1023)
    # t.CreateIPRange('IPRange_Hank.csv')
    # t.DelNetworkeByFile('IPRange_Hank.csv')
