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
        lan1.SendDHCPv4Offer()
        lan1.SendDHCPv6Advertise()
        lan1.SendRA()
        time.sleep(10)
        unknowDHCPList = AthenacWebAPI.GetUnknowDHCPList()
        checkDHCPv4 = False
        checkDHCPv6 = False
        checkSLAAC = False
        for unknowDHCP in unknowDHCPList:
            if unknowDHCP['Ip'] == lan1.Ip and unknowDHCP['Mac'] == lan1MACUpper and unknowDHCP['ServerType'] == 1: checkDHCPv4 = True; continue
            if unknowDHCP['Ip'] == lan1.linklocalIp[0] and unknowDHCP['Mac'] == lan1MACUpper and unknowDHCP['ServerType'] == 1: checkDHCPv6 = True; continue
            if unknowDHCP['Ip'] == lan1.globalIp[0] and unknowDHCP['Mac'] == lan1MACUpper and unknowDHCP['ServerType'] == 2:checkSLAAC=True; continue
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
        lan1.SendARPReply(lan1.Ip,1000)
        time.sleep(120)
        borDevices = AthenacWebAPI.GetBrocastDeviceList()
        for borDevice in borDevices:
            if borDevice['Ip'] == lan1.Ip and borDevice['Mac'] == lan1MACUpper: check = True; break
        if not check:WriteLog(f'False : BrocastcastTest {lan1.Ip}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('BroadcastTestCaseFinish')

def MultcastTestCase()->None:
    WriteLog('MuticastTestCaseStart')
    try:
        check = False
        lan1.SendNA(lan1.globalIp,1000)
        time.sleep(120)
        mutidevices = AthenacWebAPI.GetMulicastDeviceList()
        for mutidevice in mutidevices:
            if mutidevice['Ip'] == lan1.globalIp[0] and mutidevice['Mac'] == lan1MACUpper: check = True; break
        if not check:WriteLog(f'False : MultcastTestCase {lan1.globalIp}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('MuticastTestCaseFinish')
            
def OutofVLANTestCase()->None:
    WriteLog('OutofVLANTestCaseStart')
    try:
        check = False
        lan1.SendARPReply('10.1.1.87')
        time.sleep(10)
        outofVLANDevices = AthenacWebAPI.GetOutofVLANList()
        for outofVLANDevice in outofVLANDevices:
            if outofVLANDevice['Ip'] == '10.1.1.87' and outofVLANDevice['Mac'] == lan1MACUpper: check = True; break
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
            lan1.SendARPReply(TestIPv4)
            lan2.SendARPReply(TestIPv4)
            lan1.SendNA(TestIPv6)
            lan2.SendNA(TestIPv6)
            time.sleep(2)
        time.sleep(10)
        IPconflictdevices = AthenacWebAPI.GetIPconflictDeviceList()
        for IPconflictdevice in IPconflictdevices:
            if IPconflictdevice['Ip'] == TestIPv4 and lan1MACUpper in IPconflictdevice['Macs'] and lan2MACUpper in IPconflictdevice['Macs']:checkv4 = True; continue
            if IPconflictdevice['Ip'] == TestIPv6 and lan1MACUpper in IPconflictdevice['Macs'] and lan2MACUpper in IPconflictdevice['Macs']:checkv6 = True; continue
        if not checkv4 : WriteLog(f'False : IPconflictTestCase {TestIPv4}')
        if not checkv6 : WriteLog(f'False : IPconflictTestCase {TestIPv6}')
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('IPconflictTestCaseSFinish')

def DHCPpressureTestCase()->None:
    WriteLog('DHCPpressureTestCaseStart')
    try:
        log = lan1.DHCPv4ClientTest()
        WriteLog(log)
        log = lan1.DHCPv6ClientTest()
        WriteLog(log)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('DHCPpressureTestCaseFinish')

def MACblockTestCase()->None:
    WriteLog('MACblockTestCaseStart')
    try:
        MacData = AthenacWebAPI.GetMACDetail(MAC=lan2MACUpper,Isonline=True,SiteId=1)
        AthenacWebAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=True)
        time.sleep(10)
        if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
        if not lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Recive ARP Reply {TestIPv4} by Change IP')
        if not lan2.NDPBlockCheck(lan2.globalIp,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {lan2.globalIp}')
        if not lan2.NDPBlockCheck(TestIPv6,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {TestIPv6}')
        AthenacWebAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('MACblockTestCaseFinish')

def IPBlockCase()->None:
    WriteLog('IPBlockCaseStart')
    try:
        IPData = AthenacWebAPI.GetIPv4Detail(lan2.Ip,True)
        AthenacWebAPI.BlockIPv4(IPData[0]['HostId'],True)
        time.sleep(10)
        if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
        if lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Recive ARP Rqply {TestIPv4} by Change IP')
        AthenacWebAPI.BlockIPv4(IPData[0]['HostId'],False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('IPBlockCaseFinish')

def RadiusDynamicVLANTestCase()->None:
    WriteLog('RadiusDynamicVLANTestCaseStart')
    try:
        AthenacWebAPI.UpdateRadiusSetting()
        AthenacWebAPI.ClearAllRadiusClientatSite()
        AthenacWebAPI.ClearAllRadiusClientatSite()
        AthenacWebAPI.AddRadiusClient()
        AthenacWebAPI.DelVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
        dynamicset = RadiusSetting()
        radiusresult = lan1.GetRadiusReply(serverIP,lan1.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from External Default VLAN')
        else : 
            if radiusresult['VLANId'] != str(dynamicset.ExternalDefaultVLan):
                WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalDefaultVLan}, is VLAN ID {radiusresult["VLANId"]} from External Default VLAN')
        radiusresult = None
        AthenacWebAPI.AddVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
        radiusresult = lan1.GetRadiusReply(serverIP,lan1.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from Internal Default VLAN')
        else:
            if radiusresult['VLANId'] != str(dynamicset.InternalDefaultVLan):
                WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {radiusresult["VLANId"]} from Internal Default VLAN')
        radiusresult = None
        AthenacWebAPI.AddVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value,int(VLANIDMapping))
        radiusresult = lan1.GetRadiusReply(serverIP,lan1.Ip)
        if not radiusresult : WriteLog('False : not Recived Radius Reply Packet from VLAN Mapping List')
        else:
            if radiusresult['VLANId'] != VLANIDMapping:
                WriteLog(f'False : Recive not VLAN ID {VLANIDMapping} is VLAN ID {radiusresult["VLANId"]} from VLAN Mapping List')
        AthenacWebAPI.DelVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        AthenacWebAPI.UpdateRadiusSetting(dynamicset)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('RadiusDynamicVLANTestCaseFinish')

def RadiusCoATestCasebyQuar()->None:
    WriteLog('RadiusCoATestCaseStart')
    try:
        dynamicset = RadiusSetting()
        dynamicset.SiteVerifyModule = SiteVerifyModule.EnableDbVerify.value
        dynamicset.EnableInternalAutoQuarantine = True
        dynamicset.EnableExternalAutoQuarantine = True
        AthenacWebAPI.UpdateRadiusSetting(dynamicset)
        AthenacWebAPI.ClearAllRadiusClientatSite()
        AthenacWebAPI.ClearAllMappingatSite()
        AthenacWebAPI.AddRadiusClient()
        listens = PacketListenFromFilter(lan1.nicname)
        CoAPacketCheck = threading.Thread(target=listens.Sniffer,args=['udp and port 3799',60*30])
        CoAPacketCheck.start() #Packet listen start
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId'] #Test external default VLAN
        if lan1replyvlanid != str(dynamicset.ExternalDefaultVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalDefaultVLan} is VLAN ID {lan1replyvlanid} from External Default VLAN')
        lan1.SendDHCPv4Offer() #Known DHCPv4 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv4')
        lan1.SendDHCPv6Advertise() #Known DHCPv6 test by external MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by DHCPv6')
        lan1.SendARPReply(lan1.Ip,1000) #Broadcast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Broadcast')
        lan1.SendNA(lan1.globalIp,1000) #Muticast test by external MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from External Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.ExternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from External Quarantine VLAN by Muticast')
        AthenacWebAPI.AddVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId'] #Test internal default VLAN
        if lan1replyvlanid != str(dynamicset.InternalDefaultVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {lan1replyvlanid} from Internal Default VLAN')
        lan1.SendDHCPv4Offer() #Known DHCPv4 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by DHCPv4')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by DHCPv4')
        lan1.SendDHCPv6Advertise() #Known DHCPv6 test by internal MAC
        time.sleep(10)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by DHCPv6')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by DHCPv6')
        lan1.SendARPReply(lan1.Ip,1000) #Broadcast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by Broadcast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from Internal Quarantine VLAN by Broadcast')
        lan1.SendNA(lan1.globalIp,1000) #Muticast test by internal MAC
        time.sleep(140)
        if not listens.radiuspackets:
            WriteLog('False : not Recive CoA Packet from internal Quarantine VLAN by Muticast')
        else: listens.radiuspackets.clear()
        lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
        if lan1replyvlanid != str(dynamicset.InternalQuarantineVLan):
            WriteLog(f'False :  Recive not VLAN ID {dynamicset.InternalQuarantineVLan} is VLAN ID {lan1replyvlanid} from internal Quarantine VLAN by Muticast')
        AthenacWebAPI.DelVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
        dynamicset.EnableDynamicVLAN = False
        dynamicset.EnableRadius = False
        dynamicset.EnableInternalAutoQuarantine =False
        dynamicset.EnableExternalAutoQuarantine = False
        AthenacWebAPI.UpdateRadiusSetting(dynamicset)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('RadiusCoATestCaseFinish')

def UnauthMACBlockTestCase()->None:
    WriteLog('UnauthMACBlockTestCaseStart')
    try:
        AthenacWebAPI.SwitchMACSiteSafeMode(True)
        MacData = AthenacWebAPI.GetMACDetail(MAC=lan2MACUpper,Isonline=True,SiteId=1)
        AthenacWebAPI.AuthMAC(macid=MacData[0]['MacAddressId'],auth=False)
        time.sleep(10)
        if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
        if not lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Recive ARP Reply {TestIPv4} by Change IP')
        if not lan2.NDPBlockCheck(lan2.globalIp,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {lan2.globalIp}')
        if not lan2.NDPBlockCheck(TestIPv6,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {TestIPv6}')
        AthenacWebAPI.AuthMAC(macid=MacData[0]['MacAddressId'],auth=True)
        AthenacWebAPI.SwitchMACSiteSafeMode(False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('UnauthMACBlockTestCaseFinish')

def UnauthIPBlockTestCase()->None:
    WriteLog('UnauthIPBlockTestCaseStart')
    try:
        AthenacWebAPI.SwitchIPSiteSafeMode(True)
        IPData = AthenacWebAPI.GetIPv4Detail(lan2.Ip,True)
        AthenacWebAPI.AuthIP(IPData[0]['HostId'],False)
        time.sleep(10)
        if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
        if lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Recive ARP Rqply {TestIPv4} by Change IP')
        AthenacWebAPI.AuthIP(IPData[0]['HostId'],True)
        AthenacWebAPI.SwitchIPSiteSafeMode(False)
    except Exception as e:
        WriteLog('Exception : ' + str(e))
    WriteLog('UnauthIPBlockTestCaseFinish')

def Radius8021XTestCase()->None:
    WriteLog('Radius8021XTestCaseStart')
    try:
        radiusset = RadiusSetting(EnableDynamicVLAN=False)
        AthenacWebAPI.UpdateRadiusSetting(radiusset)
        AthenacWebAPI.ClearAllRadiusClientatSite()
        AthenacWebAPI.AddRadiusClient(RadiusClient(RadiusAVPId=2))
        AthenacWebAPI.SwitchMACSiteSafeMode(enable=True)
        macdata = AthenacWebAPI.GetMACDetail(MAC=lan1MACUpper,Isonline=True,SiteId=1)
        AthenacWebAPI.AuthMAC(macdata[0]['MacAddressId'],False)
        radiuscode = lan1.GetRadiusReply(serverIP,lan1.Ip)['RadiusCode']
        if radiuscode != 3 : WriteLog(f'False : Radius code not 3 is {radiuscode}')
        AthenacWebAPI.AuthMAC(macdata[0]['MacAddressId'],True)
        radiuscode = lan1.GetRadiusReply(serverIP,lan1.Ip)['RadiusCode']
        if radiuscode != 2 : WriteLog(f'False : Radius code not 2 is {radiuscode}')
        AthenacWebAPI.SwitchMACSiteSafeMode(enable=False)
        radiusset.EnableRadius = False
        AthenacWebAPI.UpdateRadiusSetting(radiusset)
    except Exception as e:
        WriteLog('Exception : ' + str(e)) 
    WriteLog('Radius8021XTestCaseFinish')


with open('settingconfig.json') as f:
    configfile = f.read()
    settingconfig = json.loads(configfile)
serverIP = settingconfig['serverIP']
APIaccount = settingconfig['APIaccount']
APIpwd = settingconfig['APIpwd']
AthenacWebAPI = AthenacWebAPILibry(f'http://{serverIP}:8000',APIaccount,APIpwd)
AthenacCoreAPI = AthenacCoreAPILibry(f'https://{serverIP}:18000',settingconfig['probeID'],settingconfig['daemonID'])
TestIPv4 = settingconfig['TestIPv4']
TestIPv6 = settingconfig['TestIPv6']
ProbeMAC = settingconfig['ProbeMAC']
VLANIDMapping = settingconfig['VLANIDMapping']
lan1 = PacketAction(settingconfig['lan1'])
lan1MACUpper = ''.join(lan1.mac.upper().split(':'))
lan2 = PacketAction(settingconfig['lan2'])
lan2MACUpper = ''.join(lan2.mac.upper().split(':'))
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
WriteLog('----------------------All test are over----------------------------')
