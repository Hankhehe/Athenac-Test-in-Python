import threading,time,json,base64,pytest_check as check
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.athenac_probe_API_libry import AthenacProbeAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule,RegisterTypebyAutoRegist
from APITools.DataModels.datamodel_apidata import BlockMessageSetting, RadiusClient, RadiusSetting,HostAgentClientInfo

class TestIPAM:
    def test_IPBlock(self)->None:
        '''IP 封鎖測試'''
        AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=True,siteid=SiteID_) #封鎖 lan2 的 IP
        time.sleep(10)
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 IP 在主機列表上線
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_) #檢查 lan2 的 IP 是否被封鎖
        ,f'The blocked {lan2_.Ip} is not receive blocked-reply of ARP while {lan2_.mac} is using {lan2_.Ip} access gateway')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 Test IP 在主機列表上線
        check.is_false(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_) #檢查 lan2 使用其它合法 IP 時是否被封鎖
        ,f'The authed {TestIPv4_} receive blocked-reply of ARP while {lan2_.mac} is using {TestIPv4_} access gateway')
        AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=False,siteid=SiteID_) #解除封鎖 lan2 的 IP

    def test_MACblock(self)->None:
        '''MAC 封鎖測試'''
        AthenacWebAPI_.BlockMAC(mac=lan2MACUpper_,block=True,siteid=SiteID_) # 封鎖 lan2 的 MAC 封鎖
        time.sleep(10)
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 IP 在主機列表上線
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_) #檢查 lan2 的 IP 是否被封鎖
        ,f'The blocked {lan2MACUpper_} is not receive blocked-reply of ARP while {lan2MACUpper_} is using {lan2_.Ip} to access to {lan2_.gatewayIp}')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 Test IP 在主機列表上線
        check.is_true(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_) #檢查 lan2 使用其它合法 IP 時是否被封鎖
        ,f'The blocked {lan2MACUpper_} is not receive blocked-reply of ARP while {lan2MACUpper_} is using {TestIPv4_} to access to {lan2_.gatewayIp}')
        lan2_.SendNA(IP=lan2_.globalIp,Count=2,WaitSec=2) #發送 NDP 確保 lan2 的 IPv6 在主機列表上線
        check.is_true(lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_) #檢查 lan2 的 IPv6 是否被封鎖
        ,f'The blocked {lan2MACUpper_} is not receive blocked-reply of NDP while {lan2MACUpper_} is using {lan2_.globalIp} to access to {lan2_.gatewatIpv6}')
        lan2_.SendNA(IP=TestIPv6_,Count=2,WaitSec=2) #發送 NDP 確保 lan2 的 Test IPv6 在主機列表上線
        check.is_true(lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_) # 檢查 lan2 使用其它合法 IPv6 時是否被封鎖
        ,f'The blocked {lan2MACUpper_} is not receive blocked-reply of NDP while {lan2MACUpper_} is using IPv6 {TestIPv6_} to access to {lan2_.gatewatIpv6}')
        AthenacWebAPI_.BlockMAC(mac=lan2MACUpper_,block=False,siteid=SiteID_) #解除 lan2 的 MAC 封鎖

    def test_ProtectIP(self)->None:
        '''固定 IP 封鎖測試'''
        AthenacWebAPI_.DelIP(ip=TestIPv4_,siteid=SiteID_) #針對 Test IP 做 IP 刪除，確保沒有其它 IP 政策
        AthenacWebAPI_.CreateProtectIP(ip=TestIPv4_,mac=lan1MACUpper_,siteid=SiteID_) #針對 Test IP 設定固定 IP 給 lan1 的 MAC
        check.is_false(lan1_.ARPBlockCheck(srcIP='0.0.0.0',dstIP=TestIPv4_,ProbeMAC=ProbeMAC_) #lan1 使用 0.0.0.0 詢問固定 IP 時，檢查是否有被封鎖
        ,f'lan1 receive blocked-reply ARP while the {lan1MACUpper_} is using 0.0.0.0 query which {TestIPv4_} if is using or not')
        check.is_true(lan2_.ARPBlockCheckforProtect(srcIP='0.0.0.0',dstIP=TestIPv4_,ProbeMAC=ProbeMAC_) # lan2 使用 0.0.0.0 詢問固定 IP 時，檢查是否有被封鎖
        ,f'lan2 is not receive blocked-reply ARP while the {lan2MACUpper_} is using 0.0.0.0 query which {TestIPv4_} if is using or not')
        check.is_true(lan2_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_) #lan2 使用固定 IP 詢問 Gateway 時，檢查是否有被封鎖
        ,f'lan2 is Not receive blocked-reply ARP while the {lan2MACUpper_} is using {TestIPv4_} access to {lan2_.gatewayIp}')
        AthenacWebAPI_.DelIP(ip=TestIPv4_,siteid=SiteID_) #針對 Test IP 做 IP 刪除，清除固定 IP 政策

    def test_BindingIP(self)->None:
        '''禁止變更 IP 封鎖測試'''
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_) #針對 lan2 的 IP 做 IP 刪除，確保沒有其他 IP 政策 
        time.sleep(5)
        AthenacWebAPI_.CreateBindingIP(ip=lan2_.Ip,siteid=SiteID_) #將 lan2 的 IP 和 MAC 設定禁止變更
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2) #lan2 使用 TestIP 發送 ARP 觸發上線來觸發禁止變更封鎖。
        check.is_true(lan2_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_) #lan2 使用 Test IP 詢問 Gatewat，檢查是否被封鎖
        ,f'lan2 is not receive blocked-reply of ARP while the {lan2MACUpper_} is using {TestIPv4_} access to {lan2_.gatewayIp} \
            during {lan2MACUpper_} binding {lan2_.Ip}')
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_) #針對 lan2 的 IP 做 IP 刪除，確保沒有其他 IP 政策 
        
        #在沒有禁止變更的情況下 lan2 使用 Test IP 詢問 Gateway 時，檢查是否被封鎖 
        check.is_false(lan1_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan1_.gatewayIp,ProbeMAC=ProbeMAC_) 
        ,f'lan2 receive blocked-reply of ARP while the {lan2MACUpper_} is using {TestIPv4_} access to {lan2_.gatewayIp} \
            during {lan2MACUpper_} is not binding {lan2_.Ip}')

    def test_UnauthMACBlock(self)->None:
        '''未授權 MAC 封鎖測試'''
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_) #開啟 Site MAC 安全模式
        AthenacWebAPI_.AuthMAC(mac=lan2MACUpper_,auth=False,siteid=SiteID_) #針對 lan2 的 MAC 取消授權
        time.sleep(10)
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 IP 在主機列表上線
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_) #lan2 使用 lan2 IP 詢問 gateway 檢查是否被封鎖
        ,f'lan2 is not receive blocked-reply of ARP while lan2 MAC is being unauthened and lan2 is using {lan2_.Ip} access gateway')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2) #因 lan2 沒有這個 IP，所以 lan2 使用 Test IP 發送 ARP 觸發上線
        check.is_true(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_) #lan2 使用 Test IP 詢問 gateway 檢查是否被封鎖
        ,f'lan2 is not receive blocked-reply of ARP while lan2 MAC is being unauthened and lan2 is using {TestIPv4_} access gateway')
        lan2_.SendNA(IP=lan2_.globalIp,Count=2,WaitSec=2) #發送 NDP 確保 lan2 的 IPv6 在主機列表上線
        check.is_true(lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_) #lan2 使用 lan2 IPv6 詢問 gateway 檢查是否被封鎖
        ,f'lan2 is not receive blocked-reply of NDP while lan2 MAC is being unauthened and lan2 is using {lan2_.globalIp} access gateway')
        lan2_.SendNA(IP=TestIPv6_,Count=2,WaitSec=2) #因 lan2 沒有這個 IPv6，所以 lan2 使用 Test IPv6 發送 NDP 觸發上線
        check.is_true(lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_) #lan2 使用 Test IPv6 詢問 gateway 檢查是否被封鎖
        ,f'lan2 is not receive blocked-reply of NDP while lan2 MAC is being unauthened and lan2 is using {TestIPv6_} access gateway')
        AthenacWebAPI_.AuthMAC(mac=lan2MACUpper_,auth=True,siteid=SiteID_) #針對 lan2 的 MAC 做 MAC 授權
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_) #關閉 Site MAC 安全模式

    def test_UnauthIPBlock(self)->None:
        '''未授權 IP 封鎖'''
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=True,siteid=SiteID_) #開啟 Site IP 安全模式
        AthenacWebAPI_.AuthIPv4(ip=lan2_.Ip,auth=False,siteid=SiteID_) #針對 lan2 的 IP 做 IP 取消授權
        time.sleep(10)
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2) #發送 ARP 確保 lan2 的 IP 在主機列表上線
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_) #lan2 使用 lan2 IP 詢問 gateway 時，檢查是否被封鎖
        ,f'lan2 is not receive blocked-replt of ARP while lan2 is using {lan2_.Ip} access gateway but {lan2_.Ip} is authed')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2) #因 lan2 沒有 Test IP 所以 lan2 使用 Test IP 發送 ARP 觸發上線
        check.is_false(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_) #lan2 使用 Test IP 詢問 gateway，檢查是否被封鎖
        ,f'lan2 receive blocked-reply of ARP while lan2 is using {TestIPv4_} access gateway but {TestIPv4_} is not unauthened')
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=False,siteid=SiteID_)

    def test_UserApply(self)->None:
        '''透過封鎖畫面做授權的測試'''
        def CheckAuth(account:str,encryptpwd:str,authtype:int,auth:bool) -> None:
            '''AuthType 1 = AD, DB = 2, LDAP = 3'''
            messagetype = ''
            if authtype == 1 : messagetype = 'AD' 
            elif authtype == 2 : messagetype = 'DB' 
            elif authtype == 3 : messagetype = 'LDAP' 
            AthenacCoreAPI_.AuthMACFromUserApply(lan2_.Ip,lan2MACUpper_,account,encryptpwd)
            MACdata =  AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_) #取得 lan2 MAC 的狀態
            if not MACdata : 
                #當無法透過 API 取得 lan2 MAC 資料時就跳錯
                check.is_true(False,f'can not queried {lan2MACUpper_} Detail while verify by {messagetype}')
            elif auth:
                #檢查 lan2 的 MAC 的授權狀態是為授權 
                check.is_true(MACdata['IsRegisteded'] == 1,f'{lan2MACUpper_} result is unauthed but {lan2MACUpper_} has authed by {messagetype}')
                #檢查 lan2 的 MAC 的 Register ID 是否為認證通過的帳號
                check.is_true(MACdata['RegisterUserId'] == account,f'{lan2MACUpper_} registered ID is not {account},it is {MACdata["RegisterUserId"]}')
            elif not auth:
                #檢查 lan2 的 MAC 的授權狀態是為授權 
                check.is_true(MACdata['IsRegisteded'] == 0,f'{lan2MACUpper_} result is authed but {lan2MACUpper_} has not authed by {messagetype}')
            else: check.is_true(False,'Unknow error')

        blockmessagesetting = BlockMessageSetting(EnableBlockNotify=True,EnableVerifyModule=True,ADverify=True,DBverify=True,LDAPverify=True)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_) #開啟 Site MAC 安全模式
        AthenacWebAPI_.UpdateBlockMessage(config=blockmessagesetting,siteid=SiteID_) #設定封鎖訊息&驗證方式

        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_) #取消授權 lan2 的 MAC
        CheckAuth(account='Hank',encryptpwd='sDPuXGCV1zAEjGFN0qL+lg==',authtype=1,auth=False) #使用 AD 帳號但錯的密碼做授權 lan2 MAC, Hank errorpwd
        CheckAuth(account='Hank',encryptpwd='QkIHIDPyeiIALps4IKGH+w==',authtype=1,auth=True) #使用 AD 帳號授權 lan2 MAC, Hank
        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_)
        CheckAuth(account='admin',encryptpwd='sDPuXGCV1zAEjGFN0qL+lg==',authtype=2,auth=False) #使用 DB 帳號但錯的密碼做授權 lan2 MAC, admin errorpwd
        CheckAuth(account='admin',encryptpwd='36IqJwCHVwl9IS4w4b1mMw==',authtype=2,auth=True) #使用 DB 帳號授權 lan2 MAC,  admin admin
        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_)
        CheckAuth(account='RAJ',encryptpwd='sDPuXGCV1zAEjGFN0qL+lg==',authtype=3,auth=False) #使用 AD 帳號但錯的密碼做授權 lan2 MAC, RAJ errorpwd
        CheckAuth(account='RAJ',encryptpwd='AgRAu+JjydaLEw3me8kTxA==',authtype=3,auth=True) #使用 DB 帳號授權 lan2 MAC,  RAJ 111aaaBBB
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_) # 關閉 Site MAC 安全模式

