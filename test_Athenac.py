import threading,time,json,pytest_check as check
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule,SendHostAgentType,RegisterTypebyAutoRegist
from APITools.DataModels.datamodel_apidata import BlockMessageSetting, RadiusClient, RadiusSetting

class CTestIPAM:
    def test_IPBlockCase(self)->None:
            AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=True,siteid=SiteID_)
            time.sleep(10)
            check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_),f' Not Receive ARP {lan2_.Ip}')
            lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2)
            check.is_false(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_),f' Recive ARP Rqply {TestIPv4_} by Change IP')
            AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=False,siteid=SiteID_)

    def test_MACblockTestCase(self)->None:
        AthenacWebAPI_.BlockMAC(mac=lan2MACUpper_,block=True,siteid=SiteID_)
        time.sleep(10)
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_),f' Not Receive ARP {lan2_.Ip}')
        check.is_true(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_),f' Not Recive ARP Reply {TestIPv4_} by Change IP')
        check.is_true(lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_),f' Not Receive NDP Adver {lan2_.globalIp}')
        lan2_.SendNA(IP=TestIPv6_,Count=2,WaitSec=2)
        check.is_true(lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_),f' Not Receive NDP Adver {TestIPv6_}')
        AthenacWebAPI_.BlockMAC(mac=lan2MACUpper_,block=False,siteid=SiteID_)

    def test_ProtectIPTestCase(self)->None:
        AthenacWebAPI_.DelIP(ip=TestIPv4_,siteid=SiteID_)
        AthenacWebAPI_.CreateProtectIP(ip=TestIPv4_,mac=lan1MACUpper_,siteid=SiteID_)
        check.is_false(lan1_.ARPBlockCheck(srcIP='0.0.0.0',dstIP=TestIPv4_,ProbeMAC=ProbeMAC_)
        ,f' Recive ARP {TestIPv4_} by lan1 MAC use 0.0.0.0 check IP used {TestIPv4_}')
        check.is_true(lan2_.ARPBlockCheck(srcIP='0.0.0.0',dstIP=TestIPv4_,ProbeMAC=ProbeMAC_)
        ,f' Not Recive ARP {TestIPv4_} by lan2 MAC use 0.0.0.0 check IP used {TestIPv4_}')
        check.is_true(lan2_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_)
        ,f' Not Recive ARP {TestIPv4_} by lan2 MAC use {TestIPv4_}')
        AthenacWebAPI_.DelIP(ip=TestIPv4_,siteid=SiteID_)

    def test_BindingIPTestCase(self)->None:
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_)
        time.sleep(5)
        AthenacWebAPI_.CreateBindingIP(ip=lan2_.Ip,siteid=SiteID_)
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2)
        check.is_true(lan2_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan2_.gatewayIp,ProbeMAC=ProbeMAC_)
        ,f' Not Recive ARP {TestIPv4_} by lan2 MAC use {TestIPv4_}')
        AthenacWebAPI_.DelIP(ip=lan2_.Ip,siteid=SiteID_)
        check.is_false(lan1_.ARPBlockCheck(srcIP=TestIPv4_,dstIP=lan1_.gatewayIp,ProbeMAC=ProbeMAC_)
        ,f' Recive ARP {TestIPv4_} by lan1 MAC use {TestIPv4_}')

    def test_UnauthMACBlockTestCase(self)->None:
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.AuthMAC(mac=lan2MACUpper_,auth=False,siteid=SiteID_)
        time.sleep(10)
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_)
        ,f' Not Receive ARP {lan2_.Ip}')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2)
        check.is_true(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_)
        ,f' Not Recive ARP Reply {TestIPv4_} by Change IP')
        check.is_true(lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_)
        ,f' Not Receive NDP Adver {lan2_.globalIp}')
        lan2_.SendNA(IP=TestIPv6_,Count=2,WaitSec=2)
        check.is_true(lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_)
        ,f' Not Receive NDP Adver {TestIPv6_}')
        AthenacWebAPI_.AuthMAC(mac=lan2MACUpper_,auth=True,siteid=SiteID_)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)

    def test_UnauthIPBlockTestCase(self)->None:
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.AuthIP(ip=lan2_.Ip,auth=False,siteid=SiteID_)
        time.sleep(10)
        check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_)
        ,f' Not Receive ARP {lan2_.Ip}')
        lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2)
        check.is_false(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_)
        ,f' Recive ARP Rqply {TestIPv4_} by Change IP')
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=False,siteid=SiteID_)

    def test_UserApplyTestCase(self)->None:
        ADAccount= 'Hank'
        DBAccount = 'admin'
        LDAPaccount ='RAJ'
        blockmessagesetting = BlockMessageSetting(EnableBlockNotify=True,EnableVerifyModule=True,ADverify=True,DBverify=True,LDAPverify=True)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.UpdateBlockMessage(config=blockmessagesetting,siteid=SiteID_)
        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_)
        AthenacCoreAPI_.AuthMACFromUserApply(lan2_.Ip,lan2MACUpper_,ADAccount,'QkIHIDPyeiIALps4IKGH+w==') # verify by AD
        MACdata =  AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_)
        if not MACdata : 
            check.is_not_none(MACdata,f' can not queried this {lan2MACUpper_} Detail from verify by AD')
        else: 
            check.is_true(MACdata['IsRegisteded'] == 1 and MACdata['RegisterUserId'] == ADAccount
            ,f' verify fail, MAC is {lan2MACUpper_} from verify by AD')
        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_)
        AthenacCoreAPI_.AuthMACFromUserApply(lan2_.Ip,lan2MACUpper_,DBAccount,'36IqJwCHVwl9IS4w4b1mMw==') # verify by DB
        MACdata =  AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_)
        if not MACdata : 
            check.is_not_none(MACdata,f' can not queried this {lan2MACUpper_} Detail from verify by DB')
        else: 
            check.is_true(MACdata['IsRegisteded'] == 1 and MACdata['RegisterUserId'] == DBAccount
            ,f' verify fail, MAC is {lan2MACUpper_} from verify by DB')
        AthenacWebAPI_.AuthMAC(lan2MACUpper_,auth=False,siteid=SiteID_)
        AthenacCoreAPI_.AuthMACFromUserApply(lan2_.Ip,lan2MACUpper_,LDAPaccount,'AgRAu+JjydaLEw3me8kTxA==') # verify by LDAP
        MACdata =  AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_)
        if not MACdata : 
            check.is_not_none(MACdata,f' can not queried this {lan2MACUpper_} Detail from verify by LDAP')
        else: 
            check.is_true(MACdata['IsRegisteded'] == 1 and MACdata['RegisterUserId'] == LDAPaccount
            ,f' verify fail, MAC is {lan2MACUpper_} from verify by LDAP')
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)

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
    def test_IPconflictTestCase(self)->None:
        checkv4 = False
        checkv6 = False
        for i in range(10):
            lan1_.SendARPReply(TestIPv4_)
            lan2_.SendARPReply(TestIPv4_)
            lan1_.SendNA(TestIPv6_)
            lan2_.SendNA(TestIPv6_)
            time.sleep(2)
        time.sleep(10)
        IPconflictdevices = AthenacWebAPI_.GetIPconflictDeviceList()
        for IPconflictdevice in IPconflictdevices:
            if IPconflictdevice['Ip'] == TestIPv4_ and lan1MACUpper_ in IPconflictdevice['Macs'] and lan2MACUpper_ in IPconflictdevice['Macs']:checkv4 = True; continue
            if IPconflictdevice['Ip'] == TestIPv6_ and lan1MACUpper_ in IPconflictdevice['Macs'] and lan2MACUpper_ in IPconflictdevice['Macs']:checkv6 = True; continue
        check.is_true(checkv4,f' IPconflictTestCase {TestIPv4_}')
        check.is_true(checkv6,f' IPconflictTestCase {TestIPv6_}')
            
    def test_OutofVLANTestCase(self)->None:
        checkflag = False
        lan1_.SendARPReply('10.1.1.87')
        time.sleep(10)
        outofVLANDevices = AthenacWebAPI_.GetOutofVLANList()
        for outofVLANDevice in outofVLANDevices:
            if outofVLANDevice['Ip'] == '10.1.1.87' and outofVLANDevice['Mac'] == lan1MACUpper_: checkflag = True; break
        check.is_true(checkflag,' OutofVLANTestCase IP: 10.1.1.87')

    def test_UnknowDHCPTestCase(self)->None:
        lan1_.SendDHCPv4Offer()
        lan1_.SendDHCPv6Advertise()
        lan1_.SendRA()
        time.sleep(10)
        unknowDHCPList = AthenacWebAPI_.GetUnknowDHCPList()
        checkDHCPv4 = False
        checkDHCPv6 = False
        checkSLAAC = False
        for unknowDHCP in unknowDHCPList:
            if unknowDHCP['Ip'] == lan1_.Ip and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 1: checkDHCPv4 = True; continue
            if unknowDHCP['Ip'] == lan1_.linklocalIp and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 1: checkDHCPv6 = True; continue
            if unknowDHCP['Ip'] == lan1_.globalIp and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 2:checkSLAAC=True; continue
        check.is_true(checkDHCPv4,' UnknowDHCPTestCase DHCPv4')
        check.is_true(checkDHCPv6,' UnknowDHCPTestCase DHCPv6')
        check.is_true(checkSLAAC,' UnknowDHCPTestCase SLAAC')

    def test_BroadcastTesttCase(self)->None:
        checkfalg = False
        lan1_.SendARPReply(lan1_.Ip,1000)
        time.sleep(120)
        borDevices = AthenacWebAPI_.GetBrocastDeviceList()
        for borDevice in borDevices:
            if borDevice['Ip'] == lan1_.Ip and borDevice['Mac'] == lan1MACUpper_: checkfalg = True; break
        check.is_true(checkfalg,f' BrocastcastTest {lan1_.Ip}')
 
    def test_MultcastTestCase(self)->None:
        checkflag = False
        lan1_.SendNA(lan1_.globalIp,1000)
        time.sleep(120)
        mutidevices = AthenacWebAPI_.GetMulicastDeviceList()
        for mutidevice in mutidevices:
            if mutidevice['Ip'] == lan1_.globalIp and mutidevice['Mac'] == lan1MACUpper_: checkflag = True; break
        check.is_true(checkflag,f' MultcastTestCase {lan1_.globalIp}')

