import threading,time,datetime,codecs,json
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from APITools.DataModels.datamodel_apidata import RadiusClient, RadiusSetting

def WriteLog(Txt:str)->None:
    with codecs.open('TestLog.txt','a','utf-8') as f:
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' : '+Txt+'\n')

def UnknowDHCPTestCase()->None:
    WriteLog('UnknowDHCPTestCaseStart')
    try:
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
            if unknowDHCP['Ip'] == lan1_.linklocalIp[0] and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 1: checkDHCPv6 = True; continue
            if unknowDHCP['Ip'] == lan1_.globalIp[0] and unknowDHCP['Mac'] == lan1MACUpper_ and unknowDHCP['ServerType'] == 2:checkSLAAC=True; continue
        if not checkDHCPv4: WriteLog('False : UnknowDHCPTestCase DHCPv4')
        if not checkDHCPv6: WriteLog('False : UnknowDHCPTestCase DHCPv6')
        if not checkSLAAC: WriteLog('False : UnknowDHCPTestCase SLAAC')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('UnknowDHCPTestCaseFinish')

def BroadcastTesttCase()->None:
    WriteLog('BroadcastTestCaseStart')
    try:
        check = False
        lan1_.SendARPReply(lan1_.Ip,1000)
        time.sleep(120)
        borDevices = AthenacWebAPI_.GetBrocastDeviceList()
        for borDevice in borDevices:
            if borDevice['Ip'] == lan1_.Ip and borDevice['Mac'] == lan1MACUpper_: check = True; break
        if not check:WriteLog(f'False : BrocastcastTest {lan1_.Ip}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('BroadcastTestCaseFinish')

def MultcastTestCase()->None:
    WriteLog('MuticastTestCaseStart')
    try:
        check = False
        lan1_.SendNA(lan1_.globalIp,1000)
        time.sleep(120)
        mutidevices = AthenacWebAPI_.GetMulicastDeviceList()
        for mutidevice in mutidevices:
            if mutidevice['Ip'] == lan1_.globalIp[0] and mutidevice['Mac'] == lan1MACUpper_: check = True; break
        if not check:WriteLog(f'False : MultcastTestCase {lan1_.globalIp}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('MuticastTestCaseFinish')
            
def OutofVLANTestCase()->None:
    WriteLog('OutofVLANTestCaseStart')
    try:
        check = False
        lan1_.SendARPReply('10.1.1.87')
        time.sleep(10)
        outofVLANDevices = AthenacWebAPI_.GetOutofVLANList()
        for outofVLANDevice in outofVLANDevices:
            if outofVLANDevice['Ip'] == '10.1.1.87' and outofVLANDevice['Mac'] == lan1MACUpper_: check = True; break
        if not check: WriteLog('False : OutofVLANTestCase IP: 10.1.1.87')
    except Exception as e :
        WriteLog('Exception : ' + str(e))
    WriteLog('OutofVLANTestCaseFinish')

def IPconflictTestCase()->None:
    WriteLog('IPconflictTestCaseStart')
    try:
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
        if not checkv4 : WriteLog(f'False : IPconflictTestCase {TestIPv4_}')
        if not checkv6 : WriteLog(f'False : IPconflictTestCase {TestIPv6_}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('IPconflictTestCaseSFinish')

def DHCPpressureTestCase()->None:
    WriteLog('DHCPpressureTestCaseStart')
    try:
        log = lan1_.DHCPv4ClientTest()
        WriteLog(log)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('DHCPpressureTestCaseFinish')

def DHCPv6pressureTestCase()->None:
    WriteLog('DHCPv6pressureTestCaseStart')
    try:
        log = lan1_.DHCPv6ClientTest()
        WriteLog(log)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('DHCPpv6ressureTestCaseFinish')


def MACblockTestCase()->None:
    WriteLog('MACblockTestCaseStart')
    try:
        MacData = AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_)
        AthenacWebAPI_.BlockMAC(macid=MacData[0]['MacAddressId'],block=True)
        time.sleep(10)
        if not lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Receive ARP {lan2_.Ip}')
        if not lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Recive ARP Reply {TestIPv4_} by Change IP')
        if not lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_): WriteLog(f'False : Not Receive NDP Adver {lan2_.globalIp}')
        if not lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_): WriteLog(f'False : Not Receive NDP Adver {TestIPv6_}')
        AthenacWebAPI_.BlockMAC(macid=MacData[0]['MacAddressId'],block=False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('MACblockTestCaseFinish')

def IPBlockCase()->None:
    WriteLog('IPBlockCaseStart')
    try:
        IPData = AthenacWebAPI_.GetIPv4Detail(lan2_.Ip,SiteID_)
        AthenacWebAPI_.BlockIPv4(IPData[0]['HostId'],True)
        time.sleep(10)
        if not lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Receive ARP {lan2_.Ip}')
        if lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Recive ARP Rqply {TestIPv4_} by Change IP')
        AthenacWebAPI_.BlockIPv4(IPData[0]['HostId'],False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('IPBlockCaseFinish')

def RadiusDynamicVLANTestCase()->None:
    WriteLog('RadiusDynamicVLANTestCaseStart')
    try:
        dynamicset = RadiusSetting(SiteId=SiteID_)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=DynamicAVPID_)
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_)
        AthenacWebAPI_.AddRadiusClient(radiusclientset)
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from External Default VLAN')
        else : 
            if radiusresult['VLANId'] != str(dynamicset.ExternalDefaultVLan):
                WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalDefaultVLan}, is VLAN ID {radiusresult["VLANId"]} from External Default VLAN')
        radiusresult = None
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from Internal Default VLAN')
        else:
            if radiusresult['VLANId'] != str(dynamicset.InternalDefaultVLan):
                WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {radiusresult["VLANId"]} from Internal Default VLAN')
        radiusresult = None
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,VLANIDMapping_,SiteID_)
        radiusresult = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from VLAN Mapping List')
        else:
            if radiusresult['VLANId'] != str(VLANIDMapping_):
                WriteLog(f'False : Recive not VLAN ID {VLANIDMapping_} is VLAN ID {radiusresult["VLANId"]} from VLAN Mapping List')
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('RadiusDynamicVLANTestCaseFinish')

