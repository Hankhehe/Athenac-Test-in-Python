import requests,json,re,time,ipaddress
from urllib import parse
from CreateData import iprelated,macrelated
from APITools.DataModels.datamodel_apidata import RadiusSetting,RadiusClient,BlockMessageSetting
from requests_toolbelt.adapters.source import SourceAddressAdapter

class AthenacWebAPILibry:
    def __init__(self,ServerIP:str,Account:str,Pwd:bytes,nicip:str) -> None:
        self.ServerIP = ServerIP
        self.Account = Account
        self.Pwd = Pwd
        self.Token = ''
        self.FreshToken = ''
        self.retriesnum = 3
        self.APIsource = requests.Session()
        self.APIsource.mount('http://',SourceAddressAdapter(nicip))
        self.APIsource.mount('https://',SourceAddressAdapter(nicip))
        self.APIsource.trust_env=False
        self.GetLoginToken()

    def GetPortWorerkIPbyID(self,portworkerID:str)-> str | None:
        r = None
        path = '/api/Probes'
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP+path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return
        if r :
            r = json.loads(r.text)['Data'][0]['PortWorkers']
            for i in r :
                if str(i['PortWorkerId']) == portworkerID :
                    return i['CommunicationIP']    

    def GetLoginToken(self)-> None:
        Path = '/api/connect/token'
        Header = {'Content-Type': 'application/x-www-form-urlencoded' }
        FormData = {"grant_type": 'password','scope':'offline_access', 'username': self.Account, 'password': self.Pwd} 
        Data = parse.urlencode(FormData)
        r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
        r = json.loads(r.text)
        self.Token = 'Bearer '+ r['access_token']
        self.FreshToken ='Bearer ' + r['refresh_token']

    def DumpJson(self,Path:str)->None:
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP + Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return
        if r :
            r = json.loads(r.text)
            with open('Log.json','w') as f:
                f.write(json.dumps(r,indent=4,ensure_ascii=False))    

    def GetCustomerFieldInfo(self,Type:int)->dict | None:
        if Type > 3 : return 
        Path='/api/CustomFieldInfo?customFieldType='+str(Type)
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP + Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r :
            return json.loads(r.text)

#region IP Related
    def GetIPDetail(self,IP:str,siteid:int,IPv6Type:bool=False)->dict | None:
        if IPv6Type :
            Path = '/api/Hosts/Ipv6'
        else:
            Path = '/api/Hosts/Ipv4'
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'IpInfo.Ip','value':IP,'operator':'eq'}]}}
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r= self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401 :
                self.GetLoginToken()
            else: return
        if r :
            r=json.loads(r.text)['Data']
            for i in r:
                if int(i['IpInfo']['SiteId']) == siteid:
                    return {'IpAddressId':i['IpInfo']['IpAddressId']
                    ,'HostId':i['HostId']
                    ,'Isonline':i['IsOnline']
                    ,'IsGLBP':i['IsGLBP']
                    ,'IsRegisted':i['IpInfo']['IsRegisted']
                    ,'IsBlockByUnAuth':i['IpInfo']['BlockingStatus']['IsBlockByUnAuth']
                    ,'IsImportantIP':i['IpInfo']['IsImportantIP']
                    ,'SiteId':i['IpInfo']['SiteId']}

    def AuthIPv4(self,ip:str,auth:bool,siteid:int)->None:
        ipdata = self.GetIPDetail(ip,siteid)
        if not ipdata : return
        if auth:Path = f'/api/Hosts/AuthorizeIP/Host/{ipdata["HostId"]}'
        else: Path = f'/api/Hosts/UnAuthorizeIP/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def BlockIPv4(self,ip:str,block:bool,siteid:int)->None:
        ipdata = self.GetIPDetail(ip,siteid)
        if not ipdata : return
        if block: Path =f'/api/Hosts/BlockIp/V4/{ipdata["HostId"]}'
        else: Path = f'/api/Hosts/UnBlockIp/V4/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def CreateProtectIP(self,ip:str,mac:str,siteid:int,IPv6Type:bool=False)->None:
        mac = ''.join(re.split(':|-',mac)).upper()
        Path = '/api/Hosts/ProtectIpWithMac'
        macdata = self.GetIPDetail(ip,siteid,IPv6Type)
        if not macdata : return
        Data = {'HostId': macdata['HostId'], 'IP': ip, 'MAC': mac, 'IpCustomField': {}, 'MacCustomField': {}}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def GetProtectIPList(self,ip:str,siteid:int,IPv6Type:bool=False)->list[dict]:
        ipdata = self.GetIPDetail(ip,siteid,IPv6Type)
        if not ipdata : return []
        Path = f'/api/Hosts/IpProtection/Table/{ipdata["IpAddressId"]}'
        result = []
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
            r = json.loads(r.text)
            for i in r :
                result.append({'Id':i['Id'],'IP':i['IP'],'MAC':i['MAC']})
        return result

    def DelProtectIP(self,ip:str,siteid:int,IPv6Type:bool=False)->None:
        ipProtectionIds =self.GetProtectIPList(ip,siteid,IPv6Type)
        for ipProtectionId in ipProtectionIds:
            Path= f'/api/Hosts/IpProtection/Delete/{ipProtectionId["Id"]}'
            for retries in range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()

    def CreateBindingIP(self,ip:str,siteid:int,IPv6Type:bool=False)->None:
        ipdata = self.GetIPDetail(IP=ip,siteid=siteid,IPv6Type=IPv6Type)
        if not ipdata : return
        Path = f'/api/Hosts/AddMacBindingIp/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def DelIP(self,ip:str,siteid:int,IPv6Type:bool=False)->None:
        ipdata = self.GetIPDetail(ip,siteid,IPv6Type)
        if not ipdata : return
        Path = f'/api/Hosts/Delete/Ip/{ipdata["IpAddressId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

