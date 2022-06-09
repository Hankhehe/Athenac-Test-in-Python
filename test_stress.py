import json,time,threading
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry


class TestDHCP:
    def test_DHCPv4(self)->None:
        macint = 186916976721920
        for tranId in range(210):
            result =  lan2_.GetIPfromDHCPv4(tranId=tranId,mac=hex(macint)[2::])
            assert result,f'False :DHCP ID : {tranId} gets IPv4 fail'
            macint +=1

    def test_DHCPv6(self)->None:
        macint = 186916976721920
        for tranId in range(300):
            result =  lan2_.GetIPfromDHCPv6(tranId=tranId,mac=hex(macint)[2::])
            assert result,f'False :DHCPv6 ID : {tranId} gets IPv6 fail'
            macint +=1

class TestLotOfDevice:
    def test_SendIPv4Online(self)-> None:
        iplist = iprelated.CreateIPDataByCIDROrPrifix(cidr=f'{".".join(str.split(lan2_.Ip,".")[0:2]) + ".0.0"}/24')
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(iplist))
        for i in range(1,len(iplist)-1):
            lan2_.SendARPReply(IP=iplist[i],MAC=maclist[i])
        time.sleep(120)
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=SiteID_,isOnline=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(iplist)):
            if str(iplist[i]) in onlineHostsdict :
                assert onlineHostsdict[str(iplist[i])] == maclist[i],f'{str(iplist[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(iplist[i])]}'
            else : assert False,f'it do not found IP {str(iplist[i])} in hosts as online'
    
    def test_SendIPv6Online(self) -> None:
        ipv6list = iprelated.CreateIPDataByCIDROrPrifix(cidr=f'{":".join(str.split(lan2_.globalIp,":")[0:4]) + "::"}/120')
        maclist = macrelated.CreateMACData(mac='AA0000000000',count=len(ipv6list))
        for i in range(1,len(ipv6list)-1):
            lan2_.SendNA(IP=ipv6list[i],MAC=maclist[i])
        time.sleep(120)
        onlineHostslist = AthenacWebAPI_.GetUsedHost(SiteId=SiteID_,isOnline=True,IPv6type=True)
        onlineHostsdict = {}
        for i in onlineHostslist :
            onlineHostsdict[i['IP']] = i['MAC']
        for i in range(1,len(ipv6list)):
            if str(ipv6list[i]) in onlineHostsdict :
                assert onlineHostsdict[str(ipv6list[i])] == maclist[i],f'{str(ipv6list[i])} MAC is not {maclist[i]},it is {onlineHostsdict[str(ipv6list[i])]}'
            else : assert False,f'it do not found IP {str(ipv6list[i])} in hosts as online'

with open('settingconfig_Hank.json') as f:
    settingconfig_ = json.loads(f.read())
lan1_ = PacketAction(settingconfig_['lan1'])
lan2_ = PacketAction(settingconfig_['lan2'])
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = settingconfig_['APIpwd']
AthenacWebAPI_ = AthenacWebAPILibry(f'https://{serverIP_}:8001',APIaccount_,APIpwd_)
SiteID_ = settingconfig_['SiteId']