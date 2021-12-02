import threading
import time
import datetime
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from APITools.DataModels.datamodel_apidata import RadiusSetting

def WriteLog(Txt:str)->None:
    with open('TestLog.txt','a') as f:
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' : '+Txt+'\n')

def UnknowDHCPTestCase()->None:
    WriteLog('UnknowDHCPTestCaseStart')
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
    WriteLog('UnknowDHCPTestCaseFinish')

def BroadcastTesttCase()->None:
    WriteLog('BroadcastTestCaseStart')
    check = False
    lan1.SendARPReply(lan1.Ip,1000)
    time.sleep(120)
    borDevices = AthenacWebAPI.GetBrocastDeviceList()
    for borDevice in borDevices:
        if borDevice['Ip'] == lan1.Ip and borDevice['Mac'] == lan1MACUpper: check = True; break
    if not check:WriteLog('False : BrocastcastTest %s'%(lan1.Ip))
    WriteLog('BroadcastTestCaseFinish')

def MultcastTestCase()->None:
    WriteLog('MuticastTestCaseStart')
    check = False
    lan1.SendNA(lan1.globalIp,1000)
    time.sleep(120)
    mutidevices = AthenacWebAPI.GetMulicastDeviceList()
    for mutidevice in mutidevices:
        if mutidevice['Ip'] == lan1.globalIp[0] and mutidevice['Mac'] == lan1MACUpper: check = True; break
    if not check:WriteLog('False : MultcastTestCase %s'%(lan1.globalIp))
    WriteLog('MuticastTestCaseFinish')
            
def OutofVLANTestCase()->None:
    WriteLog('OutofVLANTestCaseStart')
    check = False
    lan1.SendARPReply('10.1.1.87')
    time.sleep(10)
    outofVLANDevices = AthenacWebAPI.GetOutofVLANList()
    for outofVLANDevice in outofVLANDevices:
        if outofVLANDevice['Ip'] == '10.1.1.87' and outofVLANDevice['Mac'] == lan1MACUpper: check = True; break
    if not check: WriteLog('False : OutofVLANTestCase IP: 10.1.1.87')
    WriteLog('OutofVLANTestCaseFinish')

def IPconflictTestCase()->None:
    WriteLog('IPconflictTestCaseStart')
    checkv4 = False
    checkv6 = False
    targetip = '192.168.21.87'
    targetipv6 = '2001:b030:2133:815::87'
    for i in range(10):
        lan1.SendARPReply(targetip)
        lan2.SendARPReply(targetip)
        lan1.SendNA(targetipv6)
        lan2.SendNA(targetipv6)
        time.sleep(2)
    time.sleep(10)
    IPconflictdevices = AthenacWebAPI.GetIPconflictDeviceList()
    for IPconflictdevice in IPconflictdevices:
        if IPconflictdevice['Ip'] == targetip and lan1MACUpper in IPconflictdevice['Macs'] and lan2MACUpper in IPconflictdevice['Macs']:checkv4 = True; continue
        if IPconflictdevice['Ip'] == targetipv6 and lan1MACUpper in IPconflictdevice['Macs'] and lan2MACUpper in IPconflictdevice['Macs']:checkv6 = True; continue
    if not checkv4 : WriteLog('False : IPconflictTestCase' + targetip )
    if not checkv6 : WriteLog('False : IPconflictTestCase' + targetipv6 )
    WriteLog('IPconflictTestCaseSFinish')

def DHCPpressureTestCase()->None:
    WriteLog('DHCPpressureTestCaseStart')
    log = lan1.DHCPv4ClientTest(3)
    WriteLog(log)
    log = lan1.DHCPv6ClientTest(3)
    WriteLog(log)
    WriteLog('DHCPpressureTestCaseFinish')