class TestAutoRegist:
    def test_HostAgent(self)->None:
        '''模擬 Agent 發送假資料給 Server 測試 Server 功能'''
        def CheckAuth(authtype:int,auth:bool) -> None:
            '''type 1 = it join domain and AD is loging
            type 2 = is not join domain and local account login
            type 3 = agent no response'''
            messagetype = ''
            if authtype == 1: messagetype ='join domain and AD is loging'
            elif authtype == 2 : messagetype ='is not join domain and local account login'
            elif authtype == 3 : messagetype = 'no response of agent'
            MACData = AthenacWebAPI_.GetMACDetail(lan2_.mac,SiteId=SiteID_) #取得 lan2 MAC 的相關資訊
            if not MACData:
                #當無法透過 API 取得 lan2 MAC 資料時就跳錯
                check.is_true(False,f'can not queried {lan2MACUpper_} Detail while {lan2MACUpper_} is {messagetype}')
            elif auth :
                #檢查 lan2 MAC 的授權狀態是否為 True
                check.is_true(MACData['IsRegisteded'],f'{lan2MACUpper_} registered status is unauthened while {lan2MACUpper_} is {messagetype}')
                #檢查 lan2 MAC 的授權型態是否為網域自動授權(此型態會讓 MAC 變藍色)
                check.is_true(MACData['RegisterType'] == 3,f'{lan2MACUpper_} registered type is not AD while {lan2MACUpper_} is {messagetype}' )
            elif not auth:
                check.is_false(MACData['IsRegisteded'],f'{lan2MACUpper_} registeerd status is authened while {lan2MACUpper_} is {messagetype}')
                #檢查 lan2 MAC 的授權型態是否為預設值
                check.is_true(MACData['RegisterType'] == 0,f'{lan2MACUpper_} registered type is not default while {lan2MACUpper_} is {messagetype}')
            else: check.is_true(False,'Unknow error')

        def SendAgentInfo(domain:str,account:str) -> None:
            AthenacProbeAPI_.SendInfoToProbeByAPI(HostAgentClientInfo(hostName='TestMachine',macs=[lan2MACUpper_],domainname=domain
            ,logonusers=[{'logonAccount':account,'remoteLogin':False,'gpoResult':None}]
            ,ostype='windows',osdesc='Windows Test'))

        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_) #開啟 Site MAC 安全模式
        AthenacWebAPI_.UpdateAutoRegister(registtype=RegisterTypebyAutoRegist.VBS.value,siteid=SiteID_) #啟用 AD 自動授權 by VBS 驗證
        AthenacWebAPI_.ClearAllDomainServerforAutoRegist(siteid=SiteID_) #清除所有自動授權內的 AD Server IP 資訊，確保環境乾淨
        AthenacWebAPI_.AddDomainServerforAutoRegist(domainname='PIXIS',ip='192.168.10.201',siteid=SiteID_) #新增 PIXIS 公司的 AD IP 和網域名稱
        AthenacWebAPI_.DelMAC(mac=lan2_.mac,siteid=SiteID_) #刪除 lan2 MAC，刪除該 MAC 所有的網域群組等資訊
        lan2_.SendARPReply(lan2_.Ip,Count=10,WaitSec=1) #lan2 使用 lan2 IP 發送 ARP 確保主機列表有上線

        #模擬 Agent 發送 lan2 的 MAC 和網域群組名稱以及 AD 帳號登入中的資訊給 Server
        SendAgentInfo(domain='PIXIS',account='PIXIS\\Hank')
        time.sleep(50) #因 Server 收到後要一段時間才會授權所以進行等待
        CheckAuth(authtype=1,auth=True) #檢查 lan2 的狀態是否為授權且授權型態是否為 3

        #模擬 Agent 發送 lan2 的 MAC 和 WORKGROUP 的網域群組以及本機帳號登入中的資訊給 Server
        SendAgentInfo(domain='WORKGROUP',account='Local\\User')
        time.sleep(50)
        CheckAuth(authtype=2,auth=False) #檢查 lan2 的狀態是否為未授權且授權型態是否為 0

        #因要測試已被自動授權的電腦在移除 Agent 的情況下上線後經過兩分鐘後是否會自動取消授權，所以需要先發送已加入網域且 AD 帳號登入中的資訊讓 Server 自動授權此 MAC。
        SendAgentInfo(domain='PIXIS',account='PIXIS\\Hank')
        time.sleep(50)
        CheckAuth(authtype=1,auth=True)
        AthenacWebAPI_.DelIP(lan2_.Ip,siteid=SiteID_) #刪除 lan2 的 IP 來觸發重新上線
        lan2_.SendARPReply(lan2_.Ip,Count=10,WaitSec=1) #lan2 使用 lan2 IP 發送 ARP 觸發上線確保主機列表有資料
        time.sleep(60*4) #因自動取消授權要等 2 兩分鐘，所以這邊等 4 分鐘，因為怕 Server 太忙。
        CheckAuth(authtype=3,auth=False) #檢查 lan2 的狀態是否為未授權且授權型態是否為 0
        AthenacWebAPI_.UpdateAutoRegister(registtype=RegisterTypebyAutoRegist.Closed.value,siteid=SiteID_) #關閉 AD 自動授權
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_) #關閉 Site MAC 安全模式