class TestRadius:
    def test_Radius8021XTestCase(self)->None:
        radiusset = RadiusSetting(SiteId=SiteID_,EnableDynamicVLAN=False)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=AuthAVPID_)
        AthenacWebAPI_.UpdateRadiusSetting(radiusset)
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_)
        AthenacWebAPI_.AddRadiusClient(radiusclientset)
        AthenacWebAPI_.SwitchSiteMonitMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        AthenacWebAPI_.AuthMAC(mac=lan1MACUpper_,auth=False,siteid=SiteID_)
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if radiuscode:
            radiuscode =radiuscode['RadiusCode']
        check.is_true(radiuscode == 3,f' Radius code not 3 is {radiuscode}')
        AthenacWebAPI_.AuthMAC(mac=lan1MACUpper_,auth=True,siteid=SiteID_)
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if radiuscode:
            radiuscode =radiuscode['RadiusCode']
        check.is_true(radiuscode == 2,f' Radius code not 2 is {radiuscode}')
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)
        AthenacWebAPI_.SwitchSiteMonitMode(enable=False,siteid=SiteID_)
        radiusset.EnableRadius = False
        AthenacWebAPI_.UpdateRadiusSetting(radiusset)

    def test_RadiusDynamicVLANTestCase(self)->None:
        dynamicset = RadiusSetting(SiteId=SiteID_)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=DynamicAVPID_)
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_)
        AthenacWebAPI_.AddRadiusClient(radiusclientset)
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult :
            check.is_not_none(radiusresult,' not Recived Radius Reply Packet from External Default VLAN')
        else : 
            check.is_true(radiusresult['VLANId'] == str(dynamicset.ExternalDefaultVLan)
            ,f' Recive not VLAN ID {dynamicset.ExternalDefaultVLan}, is VLAN ID {radiusresult["VLANId"]} from External Default VLAN')
        radiusresult = None
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult :
            check.is_not_none(radiusresult,' not Recived Radius Reply Packet from Internal Default VLAN')
        else:
            check.is_true(radiusresult['VLANId'] == str(dynamicset.InternalDefaultVLan)
            ,f' Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {radiusresult["VLANId"]} from Internal Default VLAN')
        radiusresult = None
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,VLANIDMapping_,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult :
            check.is_not_none(radiusresult,' not Recived Radius Reply Packet from VLAN Mapping List')
        else:
            check.is_true(radiusresult['VLANId'] == str(VLANIDMapping_)
            ,f' Recive not VLAN ID {VLANIDMapping_} is VLAN ID {radiusresult["VLANId"]} from VLAN Mapping List')
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)

    def test_RadiusCoATestCasebyQuar(self)->None:
        dynamicset = RadiusSetting(SiteId=SiteID_)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=DynamicAVPID_)
        dynamicset.SiteVerifyModule = SiteVerifyModule.EnableDbVerify.value
        dynamicset.EnableInternalAutoQuarantine = True
        dynamicset.EnableExternalAutoQuarantine = True
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_)
        AthenacWebAPI_.ClearAllMappingatSite(siteid=SiteID_)
        AthenacWebAPI_.AddRadiusClient(radiusclientset)
        listens = PacketListenFromFilter(lan1_.nicname)
        CoAPacketCheck = threading.Thread(target=listens.Sniffer,args=['udp and port 3799',60*15])
        CoAPacketCheck.start() #Packet listen start
        lan1replyvlanid = lan1_.GetRadiusReply(serverip= serverIP_,nasip=lan1_.Ip) #Test external default VLAN
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalDefaultVLan)
        ,f' Recive not VLAN ID {dynamicset.ExternalDefaultVLan} is VLAN ID {lan1replyvlanid} from External Default VLAN')
        lan1_.SendDHCPv4Offer() #Known DHCPv4 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from External Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv4')
        lan1_.SendDHCPv6Advertise() #Known DHCPv6 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from External Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv6')
        lan1_.SendARPReply(lan1_.Ip,1000) #Broadcast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from External Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Broadcast')
        lan1_.SendNA(lan1_.globalIp,1000) #Muticast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from External Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.ExternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Muticast')
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_)
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip) #Test internal default VLAN
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalDefaultVLan)
        ,f' Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {lan1replyvlanid} from Internal Default VLAN')
        lan1_.SendDHCPv4Offer() #Known DHCPv4 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from internal Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by DHCPv4')
        lan1_.SendDHCPv6Advertise() #Known DHCPv6 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from internal Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by DHCPv6')
        lan1_.SendARPReply(lan1_.Ip,1000) #Broadcast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from internal Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalQuarantineVLan)
        ,f' Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by Broadcast')
        lan1_.SendNA(lan1_.globalIp,1000) #Muticast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            check.is_not_none(listens.radiuspackets,' not Recive CoA Packet from internal Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if lan1replyvlanid:
            lan1replyvlanid = lan1replyvlanid['VLANId']
        check.is_true(lan1replyvlanid == str(dynamicset.InternalQuarantineVLan)
        ,f'  Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by Muticast')
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        dynamicset.EnableInternalAutoQuarantine =False
        dynamicset.EnableExternalAutoQuarantine = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)


with open('settingconfig.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = settingconfig_['APIpwd']
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
AthenacCoreAPI18002_ = AthenacCoreAPILibry(f'http://{serverIP_}:18002',settingconfig_['probeID'],settingconfig_['daemonID'])
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
time.sleep(5)


