import requests
import json
from urllib import parse
import time
import threading

from requests.api import head
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

    def GetCustomerFieldInfo(self,Type:int)->json:
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
    
    def GetMACDetail(self,MAC:str,SiteId:int)->list[dict]:
        Path = '/api/Hosts/Mac'
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'Mac','value':MAC,'operator':'eq'}
                            ,{'field':'SiteId','value':SiteId,'operator':'eq'}]}}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result=[]
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            result.append({'MacAddressId':i['MacAddressId']
            ,'HostName':i['HostName']
            ,'HostWorkgroup':i['HostWorkgroup']
            ,'IsRegisteded':i['IsRegisteded']
            ,'RegisterType':i['RegisterType']
            ,'IsIpBlockByUnAuth':i['IsIpBlockByUnAuth']
            ,'IsPrivileged':i['IsPrivileged']
            ,'IsOnline':i['IsOnline']
            ,'OSType':i['OSType']
            ,'SiteId':i['SiteId']})
        return result
    
    def GetIPv4Detail(self,IP:str,siteid:int)->list[dict]:
        Path = '/api/Hosts/Ipv4'
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'IpInfo.Ip','value':IP,'operator':'eq'}]}}
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        result=[]
        r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        r=json.loads(r.text)['Data']
        for i in r:
            if int(i['IpInfo']['SiteId']) == siteid:
                result.append({'IpAddressId':i['IpInfo']['IpAddressId']
                ,'HostId':i['HostId']
                ,'Isonline':i['IsOnline']
                ,'IsGLBP':i['IsGLBP']
                ,'IsRegisted':i['IpInfo']['IsRegisted']
                ,'IsBlockByUnAuth':i['IpInfo']['BlockingStatus']['IsBlockByUnAuth']
                ,'IsImportantIP':i['IpInfo']['IsImportantIP']
                ,'SiteId':i['IpInfo']['SiteId']})
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

    def GetRadiusClientList(self,siteid:int)->list[dict]:
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
    
    def GetRadiusSetting(self,siteid:int)->dict:
        Path = f'/api/Site/{str(siteid)}/Radius'
        Header = {'Authorization':self.Token}
        r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
        r:RadiusSetting = json.loads(r.text)
        return r
    
    def UpdateRadiusSetting(self,Data:RadiusSetting)->None:
        Path = '/api/Site/Radius'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
    
    def AddVLANMapping(self,name:str,Type:int,vlanid:int,siteid:int)->None:
        Path = '/api/Site/RadiusVLanMapping'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        Data = {"AssignVlan": vlanid, "MappingValue": name, "MappingValueType": Type, "SiteId": siteid}
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Data['Id']=vlanmappingdata['Id']
            requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
        else:
            requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
    
    def ClearAllMappingatSite(self,siteid:int)->None:
        vlanmappings = self.GetVLANMappingList(siteid)
        for vlanmapping in vlanmappings:
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmapping["Id"])}'
            Header = {'Authorization':self.Token}
            requests.delete(self.ServerIP+Path,headers=Header,verify=False)

    def DelVLANMapping(self,name:str,Type:int,siteid:int)->None:
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmappingdata["Id"])}'
            Header = {'Authorization':self.Token}
            requests.delete(self.ServerIP+Path,headers=Header,verify=False)
    
    def GetVLANMapping(self,name:str,Type:int,siteid:int)->dict:
        r = self.GetVLANMappingList(siteid)
        for i in r:
            if i['MappingValue'] == name and i['MappingValueType'] == Type: #Type 1 = MAC , 2 = Account
                return i
    
    def GetVLANMappingList(self,siteid:int)->list[dict]:
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

    def AddRadiusClient(self,Data:RadiusClient)->None:
        Path = '/api/Site/RadiusClient'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
    
    def ClearAllRadiusClientatSite(self,siteid:int)->None:
        radiusclients = self.GetRadiusClientList(siteid)
        for radiuscilient in radiusclients:
            self.DelRadiusClient(radiuscilient['Id'])
             
    def DelRadiusClient(self,id:int)->None:
        Path = f'/api/Site/RadiusClient/{str(id)}'
        Header = {'Authorization':self.Token}
        requests.delete(self.ServerIP+Path,headers=Header,verify=False)

    def SwitchMACSiteSaveMode(self,enable:bool,siteid:int)->None:
        Path = f'/api/Sites/{siteid}/ToggleMacSafeMode'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
    
    def SwitchIPSiteSaveMode(self,enable:bool,siteid:int)->None:
        Path= f'/api/Sites/{siteid}/ToggleIPv4SafeMode'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
    
    def CreateProtectIP(self,ip:str,mac:str,siteid:int)->None:
        Path = '/api/Hosts/ProtectIpWithMac'
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        hostid = self.GetIPv4Detail(ip,siteid)[0]['HostId']
        Data = {'HostId': hostid, 'IP': ip, 'MAC': mac, 'IpCustomField': {}, 'MacCustomField': {}}
        requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
    
    def GetProtectIPDetail(self,ip:str,siteid:int)->list[dict]:
        ipAddressId = self.GetIPv4Detail(ip,siteid)[0]['IpAddressId']
        Path = f'/api/Hosts/IpProtection/Table/{ipAddressId}'
        Header = {'Authorization':self.Token}
        result = []
        r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        for i in r :
            result.append({'Id':i['Id'],'IP':i['IP'],'MAC':i['MAC']})
        return result

    def DelProtectIP(self,ip:str,siteid:int)->None:
        ipProtectionIds =self.GetProtectIPDetail(ip,siteid)
        Header = {'Authorization':self.Token}
        for ipProtectionId in ipProtectionIds:
            Path= f'/api/Hosts/IpProtection/Delete/{ipProtectionId["Id"]}'
            requests.post(self.ServerIP+Path,headers=Header,verify=False)

    def DelIP(self,ip:str,siteid:int)->None:
        hostIds = self.GetIPv4Detail(ip,siteid)[0]['HostId']
        Path = f'/api/Hosts/Delete/Ip/{hostIds}'
        Header = {'Authorization':self.Token}
        requests.post(self.ServerIP+Path,headers=Header,verify=False)