class TestPreCheck:
    def test_HotfixKBbyVBSandPrecheckWhite(self)->None:
        '''未安裝 Windows Hotfix KB 編號的符規規則測試'''
        AthenacWebAPI_.ClearAllPrecheckRule() #清除所有未符規的規則
        AthenacWebAPI_.CreateUnInstallKBforPrecheckRule(siteid=SiteID_,KBNumbers=[123456]) #設定符規規則且指定要安裝的 KB 檔編號是 123456
        #模擬 Agent 發送資訊給 Server，lan2 的 MAC 未安裝的 KB 編號為 123456
        AthenacProbeAPI_.SendInfoToProbeByAPI(HostAgentClientInfo(hostName='TestMachine',macs=[lan2MACUpper_],domainname='PIXIS'
        ,logonusers=[{'logonAccount':'PIXIS\\Hank','remoteLogin':False,'gpoResult':None}]
        ,ostype='windows',osdesc='Windows Test',pendinghotfix=[f'Hotfix 123456 - KB123456']))
        time.sleep(20) #等待 20 秒，因為 Server 可能需要時間判斷
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_) #針對 lan2 的 IP 做 IP 刪除，因為要觸發上線才會觸發未符規封鎖
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2) #lan2 使用 lan2 的 IP 發送 ARP，確保主機列表有上線
        check.is_true(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_) # 檢查未符規設備 lan2 是否有被封鎖
        ,f'{lan2MACUpper_} is not receive blocked-reply of ARP while {lan2MACUpper_} is not passing pre-check')
        AthenacWebAPI_.SetPrecheckWhiteMAC(mac=lan2_.mac,white=True,siteid=SiteID_) #設定 lan2 的 MAC 為未符規白名單
        time.sleep(2)
        check.is_false(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_) #檢查 lan2 在未符規白名單情況下是否被封鎖
        ,f'{lan2MACUpper_} receive blocked-reply of ARP while {lan2MACUpper_} is white list of precheck')
        
        #以下測試情境是模擬 Agent 發送非未符規規則指定要安裝的 KB 檔編號時是否會被放行
        AthenacWebAPI_.SetPrecheckWhiteMAC(mac=lan2_.mac,white=False,siteid=SiteID_) #針對 lan2 的 MAC 做取消未符規白名單
        #發送立即檢查符規規則來確保 lan2 的 MAC 是被封鎖的，因為 lan2 目前的資料 KB 還是 123456
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
        time.sleep(2)
        check.is_true(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_)
        ,f'{lan2MACUpper_} is not receive blocked-reply of ARP while {lan2MACUpper_} is not passing pre-check')
        #模擬 Agent 發送資訊給 Server，lan2 的 MAC 未安裝的 KB 編號為 666666
        AthenacProbeAPI_.SendInfoToProbeByAPI(HostAgentClientInfo(hostName='TestMachine',macs=[lan2MACUpper_],domainname='PIXIS'
        ,logonusers=[{'logonAccount':'PIXIS\\Hank','remoteLogin':False,'gpoResult':None}]
        ,ostype='windows',osdesc='Windows Test',pendinghotfix=[f'Hotfix 666666 - KB666666']))
        time.sleep(20)
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
        time.sleep(2)
        check.is_false(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_)
        ,f'{lan2MACUpper_} receive blocked-reply of ARP while {lan2MACUpper_} is passed of pre-check')
        AthenacWebAPI_.ClearAllPrecheckRule()
    
    def test_HotfixbyVBS(self)->None:
        '''超過時間未檢查 Hotfix 和未安裝的 hotfix 數量超過罰值的符規規則測試'''
        AthenacWebAPI_.ClearAllPrecheckRule() #清除所有未符規規則，確保環境乾淨
        #設定未符規規則:更新時間要在 15 天內，或 hotfix 數量等於 0
        AthenacWebAPI_.CreateHotfixforPrecheckRule(siteid=SiteID_,hotfixcount=0,checkday=15)

        #取得符規規則的 ID ，透過未符規設備清單中的 MAC 來判定是否有被封鎖
        prechecklist = AthenacWebAPI_.GetPrecheckRuleList()
        if prechecklist:
            precheckid = prechecklist[0]['Id']
        else:
            check.is_true(False,'Create fail at Precheckrule') 
            return
        #發送 lan2 MAC 的資訊： Hotfix 檢查時間是一個月前，且有一個 hotfix 未安裝來觸發未符規
        checkdate = time.strftime('%Y/%m/%d'+' '+'%H:%M:%S',time.gmtime(time.time()-(60*60*24*30)))
        AthenacProbeAPI_.SendInfoToProbeByAPI(HostAgentClientInfo(hostName='TestMachine',macs=[lan2MACUpper_],domainname='PIXIS'
        ,logonusers=[{'logonAccount':'PIXIS\\Hank','remoteLogin':False,'gpoResult':None}]
        ,ostype='windows',osdesc='Windows Test',pendinghotfix=[f'Hotfix 123456 - KB123456'],windowshotfixlastchecktime=checkdate))
        time.sleep(20)
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_) #透過發送 API 來執行 lan2 的 MAC 立即檢查未符規

        #取得指定符規規則裡的未符規設備清單
        illegaldevices =  AthenacWebAPI_.GetPrecheckDevice(precheckid=precheckid)
        checkflag = False
        for illegaldevice in illegaldevices:
            if illegaldevice['Mac'] == lan2MACUpper_ and illegaldevice['SiteId'] == SiteID_:
                checkflag = True
        #判斷 lan2 的 MAC 是否有出現在未符規設備清單中
        check.is_true(checkflag
        ,f'{lan2MACUpper_} is not on illegal list while {lan2MACUpper_} hotfix check time is over 1 month and it pending hotfix count over 0')
        #發送 lan2 MAC 的資訊： Hotfix 檢查時間是當下，且有 0 個需要更新的 hotfix 來觸發符規
        AthenacProbeAPI_.SendInfoToProbeByAPI(HostAgentClientInfo(hostName='TestMachine',macs=[lan2MACUpper_],domainname='PIXIS'
        ,logonusers=[{'logonAccount':'PIXIS\\Hank','remoteLogin':False,'gpoResult':None}]
        ,ostype='windows',osdesc='Windows Test'))
        time.sleep(20)
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_) #透過發送 API 來執行 lan2 的 MAC 立即檢查未符規
        illegaldevices =  AthenacWebAPI_.GetPrecheckDevice(precheckid=precheckid) 
        checkflag = False
        for illegaldevice in illegaldevices:
            if illegaldevice['Mac'] == lan2MACUpper_ and illegaldevice['SiteId'] == SiteID_:
                checkflag = True
        check.is_false(checkflag
        ,f'{lan2MACUpper_} is on illegal list while {lan2MACUpper_} hotfix check time is now and it pending hotfix is 0')
        AthenacWebAPI_.ClearAllPrecheckRule()

