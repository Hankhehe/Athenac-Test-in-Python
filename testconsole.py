import threading,time,pytest_check as check,asyncio,re,json
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule,SendHostAgentType,RegisterTypebyAutoRegist
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest


WebAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
# WebAPI.CreateUnInstallKB(siteid=2,filterOS='Windows',filterdomain='PIXIS')
# WebAPI.ClearAllPrecheckRule()
# WebAPI.DelPrecheckRule(precheckid=17)
pass

coreAPI = AthenacCoreAPILibry('http://192.168.21.180:18002','11','22')
Mac = '005056AEAA69'
Domain = 'PIXIS'
coreAPI.SendHostUserbyAgent(mac = Mac,domainname=Domain,remotetype=False,sendtype=SendHostAgentType.Login.value)
coreAPI.SendHostUserbyAgent(mac = Mac,domainname=Domain,remotetype=False,sendtype=SendHostAgentType.UnblockCRequest.value)
# coreAPI.SendHotfixbyvbs(mac='005056AEAA69',ip='192.168.25.11')
pass



#------------------------------------------------------------------------------------------------------------------------------------
with open('settingconfig.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = settingconfig_['APIpwd']
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
AthenacCoreAPI18002 = AthenacCoreAPILibry(f'http://{serverIP_}:18002',settingconfig_['probeID'],settingconfig_['daemonID'])
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


# AthenacWebAPI_.UpdateAutoRegister(registtype=RegisterTypebyAutoRegist.VBS.value,siteid=SiteID_)
# AthenacWebAPI_.ClearAllDomainServerforAutoRegist(siteid=SiteID_)
# AthenacWebAPI_.AddDomainServerforAutoRegist(domainname='PIXIS',ip='192.168.10.201',siteid=SiteID_)
AthenacCoreAPI18002.SendHostUserbyAgent(mac=lan2_.mac,domainname='PIXIS',remotetype=False,sendtype=SendHostAgentType.Login.value)
pass