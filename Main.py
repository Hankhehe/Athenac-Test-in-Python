import time
import datetime
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListen
from APITools.athenac_web_API_libry import AthenacWebAPILibry


def WriteLog(Txt:str)->None:
    with open('TestLog.txt','a') as f:
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' : '+Txt+'\n')

def UnknowDHCPTestCase()->None:
    WriteLog('UnknowDHCPTestCaseStart')
    lan1.SendDHCPv4Offer()
    lan1.SendDHCPv6Advertise()
    lan1.SendRA()
    time.sleep(10)
    unknowDHCPList = AthenacAPI.GetUnknowDHCPList()
    checkDHCPv4 = False
    checkDHCPv6 = False
    checkSLAAC = False
    for unknowDHCP in unknowDHCPList:
        if unknowDHCP['Ip'] == lan1.Ip and unknowDHCP['Mac'] == lan1MACUpper and unknowDHCP['ServerType'] == 1: checkDHCPv4 = True; continue
        if unknowDHCP['Ip'] == lan1.linklocalIp[0] and unknowDHCP['Mac'] == unknowDHCP['ServerType'] and unknowDHCP['ServerType'] == 1: checkDHCPv6 = True; continue
        if unknowDHCP['Ip'] == lan1.globalIp[0] and unknowDHCP['Mac'] == unknowDHCP['ServerType'] and unknowDHCP['ServerType'] == 2:checkSLAAC=True; continue
    if not checkDHCPv4: WriteLog('False : UnknowDHCPTestCase DHCPv4')
    if not checkDHCPv6: WriteLog('False : UnknowDHCPTestCase DHCPv6')
    if not checkSLAAC: WriteLog('False : UnknowDHCPTestCase SLAAC')
    WriteLog('UnknowDHCPTestCaseFinish')

def BroadcastTesttCase()->None:
    WriteLog('BroadcastTestCaseStart')
    check = False
    lan1.SendARPReply(lan1.Ip,1000)
    time.sleep(120)
    borDevices = AthenacAPI.GetBrocastDeviceList()
    for borDevice in borDevices:
        if borDevice['Ip'] == lan1.Ip and borDevice['Mac'] == lan1MACUpper: check = True; break
    if not check:WriteLog('False : BrocastcastTest %s'%(lan1.Ip))
    WriteLog('BroadcastTestCaseFinish')

def MultcastTestCase()->None:
    WriteLog('MuticastTestCaseStart')
    check = False
    lan1.SendNA(lan1.globalIp,1000)
    time.sleep(120)
    mutidevices = AthenacAPI.GetMulicastDeviceList()
    for mutidevice in mutidevices:
        if mutidevice['Ip'] == lan1.globalIp[0] and mutidevice['Mac'] == lan1MACUpper: check = True; break
    if not check:WriteLog('False : MultcastTestCase %s'%(lan1.globalIp))
    WriteLog('MuticastTestCaseFinish')
            
def OutofVLANTestCase()->None:
    WriteLog('OutofVLANTestCaseStart')
    check = False
    lan1.SendARPReply('10.1.1.87')
    time.sleep(10)
    outofVLANDevices = AthenacAPI.GetOutofVLANList()
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
    IPconflictdevices = AthenacAPI.GetIPconflictDeviceList()
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
    MacData = AthenacAPI.GetMACDetail(MAC=lan2MACUpper,Isonline=True,SiteId=1)
    AthenacAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=True)
    time.sleep(10)
    if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
    if not lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False :Change IP Not Recive ARP Reply {TestIPv4}')
    if not lan2.NDPBlockCheck(lan2.globalIp,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {lan2.globalIp}')
    if not lan2.NDPBlockCheck(TesteIPv6,lan2.gatewatIpv6,ProbeMAC): WriteLog(f'False : Not Receive NDP Adver {TesteIPv6}')
    AthenacAPI.BlockMAC(macid=MacData[0]['MacAddressId'],block=False)
    WriteLog('MACblockTestCaseFinish')

def IPBlockCase()->None:
    WriteLog('IPBlockCaseStart')
    IPData = AthenacAPI.GetIPv4Detail(lan2.Ip,True)
    AthenacAPI.BlockIPv4(IPData[0]['HostId'],True)
    time.sleep(10)
    if not lan2.ARPBlockCheck(lan2.Ip,lan2.gatewayIp,ProbeMAC):WriteLog(f'False : Not Receive ARP {lan2.Ip}')
    if lan2.ARPBlockCheck(TestIPv4,lan2.gatewayIp,ProbeMAC):WriteLog(f'False :Change IP Not Recive ARP Rqply {TestIPv4}')
    AthenacAPI.BlockIPv4(IPData[0]['HostId'],False)
    WriteLog('IPBlockCaseFinish')

def RadiusTestCase()->None:
    AthenacAPI.UpdateRadiusSetting(1)
    pass

serverIP= input('Please input Server API Url example https://IP:8001 : ') or 'https://192.168.21.180:8001'
APIaccount = input('Please input Athenac accountname : ') or 'admin'
APIpwd = input('Please input Athenac password : ') or 'admin'
AthenacAPI = AthenacWebAPILibry(serverIP,APIaccount,APIpwd)
TestIPv4 = input('Please input TestIPv4 : ') or '192.168.21.87'
TesteIPv6 = input('Please input TestIpv6 GloboalIP : ') or '2001:b030:2133:815::87'
ProbeMAC = input('Please input ProbeMAC example aa:aa:aa:aa:aa:aa : ') or '00:aa:ff:ae:09:cc'
lan1 = PacketAction( input('Please auth nic name : ') or 'Ethernet1')
lan1MACUpper = ''.join(lan1.mac.upper().split(':'))
lan2 = PacketAction(input('Please input unauth nic name : ') or 'Ethernet2')
lan2MACUpper = ''.join(lan2.mac.upper().split(':'))

# PacketListen(ProbeMAC,lan1.nicName)
RadiusTestCase()
IPBlockCase() #use lan1 and lan2
MACblockTestCase() # use lan1 and lan2
IPconflictTestCase() # use lan1 and lan2
OutofVLANTestCase() #use lan1
BroadcastTesttCase()#use lan1
MultcastTestCase() #use lan1
UnknowDHCPTestCase() # use lan1
DHCPpressureTestCase() # use lan1
WriteLog('----------------------TestFinish from All TetsCase----------------------')
