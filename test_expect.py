import threading,time,datetime,codecs,json,pytest_check as check
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListenFromFilter
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from APITools.DataModels.datamodel_apidata import BlockMessageSetting, RadiusClient, RadiusSetting

class TestIPAM:
    def test_IPBlockCase(self)->None:
            AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=True,siteid=SiteID_)
            time.sleep(10)
            check.is_true(lan2_.ARPBlockCheck(lan2_.Ip,lan2_.gatewayIp,ProbeMAC_),f'False : Not Receive ARP {lan2_.Ip}')
            lan2_.SendARPReply(IP=TestIPv4_,Count=2,WaitSec=2)
            check.is_false(lan2_.ARPBlockCheck(TestIPv4_,lan2_.gatewayIp,ProbeMAC_),f'False : Recive ARP Rqply {TestIPv4_} by Change IP')
            AthenacWebAPI_.BlockIPv4(ip=lan2_.Ip,block=False,siteid=SiteID_)

class cancelTest:
    def calceltest_func(self):
        check.is_true(False,'error 1-1')
        check.is_true(True,'error 1-2')

    def canceltest_func2(self):
        check.is_true(True,'error 2-1')
        check.is_true(True,'error 2-2')

class CancelTest2:
    def canceltest_func3(self):
        check.is_true(False,'error 1-1')
        check.is_true(True,'error 1-2')

    def canceltest_func4(self):
        check.is_true(True,'error 2-1')
        check.is_true(True,'error 2-2')

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
