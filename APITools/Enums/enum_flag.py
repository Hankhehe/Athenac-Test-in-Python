from enum import Enum
class RadiusVLANMappingType(Enum):
    MAC = 1
    ACCOUNT = 2

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

class CustomFieldVerifyType(Enum):
    General = 0
    Guest = 1
    Staff = 2

class SendHostAgentType(Enum):
    Login = 0
    Logout = 1
    UnblockCRequest = 2
    BlockRequest = 3

class RegisterTypebyAutoRegist(Enum):
    Closed = 0
    Packet = 1
    VBS = 2

