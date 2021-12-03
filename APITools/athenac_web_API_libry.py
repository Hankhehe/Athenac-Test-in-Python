import requests
import json
from urllib import parse
import time
import threading
from APITools.DataModels.datamodel_apidata import RadiusSetting,RadiusClient
from NetPacketTools.packet_action import PacketAction

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
        Data={'take':0}
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
        Data={'take':0}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result
    
    def GetIPconflictDeviceList(self)->list[dict]:
        Path = '/api/IpConflict/Query'
        Data={'take':0}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Ip':i['Ip'],'Macs':i['Macs']})
        return result
    
    def GetMACDetail(self,MAC:str,Isonline:bool,SiteId:int)->list[dict]:
        Path = '/api/Hosts/Mac'
        Data = {'take':0,"filter":{'logic':'and'
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
        Data = {'take':0,"filter":{'logic':'and'
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
    
    def AuthMAC(self,macid:int,auth:bool)->None:
        if auth: Path ='/api/Hosts/AuthorizeMac/'+str(macid)
        else: Path ='/api/Hosts/UnauthorizeMac/'+str(macid)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def AuthIP(self,hostid:int,Auth:bool)->None:
        if Auth:Path = '/api/Hosts/AuthorizeIP/Host/'+str(hostid)
        else: Path = '/api/Hosts/UnAuthorizeIP/'+str(hostid)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)
    
    def BlockMAC(self,macid:int,block:bool)->None:
        if block: Path = '/api/Hosts/BlockMac/'+str(macid)
        else: Path = '/api/Hosts/UnblockMac/'+str(macid)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def BlockIPv4(self,hostid:int,block:bool)->None:
        if block: Path ='/api/Hosts/BlockIp/V4/'+str(hostid)
        else: Path = '/api/Hosts/UnBlockIp/V4/'+str(hostid)
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def GetRadiusClientList(self,siteid:int=1)->list[dict]:
        Path = f'/api/Site/{str(siteid)}/RadiusClients'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        Data = {'take':0}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'Id':i['Id']
            ,'IP':i['IP']
            ,'SubnetMask':i['SubnetMask']
            ,'RadiusAVPName':i['RadiusAVPName']
            ,'SharedSecret':i['SharedSecret']})
        return result
    
    def GetRadiusSetting(self,siteid:int=1)->dict:
        Path = f'/api/Site/{str(siteid)}/Radius'
        Header = {'Authorization':self.Token}
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r:RadiusSetting = json.loads(r.text)
        return r
    
    def UpdateRadiusSetting(self,Data:RadiusSetting=RadiusSetting())->None:
        Path = '/api/Site/Radius'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
    
    def AddVLANMapping(self,name:str,Type:int,vlanid:int =None,siteid:int=1)->None:
        Path = '/api/Site/RadiusVLanMapping'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        Data = {"AssignVlan": vlanid, "MappingValue": name, "MappingValueType": Type, "SiteId": siteid}
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Data['Id']=vlanmappingdata['Id']
            requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        else:
            requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
    
    def ClearAllMappingatSite(self,siteid:int=1)->None:
        vlanmappings = self.GetVLANMappingList(siteid)
        for vlanmapping in vlanmappings:
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmapping["Id"])}'
            Header = {'Authorization':self.Token}
            requests.delete(self.ServerIP+Path,headers=Header,verify=False)

    def DelVLANMapping(self,name:str,Type:int,siteid:int =1)->None:
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmappingdata["Id"])}'
            Header = {'Authorization':self.Token}
            requests.delete(self.ServerIP+Path,headers=Header,verify=False)
    
    def GetVLANMapping(self,name:str,Type:int,siteid:int=1)->dict:
        r = self.GetVLANMappingList(siteid)
        for i in r:
            if i['MappingValue'] == name and i['MappingValueType'] == Type: #Type 1 = MAC , 2 = Account
                return i
    
    def GetVLANMappingList(self,siteid:int=1)->list[dict]:
        Path = f'/api/Site/{str(siteid)}/VLanMapping'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        Data = {'take':0}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)['Data']
        for i in r:
            result.append({'AssignVlan':i['AssignVlan']
                        ,'Id':i['Id']
                        ,'MappingValue':i['MappingValue']
                        ,'MappingValueType':i['MappingValueType']
                        ,'SiteId':i['SiteId']
                        ,'SiteName':i['SiteName']})
        return result

    def AddRadiusClient(self,Data:RadiusClient=RadiusClient())->None:
        Path = '/api/Site/RadiusClient'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
    
    def ClearAllRadiusClientatSite(self,siteid:int=1)->None:
        radiusclients = self.GetRadiusClientList(1)
        for radiuscilient in radiusclients:
            self.DelRadiusClient(radiuscilient['Id'])
             
    def DelRadiusClient(self,id:int)->None:
        Path = f'/api/Site/RadiusClient/{str(id)}'
        Header = {'Authorization':self.Token}
        requests.delete(self.ServerIP+Path,headers=Header,verify=False)

    def SwitchMACSiteSafeMode(self,enable:bool,siteid:int=1)->None:
        Path = f'/api/Sites/{siteid}/ToggleMacSafeMode'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
    
    def SwitchIPSiteSafeMode(self,enable:bool,siteid:int=1)->None:
        Path= f'/api/Sites/{siteid}/ToggleIPv4SafeMode'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)