import time
import datetime
from NetPacketTools.PacketAction import PacketAction
from APITools.AthenacWebAPILibry import AthenacWebAPILibry


def WriteLog(Txt:str)->None:
    with open('TestLog.txt','a') as f:
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' : '+Txt+'\n')

def UnknowDHCPTestCase()->None:
    WriteLog('UnknowDHCPTestCaseStart')
    lan1.SendDHCPv4Offer()
    lan1.SendDHCPv6Advertise()
    lan1.SendRA()
    time.sleep(10)
    token,refretoken = AthenacAPI.GetLoginToken('admin','admin')
    unknowDHCPList = AthenacAPI.GetUnknowDHCPList(token)
    checkDHCPv4 = False
    checkDHCPv6 = False
    checkSLAAC = False
    for ip,mac,Type in unknowDHCPList:
        if ip == lan1.Ip and mac == lan1MACUpper and Type == 1: checkDHCPv4 = True; continue
        if ip == lan1.linklocalIP[0] and mac == lan1MACUpper and Type == 1: checkDHCPv6 = True; continue
        if ip == lan1.globallIP[0] and mac == lan1MACUpper and Type == 2:checkSLAAC=True; continue
    if not checkDHCPv4: WriteLog('False : UnknowDHCPTestCase DHCPv4')
    if not checkDHCPv6: WriteLog('False : UnknowDHCPTestCase DHCPv6')
    if not checkSLAAC: WriteLog('False : UnknowDHCPTestCase SLAAC')
    WriteLog('UnknowDHCPTestCaseFinish')

def BroadcastTesttCase()->None:
    WriteLog('BroadcastTestCaseStart')
    check = False
    lan1.SendARPReply(lan1.Ip,1000)
    time.sleep(120)
    Token,refreshToken = AthenacAPI.GetLoginToken('admin','admin')
    borDevices = AthenacAPI.GetBrocastDeviceList(Token)
    for ip,mac in borDevices:
        if ip == lan1.Ip and mac == lan1MACUpper: check = True; break
    if not check:WriteLog('False : BrocastcastTest %s'%(lan1.Ip))
    WriteLog('BroadcastTestCaseFinish')

def MultcastTestCase()->None:
    WriteLog('MuticastTestCaseStart')
    check = False
    lan1.SendNA(lan1.globallIP,1000)
    time.sleep(120)
    Token,refreshToken =AthenacAPI.GetLoginToken('admin','admin')
    mutidevices = AthenacAPI.GetMulicastDeviceList(Token)
    for ip,mac in mutidevices:
        if ip == lan1.globallIP[0] and mac == lan1MACUpper: check = True; break
    if not check:WriteLog('False : MultcastTestCase %s'%(lan1.globallIP))
    WriteLog('MuticastTestCaseFinish')
            
def OutofVLANTestCase()->None:
    WriteLog('OutofVLANTestCaseStart')
    check = False
    lan1.SendARPReply('10.1.1.87')
    time.sleep(10)
    Token,refreshToken =AthenacAPI.GetLoginToken('admin','admin')
    outofVLANDevices = AthenacAPI.GetOutofVLANList(Token)
    for ip,mac in outofVLANDevices:
        if ip == '10.1.1.87' and mac == lan1MACUpper: check = True; break
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
    Token,refreshToken =AthenacAPI.GetLoginToken('admin','admin')
    IPconflictdevices = AthenacAPI.GetIPconflictDeviceList(Token)
    for ip ,macs in IPconflictdevices:
        if ip == targetip and lan1MACUpper in macs and lan2MACUpper in macs:checkv4 = True; continue
        if ip == targetipv6 and lan1MACUpper in macs and lan2MACUpper in macs:checkv6 = True; continue
    if not checkv4 : WriteLog('False : IPconflictTestCase' + targetip )
    WriteLog('IPconflictTestCaseSFinish')

def  DHCPpressureTestCase()->None:
    WriteLog('DHCPpressureTestCaseStart')
    log = lan1.DHCPv4ClientTest(3)
    WriteLog(log)
    log = lan1.DHCPv6ClientTest(3)
    WriteLog(log)
    WriteLog('DHCPpressureTestCaseFinish')

lan1 = PacketAction('Ethernet1')
lan1MACUpper = ''.join(lan1.mac.upper().split(':'))
lan2 = PacketAction('Ethernet2')
lan2MACUpper = ''.join(lan2.mac.upper().split(':'))
serverIP='https://192.168.21.180:8001'
AthenacAPI = AthenacWebAPILibry(serverIP)

IPconflictTestCase()
OutofVLANTestCase()
BroadcastTesttCase()
MultcastTestCase()
UnknowDHCPTestCase()
DHCPpressureTestCase()