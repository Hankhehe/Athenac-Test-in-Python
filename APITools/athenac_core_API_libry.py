import json,re,time,requests
from CreateData import macrelated
from requests_toolbelt.adapters.source import SourceAddressAdapter

class AthenacCoreAPILibry:
    def __init__(self,ServerIP:str,pixisprobeid:str,probedaemonId:str,nicip:str) -> None:
        self.ServerIP = ServerIP
        self.PixisProbeId = pixisprobeid
        self.ProbeDaemonId = probedaemonId
        self.retriesnum = 3
        self.APIsource = requests.Session()
        self.APIsource.mount('http://',SourceAddressAdapter(nicip))
        self.APIsource.mount('https://',SourceAddressAdapter(nicip))
        self.APIsource.trust_env=False

    def LoginProbeToServer(self,daemonip:str,mac:str) -> None:
        mac = macrelated.FormatMACbyPunctuation(mac=mac,Punctuation='')
        Path = '/DaemonReport/Login'
        Header = {'Content-type': 'application/json'}
        Data = {'ProbeDaemonId':self.ProbeDaemonId,'IpAddress':daemonip,'MacAddress':mac,'Ethernets':[{'Key':1,'Value':mac}]
        ,'DeviceType':'Linux','DaemonVersion':'9.9.9.9','PortWorkerVersion':'9.9.9.9'}
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

    def SendEventOfOnorOffline(self,ip:str,mac:str,vlanID:int,isonline:bool,isIPv6:bool=False) -> None:
        Path = '/PortWorkerReport'
        if isIPv6 :
            if isonline : actioncode = 774
            else : actioncode = 775
        else:
            if isonline : actioncode = 772
            else : actioncode = 773
        Header = {'PixisProbeId':self.PixisProbeId, 'ProbeDaemonId':self.ProbeDaemonId, 'Content-type': 'application/json'}
        hostobject = {'IsNewMacOnline':True,'IP':ip,'MAC':mac,'VLANID':vlanID,'ActionCode':actioncode}
        Data = {'ActionCode':actioncode,'IsValid':True,'Payload':None,'PayloadObject':hostobject,'SenderID':0}
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

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
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data) ,verify=False)

#region Abnormal

    def SendBroOrMulticastlimitevent(self,ip:str| None,mac:str,VLANID:int,start:bool,isIPv6:bool=False) -> None:
        Path = '/PortworkerReport'
        actioncode = 1028 #broadcast stop
        if start and not isIPv6: actioncode = 1027 #broadcast start
        elif start and isIPv6 : actioncode, ip = 1029, None #multi start
        elif not start and isIPv6 : actioncode, ip = 1030, None #multi stop
        Header = {'PixisProbeId':self.PixisProbeId, 'ProbeDaemonId':self.ProbeDaemonId, 'Content-type': 'application/json'}
        PayloadObj = {'ActionCode':actioncode
        ,'ExceededValue':6000
        ,'IP':ip
        ,'MAC':mac
        ,'VLANIDs':[VLANID]}
        Data = {'ActionCode':actioncode,'IsValid':True,'Payload':None,'PayloadObject':PayloadObj,'SenderID':0}
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

    def SendUnknowDHCP(self,ip:str,mac:str,VLANID:int,start:bool) -> None:
        Path = '/PortworkerReport'
        actioncode = 1032 # unknowDHCP stop
        if start : actioncode = 1031 # unknowDHCP start
        Header = {'PixisProbeId':self.PixisProbeId, 'ProbeDaemonId':self.ProbeDaemonId, 'Content-type': 'application/json'}
        PayloadObj = {'ActionCode':actioncode
        ,'RelayDHCPServerIP':None
        ,'LinkLayerAddress':None
        ,'IP':ip
        ,'MAC':mac
        ,'VLANID':VLANID}
        Data = {'ActionCode':actioncode,'IsValid':True,'Payload':None,'PayloadObject':PayloadObj,'SenderID':0}
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

#endregion Abnormal

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
        try:
            self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        except Exception:
            print('error 2')
    
    def SendGetAllMAC(self)->None:
        Path = '/HostAgent/GetAllProbeMACs'
        try:
            self.APIsource.get(self.ServerIP+Path,verify=False)
        except Exception:
            print('error')
            
    def SendKBNumberbyVBS(self,mac:str,ip:str,KBnumbers:list[int],checktime:str=time.strftime('%Y/%m/%d'+' '+'%H:%M:%S'))->None:
        mac = ':'.join(re.split(':|-',mac)).upper()
        Path = '/Vbs/Gethotfix'
        KBNum = []
        for i in KBnumbers:
            KBNum.append(f'Hotfix {str(i)} - KB{str(i)}')
        Data = {'macs':mac,'Hotfixs':KBNum,'IPList':ip,'HotfixLastCheckTime':checktime}
        Header = {'Content-type':'application/x-www-form-urlencoded'}
        self.APIsource.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
    
#endregion
