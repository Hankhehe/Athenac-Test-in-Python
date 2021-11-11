from os import write
import requests
import json
from urllib import parse

class AthenacWebAPILibry:
    def __init__(self,ServerIP) -> None:
        self.ServerIP = ServerIP

    def GetLoginToken(self,account:str,pwd:str)->str:
        Path = '/api/connect/token'
        Header = {'Content-Type': 'application/x-www-form-urlencoded' }
        FormData = {"grant_type": 'password','scope':'offline_access', 'username': account, 'password': pwd} 
        Data = parse.urlencode(FormData)
        r = requests.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
        r = json.loads(r.text)
        return 'Bearer '+ r['access_token'],'Bearer ' + r ['refresh_token']
    
    def GetCustomerFieldInfo(self,Token:str,Type:int=0)->list:
        if Type > 3 : return 'Unknow Type'
        result = []
        Path='/api/CustomFieldInfo?customFieldType='+str(Type)
        Header = {'Authorization':Token}
        r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r:
            result.append([i['Name'],i['ColumnName'],i['FieldType']])
        return result
    
    def GetUnknowDHCPList(self,Token:str)->list:
        Data={'take':100}
        result=[]
        Path = '/api/UnknownDhcpServer/Query'
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append([i['Ip'],i['Mac'],i['ServerType']])
        return result
    
    def GetBrocastDeviceList(self,Token:str)->list:
        Path='/api/BroadcastOverload/IPv4'
        result=[]
        Header ={'Authorization':Token}
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r:
            result.append([i['Ip'],i['Mac']])
        return result

    def GetMulicastDeviceList(self,Token:str)->list:
        Path='/api/BroadcastOverload/IPv6'
        result=[]
        Header ={'Authorization':Token}
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r:
            result.append([i['Ip'],i['Mac']])
        return result
    
    def GetOutofVLANList(self,Token:str)->list:
        Path = '/api/OutOfVlan/Query'
        Data={'take':100}
        result=[]
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append([i['Ip'],i['Mac']])
        return result
    
    def GetIPconflictDeviceList(self,Token:str)->list:
        Path = '/api/IpConflict/Query'
        Data={'take':100}
        result=[]
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append([i['Ip'],i['Macs']])
        return result
    
    def GetMACDetail(self,Token:str,MAC:str,Isonline:bool,SiteId:int)->list:
        Path = '/api/Hosts/Mac'
        Data = {'take':100,"filter":{'logic':'and'
        ,'filters':[
            {'field':'Mac','value':MAC,'operator':'eq'}
            ,{'field':'IsOnline','value':str(Isonline),'operator':'eq'}
            ,{'field':'SiteId','value':SiteId,'operator':'eq'}]}}
        result=[]
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            result.append([i['MacAddressId'],i['IsRegisteded'],i['HostName'],i['HostWorkgroup'],i['IsPrivileged'],i['OSType']])
        return result
    
    def GetIPv4Detail(self,Token:str,IP:str,Isonline:bool)->list:
        Path = '/api/Hosts/Ipv4'
        Data = {'take':100,"filter":{'logic':'and'
        ,'filters':[
            {'field':'IpInfo.Ip','value':IP,'operator':'eq'}
            ,{'field':'IsOnline','value':str(Isonline),'operator':'eq'}
            ]}}
        result=[]
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            result.append([i['IpInfo']['IpAddressId'],i['HostId'],not i['IpInfo']['BlockingStatus']['IsBlockByUnAuth'],i['MacInfo']['SiteId']])
        return result
    
    def AuthMAC(self,Token:str,MacID:int,Auth:bool)->None:
        if Auth: Path ='/api/Hosts/AuthorizeMac/'+str(MacID)
        else: Path ='/api/Hosts/UnauthorizeMac/'+str(MacID)
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def AuthIP(self,Token:str,HostId:int,Auth:bool)->None:
        if Auth:Path = '/api/Hosts/AuthorizeIP/Host/'+str(HostId)
        else: Path = '/api/Hosts/UnAuthorizeIP/'+str(HostId)
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)
    
    def BlockMAC(self,Token:str,MacID:str,Block:bool)->None:
        if Block: Path = '/api/Hosts/BlockMac/'+str(MacID)
        else: Path = '/api/Hosts/UnblockMac/'+str(MacID)
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def BlockIPv4(self,Token:str,HostID:str,Block:bool)->None:
        if Block: Path ='/api/Hosts/BlockIp/V4/'+str(HostID)
        else: Path = '/api/Hosts/UnBlockIp/V4/'+str(HostID)
        Header = {'Authorization':Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def DumpJson(self,Token:str,Path:str)->None:
        result = []
        Header = {'Authorization':Token}
        r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
        r = json.loads(r.text)
        with open('Log.json','w') as f:
            f.write(json.dumps(r,indent=4,ensure_ascii=False))