class TestAutoRegist:
    def test_HostAgent(self)->None:
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.UpdateAutoRegister(registtype=RegisterTypebyAutoRegist.VBS.value,siteid=SiteID_)
        AthenacWebAPI_.ClearAllDomainServerforAutoRegist(siteid=SiteID_)
        AthenacWebAPI_.AddDomainServerforAutoRegist(domainname='PIXIS',ip='192.168.10.201',siteid=SiteID_)
        AthenacWebAPI_.DelMAC(mac=lan2_.mac,siteid=SiteID_)
        lan2_.SendARPReply(lan2_.Ip,Count=3,WaitSec=1)
        time.sleep(10)
        AthenacCoreAPI18002_.SendHostUserbyAgent(mac=lan2_.mac,domainname='PIXIS',remotetype=False,sendtype=SendHostAgentType.Login.value)
        MACData = AthenacWebAPI_.GetMACDetail(lan2_.mac,SiteId=SiteID_)
        if MACData :
            check.is_true(MACData['IsRegisteded'],f'this MAC {lan2_.mac} register is not true, when loging by used AD account')
            check.is_true(MACData['RegisterType'] == 3,f'this MAC {lan2_.mac} register type is not AD, when loging by used AD account' )
        AthenacWebAPI_.DelIP(lan2_.Ip,siteid=SiteID_)
        time.sleep(60*4)
        MACData = AthenacWebAPI_.GetMACDetail(lan2_.mac,SiteId=SiteID_)
        if MACData :
            check.is_false(MACData['IsRegisteded'],f'This MAC {lan2_.mac} register is not false, when IP start before 2 min')
            check.is_true(MACData['RegisterType'] == 0,f'this MAC {lan2_.mac} register type is not default, when ip start before 2 min' )
        AthenacCoreAPI18002_.SendHostUserbyAgent(mac=lan2_.mac,domainname='PIXIS',remotetype=False,sendtype=SendHostAgentType.UnblockCRequest.value)
        MACData = AthenacWebAPI_.GetMACDetail(lan2_.mac,SiteId=SiteID_)
        if MACData :
            check.is_true(MACData['IsRegisteded'],f'this MAC {lan2_.mac} register is not true,when login by used AD account after removed auto regist')
            check.is_true(MACData['RegisterType'] == 3,f'this MAC {lan2_.mac} register type is not AD,when login by used AD account after removed auto regist' )
        AthenacCoreAPI18002_.SendHostUserbyAgent(mac=lan2_.mac,domainname='Local',remotetype=False,sendtype=SendHostAgentType.Login.value)
        MACData = AthenacWebAPI_.GetMACDetail(lan2_.mac,SiteId=SiteID_)
        if MACData:
            check.is_false(MACData['IsRegisteded'],f'This MAC {lan2_.mac} register is not false, when loging by used local account')
            check.is_true(MACData['RegisterType'] == 0,f'This MAC {lan2_.mac} regist type is not default, when loging by used local account' )
        AthenacWebAPI_.UpdateAutoRegister(registtype=RegisterTypebyAutoRegist.Closed.value,siteid=SiteID_)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)

