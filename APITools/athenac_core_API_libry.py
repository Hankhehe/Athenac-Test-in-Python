import enum
import requests
import json

class AthenacCoreAPILibry:
    def __init__(self,ServerIP:str,pixisprobeid:str,probedaemonId:str) -> None:
        self.ServerIP = ServerIP
        self.PixisProbeId = pixisprobeid
        self.ProbeDaemonId = probedaemonId

    def AuthMACFromUserApply(self,ip:str,mac:str,account:str,pwd:str)->None:
        adname = account
        # if verifytype != 1 : adname = None
        Path = '/PortworkerReport'
        Header = {'PixisProbeId':self.PixisProbeId, 'ProbeDaemonId':self.ProbeDaemonId, 'Content-type': 'application/json'}
        authdata = {'ActionCode':2305
        ,'IP':ip
        ,'UserID':account
        ,'UserPassword':pwd
        ,'GuestApplyInfoList':[]
        ,'DbVerifyCustomFieldList':None
        ,'UserEnableGuestLogin':False
        ,'CustomAuthDate':None
        ,'AdName':account
        ,'StaffApplyInfoList':[]
        ,'MAC':mac
        ,'customFieldVerifyType':2
        ,'EnableMailVaildation':False
        ,'SiteVerifyModule':0}
        Data = {'ActionCode':2305, 'IsValid':True, 'Payload':None, 'PayloadObject':authdata,'SenderID':0}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data) ,verify=False)