def RadiusCoATestCasebyQuar()->None:
    WriteLog('RadiusCoATestCaseStart')
    try:
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
        CoAPacketCheck = threading.Thread(target=listens.Sniffer,args=['udp and port 3799',60*30])
        CoAPacketCheck.start() #Packet listen start
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId'] #Test external default VLAN
        if lan1replyvlanid != str(dynamicset.ExternalDefaultVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalDefaultVLan} is VLAN ID {lan1replyvlanid} from External Default VLAN')
        lan1_.SendDHCPv4Offer() #Known DHCPv4 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv4')
        lan1_.SendDHCPv6Advertise() #Known DHCPv6 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv6')
        lan1_.SendARPReply(lan1_.Ip,1000) #Broadcast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Broadcast')
        lan1_.SendNA(lan1_.globalIp,1000) #Muticast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Muticast')
        AthenacWebAPI_.AddVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,None,SiteID_)
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId'] #Test internal default VLAN
        if lan1replyvlanid != str(dynamicset.InternalDefaultVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {lan1replyvlanid} from Internal Default VLAN')
        lan1_.SendDHCPv4Offer() #Known DHCPv4 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by DHCPv4')
        lan1_.SendDHCPv6Advertise() #Known DHCPv6 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by DHCPv6')
        lan1_.SendARPReply(lan1_.Ip,1000) #Broadcast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by Broadcast')
        lan1_.SendNA(lan1_.globalIp,1000) #Muticast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False :  Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by Muticast')
        AthenacWebAPI_.DelVLANMapping(lan1MACUpper_,RadiusVLANMappingType.MAC.value,SiteID_)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        dynamicset.EnableInternalAutoQuarantine =False
        dynamicset.EnableExternalAutoQuarantine = False
        AthenacWebAPI_.UpdateRadiusSetting(dynamicset)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('RadiusCoATestCaseFinish')

def UnauthMACBlockTestCase()->None:
    WriteLog('UnauthMACBlockTestCaseStart')
    try:
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        MacData = AthenacWebAPI_.GetMACDetail(MAC=lan2MACUpper_,SiteId=SiteID_)
        AthenacWebAPI_.AuthMAC(macid=MacData[0]['MacAddressId'],auth=False)
        time.sleep(10)
        if not lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Receive ARP {lan2_.Ip}')
        if not lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Recive ARP Reply {TestIPv4_} by Change IP')
        if not lan2_.NDPBlockCheck(lan2_.globalIp,lan2_.gatewatIpv6,ProbeMAC_): WriteLog(f'False : Not Receive NDP Adver {lan2_.globalIp}')
        if not lan2_.NDPBlockCheck(TestIPv6_,lan2_.gatewatIpv6,ProbeMAC_): WriteLog(f'False : Not Receive NDP Adver {TestIPv6_}')
        AthenacWebAPI_.AuthMAC(macid=MacData[0]['MacAddressId'],auth=True)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('UnauthMACBlockTestCaseFinish')

def UnauthIPBlockTestCase()->None:
    WriteLog('UnauthIPBlockTestCaseStart')
    try:
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=True,siteid=SiteID_)
        IPData = AthenacWebAPI_.GetIPv4Detail(lan2_.Ip,SiteID_)
        AthenacWebAPI_.AuthIP(IPData[0]['HostId'],False)
        time.sleep(10)
        if not lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Not Receive ARP {lan2_.Ip}')
        if lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_):WriteLog(f'False : Recive ARP Rqply {TestIPv4_} by Change IP')
        AthenacWebAPI_.AuthIP(IPData[0]['HostId'],True)
        AthenacWebAPI_.SwitchIPSiteSaveMode(enable=False,siteid=SiteID_)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('UnauthIPBlockTestCaseFinish')