#endregion

#region MAC related
    def GetMACDetail(self,MAC:str,SiteId:int)->dict | None:
        Path = '/api/Hosts/Mac'
        MAC = ''.join(re.split(':|-',MAC)).upper()
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'Mac','value':MAC,'operator':'eq'}
                            ,{'field':'SiteId','value':SiteId,'operator':'eq'}]}}
        r = None
        for retriescount in range(self.retriesnum) :
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r= self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else:
                return
        if r:
            r=json.loads(r.text)['Data']
            for i in r:
                return {'MacAddressId':i['MacAddressId']
                ,'HostName':i['HostName']
                ,'HostWorkgroup':i['HostWorkgroup']
                ,'IsRegisteded':i['IsRegistered']
                ,'RegisterType':i['RegisterType']
                ,'RegisterUserId':i['RegisterUserId']
                ,'RegisterUserName':i['RegisterUserName']
                ,'IsIpBlockByUnAuth':i['IsIpBlockByUnAuth']
                ,'IsPrivileged':i['IsPrivileged']
                ,'IsOnline':i['IsOnline']
                ,'OSType':i['OSType']
                ,'SiteId':i['SiteId']}

    def AuthMAC(self,mac:str,auth:bool,siteid:int)->None:
        macdata = self.GetMACDetail(mac,siteid)
        if not macdata : return
        if auth: Path =f'/api/Hosts/AuthorizeMac/{macdata["MacAddressId"]}'
        else: Path =f'/api/Hosts/UnauthorizeMac/{macdata["MacAddressId"]}'
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else :
                return
    
    def BlockMAC(self,mac:str,block:bool,siteid:int)->None:
        macdata = self.GetMACDetail(mac,siteid)
        if not macdata : return
        if block: Path = f'/api/Hosts/BlockMac/{macdata["MacAddressId"]}'
        else: Path = f'/api/Hosts/UnblockMac/{macdata["MacAddressId"]}'
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else:
                return

    def SetPrecheckWhiteMAC(self,mac:str,white:bool,siteid:int)->None:
        macdata = self.GetMACDetail(MAC=mac,SiteId=siteid)
        if macdata and white:
            Path = f'/api/Hosts/SetPreCheckWhiteList/{macdata["MacAddressId"]}'
        elif macdata and not white:
            Path = f'/api/Hosts/CancelPreCheckWhiteList/{macdata["MacAddressId"]}'
        else: return
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def CheckPrecheckbyMAC(self,mac:str,siteid:int)->None:
        macdata = self.GetMACDetail(MAC=mac,SiteId=siteid)
        if macdata:
            Path = f'/api/Hosts/PreCheckManualDoWork/{macdata["MacAddressId"]}'
            for retriescount in range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()
            
    def DelMAC(self,mac:str,siteid:int)->None:
        mac = ''.join(re.split(':|-',mac)).upper()
        macdata = self.GetMACDetail(MAC=mac,SiteId=siteid)
        if not macdata: return
        Path = f'/api/Hosts/DeleteMacs/{macdata["MacAddressId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
                
