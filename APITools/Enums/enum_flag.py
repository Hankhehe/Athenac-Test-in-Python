from enum import Enum
class RadiusVLANMappingType(Enum):
    MAC:int = 1
    ACCOUNT:int = 2

class SiteVerifyModule(Enum):
    Close = 0
    EnableADVerify = 1
    EnableBlockNotify = 2
    EnableDbVerify = 3
    EnableLdapVerify = 4
    EnableAdAndDbVerify = 5
    EnableDbAndLdapVerify = 6
    EnableAdAndLdapVerify = 7
    EnableAdAndDbAndLdapVerify = 8