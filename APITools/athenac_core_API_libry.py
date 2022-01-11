import requests,json,re,time
from requests_toolbelt.adapters.source import SourceAddressAdapter

class AthenacCoreAPILibry:
    def __init__(self,ServerIP:str,pixisprobeid:str,probedaemonId:str) -> None:
        self.ServerIP = ServerIP
        self.PixisProbeId = pixisprobeid
        self.ProbeDaemonId = probedaemonId
        self.retriesnum = 3

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

#region hostagent related

    def SendHostUserbyAgent(self,mac:str,domainname:str,remotetype:bool,sendtype:int)->None:
        mac = ''.join(re.split(':|-',mac)).upper()
        Data = {'HostName':'TestMachine'
        ,'MACs':[mac]
        ,'HostDomain':domainname
        ,'LogonUsers':[]
        ,'HostOSType':'Windows'
        ,'HostOSDesc':'Windows Test'
        ,'Timestamp':time.strftime('%Y-%m-%d'+'T'+'%H:%M:%S')}
        if sendtype == 0 :
            Path = '/HostAgent/UpdateHostLogonUser'
            Data['LogonUsers'] = [{'LogonAccount':f'{domainname}\\TestAccount','RemoteLogin':remotetype}]
        elif sendtype == 1 :
            Path = '/HostAgent/UpdateHostLogonUser'
        elif sendtype == 2:
            Path = '/HostAgent/HostUnblockRequest'
            Data['LogonUsers'] = [{'LogonAccount':f'{domainname}\\TestAccount','RemoteLogin':remotetype}]
        elif sendtype == 3:
            Path = '/HostAgent/HostBlockRequest'
            Data['LogonUsers'] = [{'LogonAccount':'Local\\TestAccount','RemoteLogin':remotetype}]
        else: return
        Header = {'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)  

    def SendKBNumberbyVBS(self,mac:str,ip:str,KBnumber:int,checktime:str=time.strftime('%Y/%m/%d'+' '+'%H:%M:%S'))->None:
        mac = ':'.join(re.split(':|-',mac)).upper()
        Path = '/Vbs/Gethotfix'
        Data = {'macs':mac,'Hotfixs':f'Hotfix Test - KB{str(KBnumber)}','IPList':ip,'HotfixLastCheckTime':checktime}
        Header = {'Content-type':'application/x-www-form-urlencoded'}
        requests.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
    
#endregion