class TestPreCheck:
    def test_HotfixKBbyVBSandPrecheckWhite(self)->None:
        AthenacWebAPI_.ClearAllPrecheckRule()
        AthenacWebAPI_.CreateUnInstallKBforPrecheckRule(siteid=SiteID_,KBNumbers=[123456])
        AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[123456])
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_)
        lan2_.SendARPReply(IP=lan2_.Ip,Count=2,WaitSec=2)
        check.is_true(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_),f'Not recived ARP Block at MAC: {lan2_.Ip} from hotfix VBS')
        AthenacWebAPI_.SetPrecheckWhiteMAC(mac=lan2_.mac,white=True,siteid=SiteID_)
        time.sleep(2)
        check.is_false(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_),f'Recived ARP Block at MAC: {lan2_.Ip} from hotfix VBS white')
        AthenacWebAPI_.SetPrecheckWhiteMAC(mac=lan2_.mac,white=False,siteid=SiteID_)
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
        time.sleep(2)
        check.is_true(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_),f'Not recived ARP Block at MAC: {lan2_.Ip} from hotfix VBS')
        AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[666666])
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
        time.sleep(2)
        check.is_false(lan2_.ARPBlockCheck(srcIP=lan2_.Ip,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_),f'Recived ARP Block at MAC {lan2_.Ip} from hotfix VBS')
        AthenacWebAPI_.ClearAllPrecheckRule()
    
    def test_HotfixbyVBS(self)->None:
        AthenacWebAPI_.ClearAllPrecheckRule()
        AthenacWebAPI_.CreateHotfixforPrecheckRule(siteid=SiteID_,hotfixcount=0,checkday=15)
        prechecklist = AthenacWebAPI_.GetPrecheckRuleList()
        if prechecklist:
            precheckid = prechecklist[0]['Id']
        else:
            check.is_true(False,'Create fail at Precheckrule') 
            return
        checkdate = time.strftime('%Y/%m/%d'+' '+'%H:%M:%S',time.gmtime(time.time()-(60*60*24*30)))
        AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[123456],checktime=checkdate)
        AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
        illegaldevices =  AthenacWebAPI_.GetPrecheckDevice(precheckid=precheckid)
        checkflag = False
        for illegaldevice in illegaldevices:
            if illegaldevice['Mac'] == lan2MACUpper_ and illegaldevice['SiteId'] == SiteID_:
                checkflag = True
        check.is_true(checkflag,f'The MAC {lan2_.mac} is not illegalDevice by Precheck on Check Date')
        AthenacWebAPI_.ClearAllPrecheckRule()

