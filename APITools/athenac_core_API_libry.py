import requests
import json

class AthenacCoreAPILibry:
    def __init__(self,ServerIP:str,pixisprobeid:str,probedaemonId:str) -> None:
        self.ServerIP = ServerIP
        self.PixisProbeId = pixisprobeid
        self.ProbeDaemonId = probedaemonId

    def AuthMACFromApply(self,ip:str,mac:str)->None:
        Path = '/PortworkerReport'
        Header = {'PixisProbeId':self.PixisProbeId, 'ProbeDaemonId':self.ProbeDaemonId, 'Content-type': 'application/json'}
        authdata = {'ActionCode':2305
        ,'IP':ip
        ,'UserID':'admin'
        ,'UserPassword':'36IqJwCHVwl9IS4w4b1mMw=='
        ,'GuestApplyInfoList':[]
        ,'DbVerifyCustomFieldList':None
        ,'UserEnableGuestLogin':False
        ,'CustomAuthDate':None
        ,'AdName':None
        ,'StaffApplyInfoList':[]
        ,'MAC':mac
        ,'customFieldVerifyType':2
        ,'EnableMailVaildation':False
        ,'SiteVerifyModule':0}
        Data = {'ActionCode':2305, 'IsValid':True, 'Payload':None, 'PayloadObject':authdata,'SenderID':0}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data) ,verify=False)