def Radius8021XTestCase()->None:
    WriteLog('Radius8021XTestCaseStart')
    try:
        radiusset = RadiusSetting(SiteId=SiteID_,EnableDynamicVLAN=False)
        radiusclientset = RadiusClient(SiteId=SiteID_,RadiusAVPId=AuthAVPID_)
        AthenacWebAPI_.UpdateRadiusSetting(radiusset)
        AthenacWebAPI_.ClearAllRadiusClientatSite(siteid=SiteID_)
        AthenacWebAPI_.AddRadiusClient(radiusclientset)
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=True,siteid=SiteID_)
        macdata = AthenacWebAPI_.GetMACDetail(MAC=lan1MACUpper_,SiteId=SiteID_)
        AthenacWebAPI_.AuthMAC(macdata[0]['MacAddressId'],False)
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['RadiusCode']
        if radiuscode != 3 : WriteLog(f'False : Radius code not 3 is {radiuscode}')
        AthenacWebAPI_.AuthMAC(macdata[0]['MacAddressId'],True)
        radiuscode = lan1_.GetRadiusReply(serverIP_,lan1_.Ip)['RadiusCode']
        if radiuscode != 2 : WriteLog(f'False : Radius code not 2 is {radiuscode}')
        AthenacWebAPI_.SwitchMACSiteSaveMode(enable=False,siteid=SiteID_)
        radiusset.EnableRadius = False
        AthenacWebAPI_.UpdateRadiusSetting(radiusset)
    except Exception as e:
        WriteLog('Exception : ' + str(e)) 
    WriteLog('Radius8021XTestCaseFinish')

def ProtectIPTestCase()->None:
    AthenacWebAPILibry.CreateProtectIP()
    pass


with open('settingconfig.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = settingconfig_['APIpwd']
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
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

IPBlockCase() #use lan1 and lan2
MACblockTestCase() # use lan2
UnauthIPBlockTestCase() # use lan2
UnauthMACBlockTestCase() # use lan2
IPconflictTestCase() # use lan1 and lan2
OutofVLANTestCase() #use lan1
UnknowDHCPTestCase() # use lan1
BroadcastTesttCase()#use lan1
MultcastTestCase() #use lan1
Radius8021XTestCase() #use lan1
RadiusDynamicVLANTestCase() #use lan1
RadiusCoATestCasebyQuar() #use lan1
# DHCPpressureTestCase() # use lan1
# DHCPv6pressureTestCase() #use lan1
WriteLog('----------------------All test are over----------------------------')
