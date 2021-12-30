import threading,time,json,pytest_check as check
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from APITools.DataModels.datamodel_apidata import BlockMessageSetting, RadiusClient, RadiusSetting

class TestDHCP:
    def test_DHCPv4(self)->None:
        macint = 186916976721920
        for tranId in range(70):
            result =  lan1_.GetIPfromDHCPv4(tranId=tranId,mac=hex(macint)[2::])
            assert result,f'False : get IP fail by DHCPv4 at TranID {tranId}'
            macint +=1
            
    def test_DHCPv6(self)->None:
        macint = 186916976721920
        for tranId in range(300):
            result =  lan1_.GetIPfromDHCPv6(tranId=tranId,mac=hex(macint)[2::])
            assert result,f'False : get IPv6 fail by DHCPv6 at TranID {tranId}'
            macint +=1
    
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
