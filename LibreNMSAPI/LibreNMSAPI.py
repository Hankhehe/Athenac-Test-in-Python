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

admin_Token = 'a3b29560bd57878784019314e177652f'
LibreAPI174 = LibreNMSAPI(ServerURL='https://192.168.10.174',Token=admin_Token)

APIroute = LibreAPI174.GetAPIRoute()
deviceinfo = LibreAPI174.GetDevice()

with open('LibreNMSAPI/APIroute.json','w') as f:
    f.write(json.dumps(APIroute,indent=4,ensure_ascii=False))
with open('LibreNMSAPI/Devices.json','w') as f:
    f.write(json.dumps(deviceinfo,indent=4,ensure_ascii=False))
