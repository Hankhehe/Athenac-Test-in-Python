# import requests_async
import json,re,time,requests
from CreateData import macrelated

class AthenacCoreAPILibry:
    def __init__(self,ServerIP:str,pixisprobeid:str,probedaemonId:str) -> None:
        self.ServerIP = ServerIP
        self.PixisProbeId = pixisprobeid
        self.ProbeDaemonId = probedaemonId
        self.retriesnum = 3

    def LoginProbeToServer(self,daemonip:str,mac:str) -> None:
        mac = macrelated.FormatMACbyPunctuation(mac=mac,Punctuation='')
        Path = '/DaemonReport/Login'
        Header = {'Content-type': 'application/json'}
        Data = {'ProbeDaemonId':self.ProbeDaemonId,'IpAddress':daemonip,'MacAddress':mac,'Ethernets':[{'Key':1,'Value':mac}]
        ,'DeviceType':'Linux','DaemonVersion':'9.9.9.9','PortWorkerVersion':'9.9.9.9'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

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
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

    async def SendEventOfOnorOfflinebyAsync(self,ip:str,mac:str,vlanID:int,isonline:bool,isIPv6:bool=False) -> None:
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
        await requests_async.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)

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
        try:
            requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        except Exception:
            print('error 2')
    
    def SendGetAllMAC(self)->None:
        Path = '/HostAgent/GetAllProbeMACs'
        try:
            requests.get(self.ServerIP+Path,verify=False)
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
        requests.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
    
#endregion