#endregion 

#region Host Related

    def GetUsedHost(self,SiteId:int,isOnline:bool,IPv6type:bool=False) -> list[dict]:
        if IPv6type:
            Path = '/api/Hosts/Ipv6'
        else :
            Path = '/api/Hosts/Ipv4'
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'IsOnline','value':isOnline,'operator':'eq'}
                            ,{'field':'IpInfo.SiteId','value':SiteId,'operator':'eq'}
                                ,{"field": "MacInfo.MacAddressId","value": 1,"operator": "neq",}]}}
        result,r = [],None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else:
                return result
        if r :
            r = json.loads(r.text)['Data']
            for i in r :
                result.append({'HostId':i['HostId']
                ,'IsOnline':i['IsOnline']
                ,'IPSiteId':i['IpInfo']['SiteId']
                ,'IP':i['IpInfo']['Ip']
                ,'IPIsregisteded':i['IpInfo']['IsRegisted']
                ,'MAC':i['MacInfo']['Mac']
                ,'MacIsRegisteded':i['MacInfo']['IsRegistered']
                ,'HostName':i['MacInfo']['HostName']
                })
        return result

#endregion


#region abnormal network related

    def GetMulicastDeviceList(self)->list[dict]:
        Path='/api/BroadcastOverload/IPv6'
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header ={'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: 
                return result
        if r :
            r = json.loads(r.text)
            for i in r:
                result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result
    
    def GetOutofVLANList(self)->list[dict]:
        Path = '/api/OutOfVlan/Query'
        Data={'take':0}
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else:
                return result
        if r :
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result
    
    def GetIPconflictDeviceList(self)->list[dict]:
        Path = '/api/IpConflict/Query'
        Data={'take':0}
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'Ip':i['Ip'],'Macs':i['Macs']})
        return result

    def GetUnknowDHCPList(self)->list[dict]:
        Data={'take':0}
        Path = '/api/UnknownDhcpServer/Query'
        result = []
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'Ip':i['Ip'],'Mac':i['Mac'],'ServerType':i['ServerType']})
        return result
    
    def GetBrocastDeviceList(self)->list[dict]:
        Path='/api/BroadcastOverload/IPv4'
        result = []
        r = None
        for retriescount in range(self.retriesnum):
            Header ={'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
            r = json.loads(r.text)
            for i in r:
                result.append({'Ip':i['Ip'],'Mac':i['Mac']})
        return result

#endregion

#region 802.1X related

    def GetRadiusClientList(self,siteid:int)->list[dict]:
        Path = f'/api/Site/{str(siteid)}/RadiusClients'
        Data = {'take':0}
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'Id':i['Id']
                ,'IP':i['IP']
                ,'SubnetMask':i['SubnetMask']
                ,'RadiusAVPName':i['RadiusAVPName']
                ,'SharedSecret':i['SharedSecret']})
        return result
    
    def GetRadiusSetting(self,siteid:int)->dict | None:
        Path = f'/api/Site/{str(siteid)}/Radius'
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.get(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return
        if r :
            r = json.loads(r.text)
            return r
    
    def UpdateRadiusSetting(self,Data:RadiusSetting)->None:
        Path = '/api/Site/Radius'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def AddVLANMapping(self,name:str,Type:int,vlanid:int | None,siteid:int)->None:
        Path = '/api/Site/RadiusVLanMapping'
        
        Data = {"AssignVlan": vlanid, "MappingValue": name, "MappingValueType": Type, "SiteId": siteid}
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Data['Id']=vlanmappingdata['Id']
            for retriescount in range(self.retriesnum):
                Header = {'Authorization':self.Token,'Content-type': 'application/json'}
                r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()
        else:
            for retriescount in  range(self.retriesnum):
                Header = {'Authorization':self.Token,'Content-type': 'application/json'}
                r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()
    
    def ClearAllMappingatSite(self,siteid:int)->None:
        vlanmappings = self.GetVLANMappingList(siteid)
        for vlanmapping in vlanmappings:
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmapping["Id"])}'
            for retriescount in  range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = self.APIsource.delete(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()

    def DelVLANMapping(self,name:str,Type:int,siteid:int)->None:
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmappingdata["Id"])}'
            for retriescount in range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = self.APIsource.delete(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()
    
    def GetVLANMapping(self,name:str,Type:int,siteid:int)->dict | None:
        r = self.GetVLANMappingList(siteid)
        for i in r:
            if i['MappingValue'] == name and i['MappingValueType'] == Type: #Type 1 = MAC , 2 = Account
                return i
        return None
    
    def GetVLANMappingList(self,siteid:int)->list[dict]:
        Path = f'/api/Site/{str(siteid)}/VLanMapping'
        Data = {'take':0}
        r = None
        result = []
        for retriescount in range(self.retriesnum):   
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}     
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return result
        if r :
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
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def ClearAllRadiusClientatSite(self,siteid:int)->None:
        radiusclients = self.GetRadiusClientList(siteid)
        for radiuscilient in radiusclients:
            self.DelRadiusClient(radiuscilient['Id'])
             
    def DelRadiusClient(self,id:int)->None:
        Path = f'/api/Site/RadiusClient/{str(id)}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = self.APIsource.delete(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

