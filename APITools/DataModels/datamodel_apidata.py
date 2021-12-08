class RadiusSetting:
    def __init__(self,SiteId:int,DeviceDivideType:int=2,EnableDynamicVLAN:bool=True,EnableExternalAutoQuarantine:bool=False
    ,EnableExternalOnlineVerification:bool=False,EnableInternalAutoQuarantine:bool=False,EnableInternalOnlineVerification:bool=False
    ,EnableRadius:bool=True,ExternalDefaultVLan:int=81,ExternalQuarantineVLan:int=85,ExternalVerifyVLan:int=83,InternalDefaultVLan:int=80
    ,InternalQuarantineVLan:int=84,InternalVerifyVLan:int=82,SiteVerifyModule:int=0,VLanMappingType:int=2) -> None:
        self.DeviceDivideType = DeviceDivideType
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
