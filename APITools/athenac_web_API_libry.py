import requests,json,re
from urllib import parse
from APITools.DataModels.datamodel_apidata import RadiusSetting,RadiusClient,BlockMessageSetting

class AthenacWebAPILibry:
    def __init__(self,ServerIP:str,Account:str,Pwd:str) -> None:
        self.ServerIP = ServerIP
        self.Account = Account
        self.Pwd = Pwd
        self.Token = ''
        self.FreshToken = ''
        self.retriesnum = 3
        self.GetLoginToken()

    def GetLoginToken(self)-> None:
        Path = '/api/connect/token'
        Header = {'Content-Type': 'application/x-www-form-urlencoded' }
        FormData = {"grant_type": 'password','scope':'offline_access', 'username': self.Account, 'password': self.Pwd} 
        Data = parse.urlencode(FormData)
        r = requests.post(self.ServerIP+Path,headers=Header,data=Data,verify=False)
        r = json.loads(r.text)
        self.Token = 'Bearer '+ r['access_token']
        self.FreshToken ='Bearer ' + r['refresh_token']

    def DumpJson(self,Path:str)->None:
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
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
            r = requests.get(self.ServerIP + Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
        if r :
            return json.loads(r.text)

#region IP Related
    def GetIPv4Detail(self,IP:str,siteid:int)->dict | None:
        Path = '/api/Hosts/Ipv4'
        Data = {'take':0,"filter":{'logic':'and'
                    ,'filters':[
                        {'field':'IpInfo.Ip','value':IP,'operator':'eq'}]}}
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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

    def AuthIP(self,ip:str,auth:bool,siteid:int)->None:
        ipdata = self.GetIPv4Detail(ip,siteid)
        if not ipdata : return
        if auth:Path = f'/api/Hosts/AuthorizeIP/Host/{ipdata["HostId"]}'
        else: Path = f'/api/Hosts/UnAuthorizeIP/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def BlockIPv4(self,ip:str,block:bool,siteid:int)->None:
        ipdata = self.GetIPv4Detail(ip,siteid)
        if not ipdata : return
        if block: Path =f'/api/Hosts/BlockIp/V4/{ipdata["HostId"]}'
        else: Path = f'/api/Hosts/UnBlockIp/V4/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def CreateProtectIP(self,ip:str,mac:str,siteid:int)->None:
        mac = ''.join(re.split(':|-',mac)).upper()
        Path = '/api/Hosts/ProtectIpWithMac'
        macdata = self.GetIPv4Detail(ip,siteid)
        if not macdata : return
        Data = {'HostId': macdata['HostId'], 'IP': ip, 'MAC': mac, 'IpCustomField': {}, 'MacCustomField': {}}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def GetProtectIPList(self,ip:str,siteid:int)->list[dict]:
        ipdata = self.GetIPv4Detail(ip,siteid)
        if not ipdata : return []
        Path = f'/api/Hosts/IpProtection/Table/{ipdata["IpAddressId"]}'
        result = []
        r = None
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
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

    def DelProtectIP(self,ip:str,siteid:int)->None:
        ipProtectionIds =self.GetProtectIPList(ip,siteid)
        for ipProtectionId in ipProtectionIds:
            Path= f'/api/Hosts/IpProtection/Delete/{ipProtectionId["Id"]}'
            for retries in range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()

    def CreateBindingIP(self,ip:str,siteid:int)->None:
        ipdata = self.GetIPv4Detail(IP=ip,siteid=siteid)
        if not ipdata : return
        Path = f'/api/Hosts/AddMacBindingIp/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def DelIP(self,ip:str,siteid:int)->None:
        ipdata = self.GetIPv4Detail(ip,siteid)
        if not ipdata : return
        Path = f'/api/Hosts/Delete/Ip/{ipdata["HostId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
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
            r= requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
                ,'IsRegisteded':i['IsRegisteded']
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
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
            else:
                return

    def DelMAC(self,mac:str,siteid:int)->None:
        mac = ''.join(re.split(':|-',mac)).upper()
        macdata = self.GetMACDetail(MAC=mac,SiteId=siteid)
        if not macdata: return
        Path = f'/api/Hosts/DeleteMacs/{macdata["MacAddressId"]}'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token}
            r = requests.post(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
                
#endregion 

#region abnormal network related

    def GetMulicastDeviceList(self)->list[dict]:
        Path='/api/BroadcastOverload/IPv6'
        r = None
        result = []
        for retriescount in range(self.retriesnum):
            Header ={'Authorization':self.Token}
            r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.get(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
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
                r = requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()
        else:
            for retriescount in  range(self.retriesnum):
                Header = {'Authorization':self.Token,'Content-type': 'application/json'}
                r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
                r = requests.delete(self.ServerIP+Path,headers=Header,verify=False)
                if r.status_code == 200:
                    break
                elif r.status_code == 401:
                    self.GetLoginToken()

    def DelVLANMapping(self,name:str,Type:int,siteid:int)->None:
        if vlanmappingdata:= self.GetVLANMapping(name,Type,siteid):
            Path = f'/api/Site/RadiusVLanMapping/{str(vlanmappingdata["Id"])}'
            for retriescount in range(self.retriesnum):
                Header = {'Authorization':self.Token}
                r = requests.delete(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data.__dict__),verify=False)
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
            r = requests.delete(self.ServerIP+Path,headers=Header,verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def SwitchIPSiteSaveMode(self,enable:bool,siteid:int)->None:
        Path= f'/api/Sites/{siteid}/ToggleIPv4SafeMode'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def SwitchSiteMonitMode(self,enable:bool,siteid:int)->None:
        Path = f'/api/Sites/{siteid}/ToggleMonitorMode'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps({'Value':enable}),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code ==401:
                self.GetLoginToken()
    
    def UpdateBlockMessage(self,config:BlockMessageSetting,siteid:int)->None:
        # if not config.EnableVerifyModule: config.VerifyModule. ADverify,DBverify,LDAPverify = False,False,False
        Path = f'/api/Site/{siteid}/BlockMessage'
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(config.__dict__),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def UpdateAutoRegister(self,registtype:int,siteid:int)->None:
        Path = f'/api/Site/{siteid}/AdAutoRegister'
        Data = {'ADAutoRegisterMode':registtype}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.put(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()

    def AddDomainServerforAutoRegist(self,domainname:str,ip:str,siteid:str)->None:
        Path = '/api/Site/Domain'
        Data = {'Ip':ip,'Name':domainname,'SiteId':siteid,'URL':''}
        for retriescount in range(self.retriesnum):
            Header = {'Authorization':self.Token,'Content-type': 'application/json'}
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
            r = requests.post(self.ServerIP+Path,headers=Header,data=json.dumps(Data),verify=False)
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
        Header = {'Authorization':self.Token,'Content-type': 'application/json'}
        for retriescount in range(self.retriesnum):
            r = requests.delete(self.ServerIP+Path,headers=Header,verify=False)
            if r.status_code == 200:
                break
            elif r.status_code == 401:
                self.GetLoginToken()
    
    def ClearAllDomainServerforAutoRegist(self,siteid:int)->None:
        domainservers = self.GetDomainServerListforAutoRegist(siteid=siteid)
        for domainserver in domainservers:
            self.DelDomainServerforAutoRegist(siteid=siteid,id=domainserver['Id'])

#endregion

    