#endregion

#region Policy setting related

    def SwitchMACSiteSaveMode(self,enable:bool,siteid:int)->None:
        Path = f'/api/Sites/{siteid}/ToggleMacSafeMode'
        for restiescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def SwitchIPSiteSaveMode(self,enable:bool,siteid:int)->None:
        Path= f'/api/Sites/{siteid}/ToggleIPv4SafeMode'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def SwitchSiteMonitMode(self,enable:bool,siteid:int)->None:
        Path = f'/api/Sites/{siteid}/ToggleMonitorMode'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code ==401:
                self.GetLoginToken()
    
    def UpdateBlockMessage(self,config:BlockMessageSetting,siteid:int)->None:
        # if not config.EnableVerifyModule: config.VerifyModule. ADverify,DBverify,LDAPverify = False,False,False
        Path = f'/api/Site/{siteid}/BlockMessage'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(config.__dict__),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def UpdateAutoRegister(self,registtype:int,siteid:int)->None:
        Path = f'/api/Site/{siteid}/AdAutoRegister'
        Data = {'ADAutoRegisterMode':registtype}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def AddDomainServerforAutoRegist(self,domainname:str,ip:str,siteid:int)->None:
        Path = '/api/Site/Domain'
        Data = {'Ip':ip,'Name':domainname,'SiteId':siteid,'URL':''}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def GetDomainServerListforAutoRegist(self,siteid)->list:
        Path = f'/api/Site/{siteid}/Domain'
        Data = {'take':0}
        result = []
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r :
            r = json.loads(r.text)['Data']
            for i in r :
                result.append({'Id':i['Id'],'Ip':i['Ip'],'Name':i['Name'],'SiteId':i['SiteId'],'URL':i['URL']})
        return result

    def DelDomainServerforAutoRegist(self,siteid:int,id:int)->None:
        Path = f'/api/Site/{siteid}/Domain/{id}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.delete(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def ClearAllDomainServerforAutoRegist(self,siteid:int)->None:
        domainservers = self.GetDomainServerListforAutoRegist(siteid=siteid)
        for domainserver in domainservers:
            self.DelDomainServerforAutoRegist(siteid=siteid,id=domainserver['Id'])

#endregion

