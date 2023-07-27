import time,base64
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.athenac_probe_API_libry import AthenacProbeAPILibry
from NetPacketTools.packet_action_DHCPasync import PacketActionDHCPasync
from multiprocessing import Pool
from APITools.DataModels.datamodel_apidata import SettingConfigByTest

class TestDHCP:
    def test_DHCPv4(self)->None:
        '''DHCPv4 壓力測試'''
        macint = 186916976721920 #產生假 MAC AA0000000000
        for tranId in range(700):
            result =  lan2_.GetIPfromDHCPv4(tranId=tranId,mac=hex(macint)[2::]) #檢查是否有從 DHCP ACK 中取得資料
            assert result,f'The tranID ID {tranId} gets IPv4 fail'
            macint +=1 #每跑完一次 MAC 加一 ex AA0000000000 to AA0000000001

    def test_DHCPv6(self)->None:
        '''DHCPv6 壓力測試'''
        macint = 186916976721920 #產生假 MAC AA0000000000
        for tranId in range(700):
            result =  lan2_.GetIPfromDHCPv6(tranId=tranId,mac=hex(macint)[2::]) #檢查是否有從 DHCPv6 ACK 中取得資料
            assert result,f'The tranID ID {tranId} gets IPv6 fail'
            macint +=1 #每跑完一次 MAC 加一 ex AA0000000000 to AA0000000001
    
    def test_DHCPAsync(self,Count:int,logfile:str) -> None:
        '''DHCPv4 壓力測試非同步'''
        lan = PacketActionDHCPasync('Ethernet2')
        inputs = []
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=3000)
        for i in range(Count):
            inputs.append((i,maclist[i],logfile))
        pool = Pool(14)
        with open(logfile,'w') as f :
            f.write('TranID,between dis and Offer Time,between req and ACK time,YourIP \n')
        pool.starmap(lan.GetIPfromDHCPv4, inputs)
        
    def test_DHCPv6Async(self,Count:int,logfile:str) -> None:
        '''DHCPvv6 壓力測試非同步'''
        lan = PacketActionDHCPasync('Ethernet2')
        inputs = []
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=3000)
        for i in range(Count):
            inputs.append((i,maclist[i],logfile))
        pool = Pool(14)
        with open(logfile,'w') as f :
            f.write('TranID,between dis and Offer Time,between req and ACK time,YourIP \n')
        pool.starmap(lan.GetIPfromDHCPv6,inputs)

