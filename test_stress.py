import json,time,base64
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from NetPacketTools.packet_action_DHCPasync import PacketActionDHCPasync
from multiprocessing import Pool

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
    def test_SendIPv4Online(self)-> None:
        '''大量 IPv4 上線壓力測試非同步'''
        #產生 .0 到 .255 的 IP 數量
        iplist = iprelated.CreateIPDataByCIDROrPrifix(cidr=f'{".".join(str.split(lan2_.Ip,".")[0:2]) + ".0.0"}/24')
        #產生大量 MAC 從 AA0000000000 開始到 AA00000000FF ，數量由 IP 數決定
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(iplist))
        inputs = []
        for i in range(len(iplist)):
            inputs.append((iplist[i],maclist[i]))
        pool = Pool(14)
        pool.starmap(lan2_.SendARPReply,inputs)
        time.sleep(120) #等待 2 分鐘後透過 API 取得主機列表上線的 IP 和 MAC 資訊清單
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=SiteID_,isOnline=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(iplist)-1): #依序檢查是否每個 IP 和 MAC 都在清單中
            if str(iplist[i]) in onlineHostsdict :
                assert onlineHostsdict[str(iplist[i])] == maclist[i],f'{str(iplist[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(iplist[i])]}'
            else : assert False,f'It can not found IP {str(iplist[i])} in hosts as online'

    def test_SendIPv6Online(self) -> None:
        '''大量 IPv6 上線壓力測試非同步'''
        #產生 :: 到 ::ff 的 IP 數量
        ipv6list = iprelated.CreateIPDataByCIDROrPrifix(cidr=f'{":".join(str.split(lan2_.globalIp,":")[0:4]) + "::"}/120')
        #產生大量 MAC 從 AA0000000000 開始到 AA00000000FF ，數量由 IP 數決定
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(ipv6list))
        inputs = []
        for i in range(len(ipv6list)):
            inputs.append((ipv6list[i],maclist[i]))
        pool = Pool(14)
        pool.starmap(lan2_.SendARPReply,inputs)
        time.sleep(120)#等待 2 分鐘後透過 API 取得主機列表上線的 IPv6 和 MAC 資訊
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=SiteID_,isOnline=True,IPv6type=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(ipv6list)-1): #依序檢查是否每個 IPv6 和 MAC 都在清單中
            if str(ipv6list[i]) in onlineHostsdict :
                assert onlineHostsdict[str(ipv6list[i])] == maclist[i],f'{str(ipv6list[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(ipv6list[i])]}'
            else : assert False,f'It can not found IPv6 {str(ipv6list[i])} in hosts as online'

#region Config
with open('ConfigJson/Server_ReleaseTest.json') as f:
    settingconfig_ = json.loads(f.read())
lan1_ = PacketAction(settingconfig_['lan1'])
lan2_ = PacketAction(settingconfig_['lan2'])
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = base64.b64encode(settingconfig_['APIpwd'].encode('UTF-8'))
AthenacWebAPI_ = AthenacWebAPILibry(f'https://{serverIP_}:8001',APIaccount_,APIpwd_)
SiteID_ = settingconfig_['SiteId']
#endregion Config

if __name__ == '__main__':
    t1 = TestDHCP()
    t1.test_DHCPAsync(Count=2000,logfile='DHCPLog.csv')
    # t1.test_DHCPv6Async(Count=2000,logfile='DHCPv6Log.csv')