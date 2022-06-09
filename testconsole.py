import threading,time,asyncio,re,json,requests,base64,pytest_check as check
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.athenac_probe_API_libry import AthenacProbeAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule,SendHostAgentType,RegisterTypebyAutoRegist
from APITools.DataModels.datamodel_apidata import BlockMessageSetting, RadiusClient, RadiusSetting,HostAgentClientInfo
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_listen_RadiusProxy import PacketListenRadiusProxy
from NetPacketTools.packet_action_test import PacketRelated8021X
from CreateData import iprelated,macrelated


#region memo
#測試 Radius Proxy
# listen1 = PacketListenRadiusProxy('192.168.10.235','192.168.10.201',1812,'Ethernet1')
# listen1.Sniffer('udp and port 1812',60*60*24)
# pass


#發送 IPv4 衝突
#Send IP Conflict Packet
# lan2_ = PacketAction('Ethernet2')

# while True:
#     lan2_.SendARPReply(IP='172.17.255.87',MAC='AA0000000000')
#     lan2_.SendARPReply(IP='172.17.255.87',MAC='AA0000000001')
#     # lan2_.SendARPReply(IP='172.17.255.87',MAC='AA0000000002')
#     time.sleep(2)

# pass

# def SendOnline() ->None:
#     ipv4list = iprelated.CreateIPDataByCIDROrPrifix(cidr='172.17.0.0/17')
#     ipv6list = iprelated.CreateIPDataByCIDROrPrifix(cidr='2001:b030:2133:811::/112')
#     maclist = macrelated.CreateMACData(mac='AA0000000000',count=32768)
#     while True :
#         starttime = time.time()
#         for i in range(1,5002):
#             lan2_.SendARPReply(IP=str(ipv4list[i]),MAC=maclist[i])
#             lan2_.SendNA(IP=str(ipv6list[i]),MAC=maclist[i])
#         print(str(time.time()-starttime) + '---------------------------------end----------------------------------------------')

#發送大量上線 (非同步)
# async def test_onlinebyAsync():
#     for i in range(1,10):
#         tasks = asyncio.create_task(AthenacCoreAPI_.SendEventOfOnorOfflinebyAsync(ip=str(ipv4list[i]),mac=maclist[i],vlanID=17,isonline=False))
#         tasks = asyncio.create_task(AthenacCoreAPI_.SendEventOfOnorOfflinebyAsync(ip=str(ipv6list[i]),mac=maclist[i],vlanID=17,isonline=False,isIPv6=True))
#         print(f'count:{i}')
#     await tasks  # type: ignore


# asyncio.run(test_onlinebyAsync())

#endregion


#------------------------------------------------------------------------------------------------------------------------------------
with open('settingconfig_Hank.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = base64.b64encode(settingconfig_['APIpwd'].encode('UTF-8'))
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'http://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
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
#------------------------------------------------------------------------------------------------------------------------------------





