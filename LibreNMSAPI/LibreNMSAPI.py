from email.header import Header
import requests,json

class LibreNMSAPI:
    def __init__(self,ServerURL:str,Token:str) -> None:

        self.Token = Token
        self.ServerURL = ServerURL
        
    def GetAPIRoute(self) -> dict | None:
        Path = f'/api/v0'
        Header = {'Content-type':'application/json','X-Auth-Token':self.Token}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        if r.status_code == 200:
            return json.loads(r.text)
        else: return

    def GetDevice(self,Hostname:str| None = None) -> str: 
        if Hostname:
            Path = f'/api/v0/devices/{Hostname}'
        else:
            Path = f'/api/v0/devices'
        Header = {'Content-type':'application/json','X-Auth-Token':self.Token}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return r

    def GetAlert(self) -> dict:
        Path = f'/api/v0/alerts'
        Header = {'Content-type':'application/json','X-Auth-Token':self.Token}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return r
    
    def GetRule(self) -> dict:
        Path = f'/api/v0/rules'
        Header = {'Content-type':'application/json','X-Auth-Token':self.Token}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return r


admin_Token = 'a3b29560bd57878784019314e177652f'
LibreAPI174 = LibreNMSAPI(ServerURL='https://192.168.10.174',Token=admin_Token)

APIroute = LibreAPI174.GetAPIRoute()
with open('LibreNMSAPI/APIroute.json','w') as f:
    f.write(json.dumps(APIroute,indent=4,ensure_ascii=False))

deviceinfo = LibreAPI174.GetDevice()
with open('LibreNMSAPI/Devices.json','w') as f:
    f.write(json.dumps(deviceinfo,indent=4,ensure_ascii=False))

Alerts = LibreAPI174.GetAlert()
with open('LibreNMSAPI/Alerts.json','w') as f:
    f.write(json.dumps(Alerts,indent=4,ensure_ascii=False))

AlertRules = LibreAPI174.GetRule()
with open('LibreNMSAPI/AlertRule.json','w') as f:
    f.write(json.dumps(AlertRules,indent=4,ensure_ascii=False))
