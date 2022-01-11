import threading,time,pytest_check as check,asyncio,re,json
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule,SendHostAgentType,RegisterTypebyAutoRegist
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest

def test_HotfixbyVBSOnHotfixCount()->None:
    AthenacWebAPI_.ClearAllPrecheckRule()
    AthenacWebAPI_.CreateHotfixforPrecheckRule(siteid=SiteID_,hotfixcount=0,checkday=15)
    prechecklist = AthenacWebAPI_.GetPrecheckRuleList()
    if prechecklist:
        precheckid = prechecklist[0]['Id']
    else:
        check.is_true(False,'Create fail at Precheckrule') 
        return
    AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[123456])
    AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
    illegaldevices =  AthenacWebAPI_.GetPrecheckDevice(precheckid=precheckid)
    checkflag = False
    for illegaldevice in illegaldevices:
        if illegaldevice['Mac'] == lan2MACUpper_ and illegaldevice['SiteId'] == SiteID_:
            checkflag = True
    check.is_true(checkflag,f'The MAC {lan2_.mac} is not illegalDevice by Precheck on Hotfix Count')
    AthenacWebAPI_.ClearAllPrecheckRule()

def test_HotfixbyVBSOnCheckDate()->None:
    AthenacWebAPI_.ClearAllPrecheckRule()
    AthenacWebAPI_.CreateHotfixforPrecheckRule(siteid=SiteID_,hotfixcount=2,checkday=15)
    prechecklist = AthenacWebAPI_.GetPrecheckRuleList()
    if prechecklist:
        precheckid = prechecklist[0]['Id']
    else:
        check.is_true(False,'Create fail at Precheckrule') 
        return
    checkdate = time.strftime('%Y/%m/%d'+' '+'%H:%M:%S',time.gmtime(time.time()-(60*60*24*30)))
    AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[123456])
    AthenacWebAPI_.CheckPrecheckbyMAC(mac=lan2_.mac,siteid=SiteID_)
    illegaldevices =  AthenacWebAPI_.GetPrecheckDevice(precheckid=precheckid)
    checkflag = False
    for illegaldevice in illegaldevices:
        if illegaldevice['Mac'] == lan2MACUpper_ and illegaldevice['SiteId'] == SiteID_:
            checkflag = True
    check.is_true(checkflag,f'The MAC {lan2_.mac} is not illegalDevice by Precheck on Check Date')
    AthenacWebAPI_.ClearAllPrecheckRule()


#------------------------------------------------------------------------------------------------------------------------------------
with open('settingconfig.json') as f:
    settingconfig_ = json.loads(f.read())
serverIP_ = settingconfig_['serverIP']
APIaccount_ = settingconfig_['APIaccount']
APIpwd_ = settingconfig_['APIpwd']
AthenacWebAPI_ = AthenacWebAPILibry(f'http://{serverIP_}:8000',APIaccount_,APIpwd_)
AthenacCoreAPI_ = AthenacCoreAPILibry(f'https://{serverIP_}:18000',settingconfig_['probeID'],settingconfig_['daemonID'])
AthenacCoreAPI18002_ = AthenacCoreAPILibry(f'http://{serverIP_}:18002',settingconfig_['probeID'],settingconfig_['daemonID'])
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

checkdate = time.strftime('%Y/%m/%d'+' '+'%H:%M:%S',time.gmtime(time.time()-(60*60*24*30)))
AthenacCoreAPI18002_.SendKBNumberbyVBS(mac=lan2_.mac,ip=lan2_.Ip,KBnumbers=[])
# test_HotfixbyVBSOnHotfixCount()
test_HotfixbyVBSOnCheckDate()