class TestAbnormalDevice:
    def test_IPconflict(self)->None:
        '''IP 衝突測試'''
        checkv4 = False
        checkv6 = False
        for i in range(10): #使用 lan1 和 lan2 的 MAC 稱圖 test IP 和 test IPv6 ，發送 10 次每次等待 2 秒
            lan1_.SendARPReply(TestIPv4_)
            lan2_.SendARPReply(TestIPv4_)
            lan1_.SendNA(TestIPv6_)
            lan2_.SendNA(TestIPv6_)
            time.sleep(2)
        time.sleep(10)
        IPconflictdevices = AthenacWebAPI_.GetIPconflictDeviceList() #透過 API 取得 IP 衝突列表的資訊
        for IPconflictdevice in IPconflictdevices: # 檢查 IP 衝突列表中的資訊是否有 Test IP 和 Test IPv6 的資訊
            if IPconflictdevice['Ip'] == TestIPv4_ and lan1MACUpper_ in IPconflictdevice['Macs'] and lan2MACUpper_ in IPconflictdevice['Macs']:checkv4 = True; continue
            if IPconflictdevice['Ip'] == TestIPv6_ and lan1MACUpper_ in IPconflictdevice['Macs'] and lan2MACUpper_ in IPconflictdevice['Macs']:checkv6 = True; continue
        check.is_true(checkv4,f' IPconflictTestCase {TestIPv4_}')
        check.is_true(checkv6,f' IPconflictTestCase {TestIPv6_}')
            
    def test_OutofVLAN(self)->None:
        '''超出管理範圍測試 IPv4'''
        checkflag = False
        lan1_.SendARPReply('10.1.1.87') #在 lan1 所屬的 VLAN 發送 ARP 廣播觸發 10.1.1.87 上線
        time.sleep(10)
        outofVLANDevices = AthenacWebAPI_.GetOutofVLANList() #透過 API 取得超出管理範圍清單
        for outofVLANDevice in outofVLANDevices: #檢查清單中是否有 10.1.1.87 且 MAC 是 lan1 的資訊
            if outofVLANDevice['Ip'] == '10.1.1.87' and outofVLANDevice['Mac'] == lan1MACUpper_: checkflag = True; break
        check.is_true(checkflag,' OutofVLANTestCase IP: 10.1.1.87')

    def test_UnknowDHCP(self)->None:
        '''未知的 IP 派發來源測試'''
        lan1_.SendDHCPv4Offer() #使用 lan1 的 IP 觸發未知的 DHCPv4
        lan1_.SendDHCPv6Advertise() #使用 lan1 的 linklocal IP 觸發 DHCPv6
        lan1_.SendRA() #使用 lan1 的 global IP 觸發 SLAAC Stateless 
        time.sleep(10)
        unknowDHCPList = AthenacWebAPI_.GetUnknowDHCPList() #透過 API 取得未知的 IP 派發來源清單資訊
        checkDHCPv4 = False
        checkDHCPv6 = False
        checkSLAAC = False
        for unknowDHCP in unknowDHCPList:
            #檢查清單中是否有 lan1 的 IP 和 MAC 且形態是未知的 DHCPv4
            if unknowDHCP['Ip'] == lan1_.Ip and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 1: checkDHCPv4 = True; continue
            #檢查清單中是否有 lan1 的 Linklocal IP 和 MAC 且形態是未知的 DHCPv6
            if unknowDHCP['Ip'] == lan1_.linklocalIp and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 1: checkDHCPv6 = True; continue
            #檢查清單中是否有 lan1 的 Global IP 和 MAC 且形態是未知的 SLAAC
            if unknowDHCP['Ip'] == lan1_.globalIp and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 2:checkSLAAC=True; continue
        check.is_true(checkDHCPv4,' UnknowDHCPTestCase DHCPv4')
        check.is_true(checkDHCPv6,' UnknowDHCPTestCase DHCPv6')
        check.is_true(checkSLAAC,' UnknowDHCPTestCase SLAAC')

    def test_Broadcast(self)->None:
        '''ARP 的廣播超量測試'''
        checkfalg = False
        lan1_.SendARPReply(IP= lan1_.Ip,Count= 1000) #使用 lan1 的 IP 和 MAC 發送 1000 包 ARP reply廣播
        time.sleep(120) #因 Server 需要兩分鐘做平均所以等待
        borDevices = AthenacWebAPI_.GetBrocastDeviceList() #取得廣播超量的資訊清單
        for borDevice in borDevices: #檢查清單中是否有 lan1 的 IP 和 MAC
            if borDevice['Ip'] == lan1_.Ip and borDevice['Mac'] == lan1MACUpper_: checkfalg = True; break
        check.is_true(checkfalg,f' BrocastcastTest {lan1_.Ip}')
 
    def test_Multcast(self)->None:
        '''NDP 的群播超量測試'''
        checkflag = False
        lan1_.SendNA(IP= lan1_.globalIp,Count= 1000) #使用 lan1 的 Global IP 和 MAC 發送 1000 包 NDP Adver 群播
        time.sleep(120) #因 Server 需要兩分鐘做平均所以等待
        mutidevices = AthenacWebAPI_.GetMulicastDeviceList() #取得群播超量的資訊清單
        for mutidevice in mutidevices: #檢查清單中是否有 lan1 的 Global IP 和 MAC
            if mutidevice['Ip'] == lan1_.globalIp and mutidevice['Mac'] == lan1MACUpper_: checkflag = True; break
        check.is_true(checkflag,f' MultcastTestCase {lan1_.globalIp}')