#region site、network、range related

    def GetNetworkListbySite(self,siteid:int)->list:
        Path = f'/api/Networks/Query'
        r,filters,result = None,[],[]
        filters.append({'field':'SiteId','operator':'eq','value':siteid})
        Data = {'take':0,'filter':{'logic':'and','filters':filters}}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r:
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'NetworkId':i['NetworkId']
                ,'NetworkName':i['NetworkName']
                ,'SiteId':i['SiteId']
                ,'VlanID':i['VlanID']
                ,'PixisProbeId':i['PixisProbeId']
                ,'ProbeIp':i['ProbeIp']
                ,'IsEnableMonitorMode':i['IsEnableMonitorMode']
                ,'IsEnableDHCP':i['IsEnableDHCP']
                ,'IpDualStackRule':i['IpDualStackRule']})
        return result 

    def GetIPRangeInfoByName(self,RangeName:str) -> int | None:
        Path ='/api/IpRanges/V4'
        r = None
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.get(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else: return
        if r :
            r = json.loads(r.text)
            for i in r:
                if i['Name'] == RangeName:
                    return i['Id']

    def GetNetworkInfoByName(self,NetworkName:str)-> int | None :
        r = None
        Path = '/api/Networks/Query'
        Data = {'take':0}
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r :
            r = json.loads(r.text)['Data']
            for i in r :
                if i['NetworkName'] == NetworkName :
                    return i['NetworkId']

    def GetSiteInfoByName(self,SiteName:str) ->int | None:
        r = None
        Path = '/api/Sites/Query'
        Data = {'take':0}
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r :
            r = json.loads(r.text)['Data']
            for i in r :
                if i['SiteName'] == SiteName :
                    return i['SiteId']

    def AddNetwork(self,ProbeID:int,NetworkName,VLANID:int) -> None :
        Path = '/api/Networks/Create'
        Data = {"PixisProbeId": ProbeID,"NetworkName": NetworkName,"VlanId": VLANID}
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def DelNetwork(self,NetworkID:int) -> None:
        Path = f'/api/Networks/{NetworkID}'
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.delete(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def AddRange(self,mIP:str,gwIP:str,NetworkName:str) -> None :
        manageIP = str(mIP.split('/')[0])
        networkeIP = str(ipaddress.ip_interface(mIP).network)
        IPrange = ipaddress.IPv4Network(networkeIP)
        submask = str(IPrange.netmask)
        first,last = str(IPrange[1]),str(IPrange[-2])
        NetworkerId = self.GetNetworkInfoByName(NetworkName=NetworkName)
        Path = '/api/IpRanges/V4'
        Data = {"NetworkId": NetworkerId
        ,"Name": networkeIP
        ,"ManagementIp": manageIP
        ,"StartIp": first
        ,"EndIp": last
        ,"GatewayIp": gwIP
        ,"SubnetMask": submask}
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def AddDHCPool(self,RangeName:str,StartIP:str,EndIP:str) -> None:
        RangeID = self.GetIPRangeInfoByName(RangeName=RangeName)
        Path = '/api/DhcpPools'
        Data ={
                # "Id": 0,
                "IpRangeId": RangeID,
                "StartIp": StartIP,
                "EndIp": EndIP,
                "PoolType": 0,
                "EnableStaticIpBlock": False,
                "EnableOnlyAssignDHCPStaticIPPolicy": False
                }
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def AddDNSByNetwork(self,NetworkName:str,DNS1:str,DNS2:str,LeaseMinuteTime:int)-> None:
        NetWorkerID = self.GetNetworkInfoByName(NetworkName=NetworkName)
        Path = f'/api/Networks/{NetWorkerID}/DHCPv4Setting'
        Data = {
                "DNS1": DNS1,
                "DNS2": DNS2,
                "LeaseTimeInMinute": LeaseMinuteTime,
                "DhcpProxyServer": "",
                "VlanInformation": "",
                "AvayaOption": "",
                "CallServerInformation": ""
                }
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def EnablePortWorker(self,isTrunk:bool,VLANId:int,Enable:bool,PortWorkerID:str,ManageIPCIDR:str,Gateway:str) -> None:
        Path = f'/api/PortWorkers/{PortWorkerID}'
        Data = {
          "IsTrunkPort": isTrunk,
          "DefaultVlanId": VLANId,
          "PortWorkerId": int(PortWorkerID),
          "Name": PortWorkerID,
        #   "SiteId": SiteId,
          "Enable": Enable,
          "CommunicationIP": ManageIPCIDR.split('/')[0],
          "DefaultManagementIP": ManageIPCIDR,
          "DefaultGateway": Gateway,
        #   "Id": 15,
          "HasNetwork": False,
          "HasCommunicationIP": False
        }
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def ChangeSitePropertise(self,Threshold:int,siteID,SiteName:str='AutoTestSite') -> None:
        Path = f'/api/Site/{siteID}/Properties'
        Data = {'Name':SiteName,'Ipv4BroadcastLimit':Threshold,'Ipv6MulticastLimit':Threshold}
        for retirescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

#endregion

#region PreCheck related

    def CreatePrecheckRule(self,Data:dict)->None:
        Path = '/api/PreCheck/Create'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def CreateUnInstallKBforPrecheckRule(self,siteid:int,KBNumbers:list[int],filterOS:str|None=None,filterdomain:str|None=None)->None:
        netlist = self.GetNetworkListbySite(siteid=siteid)
        if netlist:
            netidlist = []
            for network in netlist:
                netidlist.append(network['NetworkId'])
        else : return
        filtercondition = []
        if filterOS:
            filtercondition.append({'Name':'MacAddress.OSType','Operator':0,'Value':filterOS})
        if filterdomain:
            filtercondition.append({'Name':'MacAddress.HostWorkgroup','Operator':0,'Value':filterdomain})
        KBNumCheck = []
        for i in KBNumbers:
            KBNumCheck.append({'ComparativeValue':'KB'+str(i),'CompareType':38,'PreCheckDataSource':0})
        precheckrule = [{'ThirdPartyInfoId':'Hotfix'
        ,'PreCheckRuleDetails':KBNumCheck
        ,'CustomFields':[]
        ,'PreCheckRuleType':0
        }]
        Data = {'EnableTime':time.strftime('%Y/%m/%d'+' '+'%H:%M:%S')
        ,'PreCheckRules':precheckrule
        ,'FilterConditionalList':filtercondition
        ,'NetworkIdList':netidlist
        ,'Name':'Uninstall KB ON VBS from test'}
        self.CreatePrecheckRule(Data=Data)

    def CreateHotfixforPrecheckRule(self,siteid:int,hotfixcount:int,checkday:int,filterOS:str|None=None,filterdomain:str|None=None)->None:
        netlist = self.GetNetworkListbySite(siteid=siteid)
        if netlist:
            netidlist = []
            for network in netlist:
                netidlist.append(network['NetworkId'])
        else : return
        filtercondition = []
        if filterOS:
            filtercondition.append({'Name':'MacAddress.OSType','Operator':0,'Value':filterOS})
        if filterdomain:
            filtercondition.append({'Name':'MacAddress.HostWorkgroup','Operator':0,'Value':filterdomain})
        precheckrule = [{'ThirdPartyInfoId':'HotfixRuleDetail'
        ,'PreCheckRuleDetails':[{'ComparativeValue':str(hotfixcount),'CompareType':18,'PreCheckDataSource':1}
        ,{'ComparativeValue':str(checkday),'CompareType':67,'PreCheckDataSource':2}]
        ,'CustomFields':[]
        ,'PreCheckRuleType':0
        }]
        Data = {'EnableTime':time.strftime('%Y/%m/%d'+' '+'%H:%M:%S')
        ,'PreCheckRules':precheckrule
        ,'FilterConditionalList':filtercondition
        ,'NetworkIdList':netidlist
        ,'Name':'hotfix on VBS from test'}
        self.CreatePrecheckRule(Data=Data)

    def GetPrecheckRuleList(self)->list:
        Path = '/api/PreCheck/Query'
        Data = {'Take':0}
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r:
            r = json.loads(r.text)['Data']
            for i in r:
                result.append({'Id':i['Id']
                ,'Name':i['Name']
                ,'SystemOrThirdPartyName':i['SystemOrThirdPartyName']
                ,'IsEnabled':i['IsEnabled']
                ,'EnableTime':i['EnableTime']
                })
        return result

    def DelPrecheckRule(self,precheckid:int)->None:
        Path = f'/api/PreCheck/Delete/{precheckid}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/x-www-form-urlencoded'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def ClearAllPrecheckRule(self)->None:
        precheckdatas = self.GetPrecheckRuleList()
        for precheckdata in precheckdatas:
            self.DelPrecheckRule(precheckid=precheckdata['Id'])

    def GetPrecheckDevice(self,precheckid:int)->list:
        Path = f'/api/PreCheck/PreviewAgainstRules/{precheckid}'
        Data = {'Take':0}
        r,result = None,[]
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = self.APIsource.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r:
            r = json.loads(r.text)['Data']
            for i in r :
                result.append({'MacAddressId':i['MacAddressId']
                ,'Mac':i['Mac']
                ,'HostName':i['HostName']
                ,'HostWorkgroup':i['HostWorkgroup']
                ,'OSType':i['OSType']
                ,'OSDetail':i['OSDetail']
                ,'SiteId':i['SiteId']
                ,'SiteName':i['SiteName']
                ,'IsOnline':i['IsOnline']
                })
        return result

#endregion 