def MACblockTestCase()->None:
    WriteLog('MACblockTestCaseStart')
    MacData = AthenacWebAPI.GetMACDetail(MAC=lan2MACUpper,Isonline=True,SiteId=1)
    AthenacWebAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=True)
    time.sleep(10)
    if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
    if not lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False :Change IP Not Recive ARP Reply {TestIPv4}')
    if not lan2.NDPBlockCheck(lan2.globalIp,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {lan2.globalIp}')
    if not lan2.NDPBlockCheck(TesteIPv6,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {TesteIPv6}')
    AthenacWebAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=False)
    WriteLog('MACblockTestCaseFinish')

def IPBlockCase()->None:
    WriteLog('IPBlockCaseStart')
    IPData = AthenacWebAPI.GetIPv4Detail(lan2.Ip,True)
    AthenacWebAPI.BlockIPv4(IPData[0]['HostId'],True)
    time.sleep(10)
    if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
    if lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False :Change IP Not Recive ARP Rqply {TestIPv4}')
    AthenacWebAPI.BlockIPv4(IPData[0]['HostId'],False)
    WriteLog('IPBlockCaseFinish')

def RadiusDynamicVLANTestCase()->None:
    WriteLog('RadiusDynamicVLANTestCaseStart')
    AthenacWebAPI.UpdateRadiusSetting()
    AthenacWebAPI.ClearAllRadiusClientatSite()
    AthenacWebAPI.ClearAllRadiusClientatSite()
    AthenacWebAPI.AddRadiusClient()
    AthenacWebAPI.DelVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
    dynamicset = RadiusSetting() 
    lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
    if lan1replyvlanid != str(dynamicset.ExternalDefaultVLan):
        WriteLog(f'False : Recive not VLAN ID {dynamicset.ExternalDefaultVLan}, is VLAN ID {lan1replyvlanid} from External Default VLAN')
    AthenacWebAPI.AddVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
    lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
    if lan1replyvlanid != str(dynamicset.InternalDefaultVLan):
        WriteLog(f'False : Recive not VLAN ID {dynamicset.InternalDefaultVLan} is VLAN ID {lan1replyvlanid} from Internal Default VLAN')
    AthenacWebAPI.AddVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value,21)
    lan1replyvlanid = lan1.GetRadiusReply(serverIP,lan1.Ip)['VLANId']
    if lan1replyvlanid != '21':
        WriteLog(f'False : Recive not VLAN ID 21 is VLAN ID {lan1replyvlanid} from VLAN Mapping List')
    AthenacWebAPI.DelVLANMapping(lan1MACUpper,RadiusVLANMappingType.MAC.value)
    WriteLog('RadiusDynamicVLANTestCaseFinish')

def RadiusCoATestCasebyQuar()->None:
    WriteLog('RadiusCoATestCaseStart')
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
    WriteLog('RadiusCoATestCaseFinish')

    
serverIP= input('Please input Athenac Server IP : ') or '192.168.21.180'
APIaccount = input('Please input Athenac accountname : ') or 'admin'
APIpwd = input('Please input Athenac password : ') or 'admin'
AthenacWebAPI = AthenacWebAPILibry(f'http://{serverIP}:8000',APIaccount,APIpwd)
AthenacCoreAPI = AthenacCoreAPILibry(f'https://{serverIP}:18000',input('Please input Probe ID : ') or '10925416137',input('Please input Daemon ID : ') or '6922375401')
TestIPv4 = input('Please input TestIPv4 : ') or '192.168.21.87'
TesteIPv6 = input('Please input TestIpv6 GloboalIP : ') or '2001:b030:2133:815::87'
ProbeMAC = input('Please input ProbeMAC example aa:aa:aa:aa:aa:aa : ') or '00:aa:ff:ae:09:cc'
lan1 = PacketAction( input('Please auth nic name : ') or 'Ethernet1')
lan1MACUpper = ''.join(lan1.mac.upper().split(':'))
lan2 = PacketAction(input('Please input unauth nic name : ') or 'Ethernet2')
lan2MACUpper = ''.join(lan2.mac.upper().split(':'))




IPBlockCase() #use lan1 and lan2
MACblockTestCase() # use lan1 and lan2
IPconflictTestCase() # use lan1 and lan2
OutofVLANTestCase() #use lan1
UnknowDHCPTestCase() # use lan1
BroadcastTesttCase()#use lan1
RadiusCoATestCasebyQuar() #use lan1
RadiusDynamicVLANTestCase() #use lan1
MultcastTestCase() #use lan1
DHCPpressureTestCase() # use lan1
WriteLog('----------------------TestFinish from All TetsCase----------------------')
