import time,json


class RadiusSetting:
    def __init__(self,SiteId:int,DeviceDivideType:int=2,EnableBlockMessageAndVerification:bool=True,EnableDynamicVLAN:bool=True,EnableExternalAutoQuarantine:bool=False
    ,EnableExternalOnlineVerification:bool=False,EnableInternalAutoQuarantine:bool=False,EnableInternalOnlineVerification:bool=False
    ,EnableRadius:bool=True,ExternalDefaultVLan:int=81,ExternalQuarantineVLan:int=85,ExternalVerifyVLan:int=83,InternalDefaultVLan:int=80
    ,InternalPreCheckVLan:int=86,InternalQuarantineVLan:int=84,InternalVerifyVLan:int=82,SiteVerifyModule:int=0,VLanMappingType:int=2) -> None:
        self.DeviceDivideType = DeviceDivideType
        self.EnableBlockMessageAndVerification = EnableBlockMessageAndVerification
        self.EnableDynamicVLAN = EnableDynamicVLAN
        self.EnableExternalAutoQuarantine = EnableExternalAutoQuarantine
        self.EnableExternalOnlineVerification = EnableExternalOnlineVerification
        self.EnableInternalAutoQuarantine = EnableInternalAutoQuarantine
        self.EnableInternalOnlineVerification = EnableInternalOnlineVerification
        self.EnableRadius = EnableRadius
        self.ExternalDefaultVLan = ExternalDefaultVLan
        self.ExternalQuarantineVLan = ExternalQuarantineVLan
        self.ExternalVerifyVLan = ExternalVerifyVLan
        self.InternalDefaultVLan = InternalDefaultVLan
        self.InternalPreCheckVLan = InternalPreCheckVLan
        self.InternalQuarantineVLan = InternalQuarantineVLan
        self.InternalVerifyVLan = InternalVerifyVLan
        self.SiteId = SiteId
        self.SiteVerifyModule = SiteVerifyModule
        self.VLanMappingType = VLanMappingType

class RadiusClient:
    def __init__(self,SiteId:int,RadiusAVPId:int,IP:str='0.0.0.0',SharedSecret:str='pixis',SubnetMask:str='0') -> None:
        self.IP= IP
        self.RadiusAVPId= RadiusAVPId
        self.SharedSecret= SharedSecret
        self.SiteId= SiteId
        self.SubnetMask= SubnetMask

class BlockMessageSetting:
    def __init__(self,EnableBlockNotify:bool,EnableVerifyModule:bool,ADverify:bool,DBverify:bool,LDAPverify:bool
    ,EnableTwoFactorAuthentication:bool = False,EnablePeriodAuth:bool = False,PeriodAuthDays:int = 1 ,EnableStaffLogin:bool=True
    ,EnableGuestLogin:bool=True,GuestAuthTempHours:int=2,EnableCustomAuthDate:bool=False) -> None:
        self.EnableBlockNotify = EnableBlockNotify
        self.BlockNotify ={'Title':'Automation test tittle','Content':'Automation test contect'}
        self.EnableVerifyModule = EnableVerifyModule
        self.VerifyModule = {
                'ADVerify':{'HasModule':ADverify,'Enable':ADverify}
                ,'DBVerify':{'HasModule':DBverify,'Enable':DBverify}
                ,'LDAPVerify':{'HasModule':LDAPverify,'Enable':LDAPverify}
                ,'EnableTwoFactorAuthentication':EnableTwoFactorAuthentication
                ,'EnablePeriodAuth':EnablePeriodAuth
                ,'PeriodAuthDays':PeriodAuthDays
                ,'EnableStaffLogin':EnableStaffLogin
                ,'EnableGuestLogin':EnableGuestLogin
                ,'GuestAuthTempHours':GuestAuthTempHours
                ,'EnableCustomAuthDate':EnableCustomAuthDate
                ,'Title':'Automation test account'
                ,'Content':'Automation Test text'
                }

class HostAgentClientInfo:
    def __init__(self,macs:list[str],hostName:str,domainname:str,ostype:str,osdesc:str,logonusers:list[dict]
    ,windowshotfixlastchecktime:str =time.strftime('%Y-%m-%d'+'T'+'%H:%M:%S'),pendinghotfix:list[str]=[],localadminaccount:list[str] =[],sharefolder:list[str]=[]) -> None:
        self.hostName = hostName 
        self.maCs = macs
        self.domainName = domainname
        self.logonusers = logonusers
        self.osType = ostype
        self.osDesc = osdesc
        self.shareFolder = sharefolder
        self.pendingHotFix = pendinghotfix
        self.windowsHotFixLastCheckTime = windowshotfixlastchecktime
        self.localAdminAccount = localadminaccount
        self.timestamp = time.strftime('%Y-%m-%d'+'T'+'%H:%M:%S')

class SettingConfigByTest:
    def __init__(self,jsonfilepath:str) -> None:
        with open(jsonfilepath,'r',encoding='UTF-8') as f:
            configdata = json.loads(f.read())
        self.serverIP:str = configdata['serverIP']
        self.APIaccount:str = configdata['APIaccount']
        self.APIPwd:str = configdata['APIpwd']
        self.TestIPv4:str = configdata['TestIPv4']
        self.TestIPv6:str = configdata['TestIPv6']
        self.ProbeMAC:str = configdata['ProbeMAC']
        self.VLANIDMapping:int = configdata['VLANIDMapping']
        self.SiteID:int = configdata['SiteId']
        self.DynamicAVPID:int = configdata['DynamicAVPID']
        self.AuthAVPID:int = configdata['AuthAVPID']
        self.lan1:str = configdata['lan1']
        self.lan2:str = configdata['lan2']
        self.probeID:str = configdata['probeID']
        self.daemonID:str = configdata['daemonID']