class TestLotOfDevice:
    def test_SendIPv4OnlineByPacket(self,CIDR:str)-> None:
        '''大量 IPv4 上線壓力測試非同步'''
        #產生 .0 到 .255 的 IP 數量
        iplist = iprelated.CreateIPDataByCIDROrPrifix(cidr=CIDR)
        #產生大量 MAC 從 AA0000000000 開始到 AA00000000FF ，數量由 IP 數決定
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(iplist))
        inputs = []
        for i in range(1,len(iplist)):
            inputs.append((iplist[i],maclist[i]))
        pool = Pool(14)
        pool.starmap(lan2_.SendARPReply,inputs)
        time.sleep(120) #等待 2 分鐘後透過 API 取得主機列表上線的 IP 和 MAC 資訊清單
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=Testconfig_.SiteID,isOnline=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(iplist)-1): #依序檢查是否每個 IP 和 MAC 都在清單中
            if str(iplist[i]) in onlineHostsdict :
                assert onlineHostsdict[str(iplist[i])] == maclist[i],f'{str(iplist[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(iplist[i])]}'
            else : assert False,f'It can not found IP {str(iplist[i])} in hosts as online'

    def test_SendIPv6OnlineByPacket(self,CIDR:str) -> None:
        '''大量 IPv6 上線壓力測試非同步'''
        #產生 :: 到 ::ff 的 IP 數量
        ipv6list = iprelated.CreateIPDataByCIDROrPrifix(cidr=CIDR)
        #產生大量 MAC 從 AA0000000000 開始到 AA00000000FF ，數量由 IP 數決定
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(ipv6list))
        inputs = []
        for i in range(1,len(ipv6list)):
            inputs.append((ipv6list[i],maclist[i]))
        pool = Pool(14)
        pool.starmap(lan2_.SendNA,inputs)
        time.sleep(120)#等待 2 分鐘後透過 API 取得主機列表上線的 IPv6 和 MAC 資訊
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=Testconfig_.SiteID,isOnline=True,IPv6type=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(ipv6list)-1): #依序檢查是否每個 IPv6 和 MAC 都在清單中
            if str(ipv6list[i]) in onlineHostsdict :
                assert onlineHostsdict[str(ipv6list[i])] == maclist[i],f'{str(ipv6list[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(ipv6list[i])]}'
            else : assert False,f'It can not found IPv6 {str(ipv6list[i])} in hosts as online'
    
    def test_SendOnlineOrOfflineByAPI(self,CIDR:str,VLANId:int,isOnline:bool,IPv6:bool) -> None:
        '''透過模擬 Probe 打 API 觸發上線或下線事件給 Server'''
        iplist = iprelated.CreateIPDataByCIDROrPrifix(cidr=CIDR)
        #產生大量 MAC 從 AA0000000000 開始到 AA00000000FF ，數量由 IP 數決定
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(iplist))
        for i in range(1,len(iplist)):
            AthenacCoreAPI_.SendEventOfOnorOffline(ip=str(iplist[i]),mac=str(maclist[i]),vlanID=VLANId,isonline=isOnline,isIPv6=IPv6)

#region Config
Testconfig_ = SettingConfigByTest('ConfigJson/Server_ReleaseTest.json')
lan1_ = PacketAction(Testconfig_.lan1)
lan1MACUpper_ = ''.join(lan1_.mac.upper().split(':'))
lan2_ = PacketAction(Testconfig_.lan2)
lan2MACUpper_ = ''.join(lan2_.mac.upper().split(':'))
AthenacWebAPI_ = AthenacWebAPILibry(f'https://{Testconfig_.serverIP}:8001',Testconfig_.APIaccount,base64.b64encode(Testconfig_.APIPwd.encode('UTF-8')),lan1_.Ip)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{Testconfig_.serverIP}:18000',Testconfig_.probeID,Testconfig_.daemonID,lan1_.Ip)
AthenacProbeAPI_ = AthenacProbeAPILibry(f'http://{AthenacWebAPI_.GetPortWorerkIPbyID(Testconfig_.probeID)}:18002',lan1_.Ip)

# endregion Config

if __name__ == '__main__':
    LotDeviceTest = TestLotOfDevice()
    LotDeviceTest.test_SendOnlineOrOfflineByAPI(CIDR='172.17.0.0/17',VLANId=17,isOnline=True,IPv6=False) #IPv4 上線
    LotDeviceTest.test_SendOnlineOrOfflineByAPI(CIDR='2001:b030:2133:811:ffff::/113',VLANId=17,isOnline=True,IPv6=True) #IPv6 上線
    LotDeviceTest.test_SendOnlineOrOfflineByAPI(CIDR='172.24.0.0/17',VLANId=24,isOnline=False,IPv6=False) #IPv4 下線
    LotDeviceTest.test_SendOnlineOrOfflineByAPI(CIDR='2001:b030:2133:811:ffff::/113',VLANId=17,isOnline=False,IPv6=True) #IPv6 下線

    # LotDeviceTest.test_SendIPv4OnlineByPacket(CIDR='172.17.0.0/17')
    # LotDeviceTest.test_SendIPv6OnlineByPacket(CIDR='2001:b030:2133:811:ffff::/113')
    # DHCPTest = TestDHCP()
    # DHCPTest.test_DHCPAsync(Count=50,logfile='DHCPLog.csv')
    # DHCPTest.test_DHCPv6Async(Count=2000,logfile='DHCPv6Log.csv')