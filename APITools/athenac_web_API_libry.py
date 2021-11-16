import requests
import json
from urllib import parse
import time
import threading

class AthenacWebAPILibry:
    def __init__(self,ServerIP:str,Account:str,Pwd:str) -> None:
        self.ServerIP = ServerIP
        self.Account = Account
        self.Pwd = Pwd
        self.Token = ''
        self.FreshToken = ''
        t = threading.Thread(target=self.GetLoginToken)
        t.start()

    def GetLoginToken(self)-> None:
        while True:
            Path = '/api/connect/token'
            Header = {'Content-Type': 'application/x-www-form-urlencoded' }
            FormData = {"grant_type": 'password','scope':'offline_access', 'username': self.Account, 'password': self.Pwd} 
            Data = parse.urlencode(FormData)
            r = requests.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
            r = json.loads(r.text)
            self.Token = 'Bearer '+ r['access_token']
            self.FreshToken ='Bearer ' + r['refresh_token']
            time.sleep(1700)

    def DumpJson(self,Path:str)->None:
        Header = {'Authorization':self.Token}
        r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
        r = json.loads(r.text)
        with open('Log.json','w') as f:
            f.write(json.dumps(r,indent=4,ensure_ascii=False))    

    def GetCustomerFieldInfo(self,Type:int=0)->json:
        if Type > 3 : return 'Unknow Type'
        Path='/api/CustomFieldInfo?customFieldType='+str(Type)
        Header = {'Authorization':self.Token}
        r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
        return json.loads(r.text)
    
    def GetUnknowDHCPList(self)->list[dict]:
        Data={'take':100}
        Path = '/api/UnknownDhcpServer/Query'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Ip':i['Ip'],'Mac':i['Mac'],'ServerType':i['ServerType']})
        return result
    
    def GetBrocastDeviceList(self)->list[dict]:
        Path='/api/BroadcastOverload/IPv4'
        Header ={'Authorization':self.Token}
        result = []
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r:
            result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result

    def GetMulicastDeviceList(self)->list[dict]:
        Path='/api/BroadcastOverload/IPv6'
        Header ={'Authorization':self.Token}
        result = []
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r:
            result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result
    
    def GetOutofVLANList(self)->list[dict]:
        Path = '/api/OutOfVlan/Query'
        Data={'take':100}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result
    
    def GetIPconflictDeviceList(self)->list[dict]:
        Path = '/api/IpConflict/Query'
        Data={'take':100}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Ip':i['Ip'],'Macs':i['Macs']})
        return result
    
    def GetMACDetail(self,MAC:str,Isonline:bool,SiteId:int)->list[dict]:
        Path = '/api/Hosts/Mac'
        Data = {'take':100,"filter":{'logic':'and'
        ,'filters':[
            {'field':'Mac','value':MAC,'operator':'eq'}
            ,{'field':'IsOnline','value':str(Isonline),'operator':'eq'}
            ,{'field':'SiteId','value':SiteId,'operator':'eq'}]}}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result=[]
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            result.append({'MacAddressId':i['MacAddressId']
            ,'IsRegisteded':i['IsRegisteded']
            ,'HostName':i['HostName']
            ,'HostWorkgroup':i['HostWorkgroup']
            ,'IsPrivileged':i['IsPrivileged']
            ,'OSType':i['OSType']})
        return result
    
    def GetIPv4Detail(self,IP:str,Isonline:bool)->list[dict]:
        Path = '/api/Hosts/Ipv4'
        Data = {'take':100,"filter":{'logic':'and'
        ,'filters':[
            {'field':'IpInfo.Ip','value':IP,'operator':'eq'}
            ,{'field':'IsOnline','value':str(Isonline),'operator':'eq'}
            ]}}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result=[]
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            result.append({'IpAddressId':i['IpInfo']['IpAddressId']
            ,'HostId':i['HostId']
            ,'IsBlockByUnAuth':not i['IpInfo']['BlockingStatus']['IsBlockByUnAuth']
            ,'SiteId':i['MacInfo']['SiteId']})
        return result
    
    def AuthMAC(self,MacID:int,Auth:bool)->None:
        if Auth: Path ='/api/Hosts/AuthorizeMac/'+str(MacID)
        else: Path ='/api/Hosts/UnauthorizeMac/'+str(MacID)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def AuthIP(self,HostId:int,Auth:bool)->None:
        if Auth:Path = '/api/Hosts/AuthorizeIP/Host/'+str(HostId)
        else: Path = '/api/Hosts/UnAuthorizeIP/'+str(HostId)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)
    
    def BlockMAC(self,MacID:str,Block:bool)->None:
        if Block: Path = '/api/Hosts/BlockMac/'+str(MacID)
        else: Path = '/api/Hosts/UnblockMac/'+str(MacID)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def BlockIPv4(self,HostID:str,Block:bool)->None:
        if Block: Path ='/api/Hosts/BlockIp/V4/'+str(HostID)
        else: Path = '/api/Hosts/UnBlockIp/V4/'+str(HostID)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def GetRadiusClientSetting(self,SiteId:str)->list[dict]:
        Path = f'/api/Site/{str(SiteId)}/RadiusClients'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        Data = {'take':10}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'IP':i['IP']
            ,'SubnetMask':i['SubnetMask']
            ,'RadiusAVPName':i['RadiusAVPName']
            ,'SharedSecret':i['SharedSecret']})
        return result
    
    def GetDynamicSetting(self,SiteId:str)->dict:
        Path = f'/api/Site/{str(SiteId)}/Radius'
        Header = {'Authorization':self.Token}
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return {'DeviceDivideType':r['DeviceDivideType']
        ,'EnableDynamicVLAN':r['EnableDynamicVLAN']
        ,'EnableExternalAutoQuarantine':r['EnableExternalAutoQuarantine']
        ,'EnableExternalOnlineVerification':r['EnableExternalOnlineVerification']
        ,'EnableInternalAutoQuarantine':r['EnableInternalAutoQuarantine']
        ,'EnableInternalOnlineVerification':r['EnableInternalOnlineVerification']
        ,'EnableRadius':r['EnableRadius']
        ,'ExternalDefaultVLan':r['ExternalDefaultVLan']
        ,'ExternalQuarantineVLan':r['ExternalQuarantineVLan']
        ,'ExternalVerifyVLan':r['ExternalVerifyVLan']
        ,'InternalDefaultVLan':r['InternalDefaultVLan']
        ,'InternalQuarantineVLan':r['InternalQuarantineVLan']
        ,'InternalVerifyVLan':r['InternalVerifyVLan']
        ,'SiteId':r['SiteId']
        ,'SiteVerifyModule':r['SiteVerifyModule']
        ,'VLanMappingType':r['VLanMappingType']
        ,'EnableBlockMessageAndVerification':r['EnableBlockMessageAndVerification']}