class TestRadius:
    def test_Radius8021X(self)->None:
        '''802.1X MAC Base 驗證測試'''
        radiusset = RadiusSetting(SiteId=SiteID_,EnableDynamicVLAN=False) 
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=AuthAVPID_) 
        AthenacWebAPI_.UpdateRadiusSetting(radiusset) #啟用 802.1X 功能
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_) #清除測試 Site 的所有 Radius Client，確保環境乾淨
        AthenacWebAPI_.AddRadiusClient(radiusclientset) #設定 Radius Client ，AVP 是 802.1X Auth ，IP 0.0.0.0
        AthenacWebAPI_.SwitchSiteMonitMode(enable=True,siteid=SiteID_) #開啟 Site 監看模式，因沒有要測封鎖，只測收到的 802.1X Radius 封包來判斷
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_) #開啟 Site MAC 安全模式
        AthenacWebAPI_.AuthMAC(mac=lan1MACUpper_,auth=False,siteid=SiteID_) #透過 API 針對 lan1 的 MAC 做取消 MAC 授權
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip) #透過 lan1 發送 802.1X request 並取得 reply 的狀態(accept or reject)
        if radiuscode:
            radiuscode =radiuscode['RadiusCode']
        check.is_true(radiuscode == 3,f'The {lan1MACUpper_} of unauthed radius code is not 3, it is {radiuscode}') #檢查未授權的 MAC 是否收到 Reject
        AthenacWebAPI_.AuthMAC(mac=lan1MACUpper_,auth=True,siteid=SiteID_) #針對 lan1 的 MAC 做 MAC 授權
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if radiuscode:
            radiuscode =radiuscode['RadiusCode']
        check.is_true(radiuscode == 2,f'The {lan1MACUpper_} of authed radius code is not 2, it is {radiuscode}') #檢查授權 MAC 是否收到 Accept
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_) #關閉 Site 監看模式
        AthenacWebAPI_.SwitchSiteMonitMode(enable=False,siteid=SiteID_) #關閉 Site MAC 安全模式
        radiusset.EnableRadius = False 
        AthenacWebAPI_.UpdateRadiusSetting(radiusset) #關閉 802.1X 功能

    def test_RadiusDynamicVLAN(self)->None:
        '''802.1X MAC Base 驗證加動態 VLAN for 內外部預設 VLAN 與 VLAN 對應表測試'''
        def CheckVLANID(VLANID:int,statustype:int)->None:
            message = ''
            if statustype ==1 : message = 'not on the VLAN mapping list'
            elif statustype ==2 : message = 'on the VLAN mapping list'
            elif statustype == 3 : message = 'on the VLAN mapping list and setting mapping VLAN ID'
            radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip) #透過 lan1 發送 Radius request，並取得 Radius 回復的資訊
            if not radiusresult :
                check.is_true(False,f'Does not receive radius reply while {lan1MACUpper_} is {message}')
            else : 
                check.is_true(radiusresult['VLANId'] == str(VLANID) #檢查 lan1 的 MAC 收到的 VLAN ID 是否在預期中
                ,f'{lan1MACUpper_} receive unexpected VLAN {radiusresult["VLANId"]} !! , expected VLAN ID is {VLANID} while it is {message}')

        dynamicset = RadiusSetting(SiteId=SiteID_)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=DynamicAVPID_)
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset) #啟用 802.1X 和動態 VLAN 功能
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_) #清除所有 Radius Client，確保環境乾淨
        AthenacWebAPI_.AddRadiusClient(radiusclientset) #設定 Radius Client ，AVP 是 802.1X Dynamic ，IP 0.0.0.0
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_) #將 lan1 的 MAC 從 VLAN 對應表中刪除，確保環境乾淨
        CheckVLANID(VLANID=dynamicset.ExternalDefaultVLan,statustype=1)

        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_) #將 lan1 的 MAC 加進 VLAN 對應表中
        CheckVLANID(VLANID=dynamicset.InternalDefaultVLan,statustype=2)
        #將 lan1 的 MAC 加進 VLAN 對應表中且設定 VLAN ID 為 VLAN Mapping VLAN ID
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,VLANIDMapping_,SiteID_) 
        CheckVLANID(VLANID=VLANIDMapping_,statustype=3)

        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_) #將 lan1 在 VLAN 對應表中刪除，做環境清除
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset) # 關閉動態 VLAN 和 802.1X 功能

    def test_RadiusCoAbyQuar(self)->None:
        '''802.1X MAC Base 驗證加動態 VLAN for 內外部預設 VLAN 隔離 VLAN 測試'''
        def Check_CoA_and_VLANID(VLANID:int,message:str) -> None:
            if not listens.radiuspackets: #檢查是否有收到 CoA 封包
                check.is_true(False,f'not receive CoA Packet from {message}')
            else: listens.radiuspackets.clear() #如果有 CoA 封包的話清除資料，已準備下次測試檢查使用
            lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip) #lan1 透過 radius request 取得 VLAN ID
            if not lan1replyvlanid:
                check.is_true(False,f'not receive radius reply from {message}')
            else:
                check.is_true(lan1replyvlanid['VLANId'] == str(VLANID) #檢查取得的 VLAN ID 是否與預期的一樣
                ,f'{lan1MACUpper_} receive unexpected VLAN ID {lan1replyvlanid} !!,expected VLAN ID is {VLANID} from {message}')

        dynamicset = RadiusSetting(SiteId=SiteID_,SiteVerifyModule=SiteVerifyModule.EnableDbVerify.value,EnableInternalAutoQuarantine=True
        ,EnableExternalAutoQuarantine=True)
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset) #啟用 802.1X 和動態 VLAN 並開啟內外部隔離 VLAN 功能
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_) #清除所有 Radius Client 確保環境乾淨
        AthenacWebAPI_.ClearAllMappingatSite(siteid=SiteID_) #清除所有 VLAN Mapping 資料，確保環境乾淨
        AthenacWebAPI_.AddRadiusClient(RadiusClient(SiteId=SiteID_,RadiusAVPId=DynamicAVPID_)) #設定 Radius Client ，AVP 是 802.1X Dynamic ，IP 0.0.0.0
        listens = PacketListenFromFilter(lan1_.nicname) 
        CoAPacketCheck = threading.Thread(target=listens.Sniffer,args=['udp and port 3799',60*15]) #透過 lan1 開啟封包監聽 15 分鐘並只聽 UDP 3799(CoA 封包)
        CoAPacketCheck.start() #開始監聽
        lan1replyvlanid = lan1_.GetRadiusReply(serverip= serverIP_,nasip=lan1_.Ip) #lan1 的 MAC 不在 VLAN 對應表中所以要取得外部預設 VLAN ID
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalDefaultVLan)
        ,f' receive not VLAN ID {dynamicset.ExternalDefaultVLan} is VLAN ID {lan1replyvlanid} from External Default VLAN')

        lan1_.SendDHCPv4Offer() #lan1 發送未知的 DHCP，觸發 CoA 以及會取得外部隔離的 VLAN ID
        time.sleep(10)
        Check_CoA_and_VLANID(VLANID=dynamicset.ExternalQuarantineVLan,message='External Quarantine VLAN by DHCPv4')

        lan1_.SendDHCPv6Advertise() #lan1 發送未知的 DHCPv6，觸發 CoA 以及會取得外部隔離的 VLAN ID
        time.sleep(10)
        Check_CoA_and_VLANID(VLANID=dynamicset.ExternalQuarantineVLan,message='External Quarantine VLAN by DHCPv6')

        lan1_.SendARPReply(IP=lan1_.Ip,Count=1000) #lan1 發送 ARP 觸發廣播超量，觸發 CoA 以及會取得外部隔離的 VLAN ID
        time.sleep(140)
        Check_CoA_and_VLANID(VLANID=dynamicset.ExternalQuarantineVLan,message='External Quarantine VLAN by Broadcast')

        lan1_.SendNA(IP=lan1_.globalIp,Count=1000) #lan1 發送 NDP 觸發群播播超量，觸發 CoA 以及會取得外部隔離的 VLAN ID, 跳過此測試因為此功能未做完
        time.sleep(140)
        # Check_CoA_and_VLANID(VLANID=dynamicset.ExternalQuarantineVLan,message='External Quarantine VLAN by Muticast')

        #將 lan1 的 MAC 加入 LAN 對應表，讓 lan1 的 MAC 變成內部設備
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_)
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip) #lan1 的 MAC 已在 VLAN 對應表中所以要取得內部預設 VLAN ID
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalDefaultVLan)
        ,f' receive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {lan1replyvlanid} from Internal Default VLAN')
        lan1_.SendDHCPv4Offer() #lan1 發送未知的 DHCP，觸發 CoA 以及會取得內部隔離的 VLAN ID
        time.sleep(10)
        Check_CoA_and_VLANID(VLANID=dynamicset.InternalQuarantineVLan,message='Internal Quarantine VLAN by DHCPv4')

        lan1_.SendDHCPv6Advertise() #lan1 發送未知的 DHCPv6，觸發 CoA 以及會取得內部隔離的 VLAN ID
        time.sleep(10)
        Check_CoA_and_VLANID(VLANID=dynamicset.InternalQuarantineVLan,message='Internal Quarantine VLAN by DHCPv6')

        lan1_.SendARPReply(IP= lan1_.Ip,Count= 1000) #lan1 發送 ARP 觸發廣播超量，觸發 CoA 以及會取得內部隔離的 VLAN ID
        time.sleep(140)
        Check_CoA_and_VLANID(VLANID=dynamicset.InternalQuarantineVLan,message='Internal Quarantine VLAN by Broadcast')

        lan1_.SendNA(IP= lan1_.globalIp,Count= 1000) #lan1 發送 NDP 觸發群播播超量，觸發 CoA 以及會取得內部隔離的 VLAN ID, 跳過此測試因為此功能未做完
        time.sleep(140)
        # Check_CoA_and_VLANID(VLANID=dynamicset.InternalQuarantineVLan,message='Internal Quarantine VLAN by Muticast')

        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_) #將 lan1 從 VLAN 對應表中刪除
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        dynamicset.EnableInternalAutoQuarantine =False
        dynamicset.EnableExternalAutoQuarantine = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset) #關閉動態 VLAN 以及內外部隔離 VLAN 且關閉 802.1X 功能

#region 依照參數設定環境
with open('settingconfig_Hank.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = base64.b64encode(settingconfig_['APIpwd'].encode('UTF-8'))
AthenacWebAPI_ = AthenacWebAPILibry(f'https://{serverIP_}:8001',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
AthenacProbeAPI_ = AthenacProbeAPILibry(f'http://{AthenacWebAPI_.GetPortWorerkIPbyID(settingconfig_["probeID"])}:18002')
TestIPv4_ = settingconfig_['TestIPv4']
TestIPv6_ = settingconfig_['TestIPv6']
ProbeMAC_ = settingconfig_['ProbeMAC']
VLANIDMapping_ = settingconfig_['VLANIDMapping']
SiteID_ = settingconfig_['SiteId']
DynamicAVPID_ = settingconfig_['DynamicAVPID']
AuthAVPID_ = settingconfig_['AuthAVPID']
lan1_ = PacketAction(settingconfig_['lan1'])
lan1MACUpper_ = ''.join(lan1_.mac.upper().split(':'))
lan2_ = PacketAction(settingconfig_['lan2'])
lan2MACUpper_ = ''.join(lan2_.mac.upper().split(':'))
#endregion
