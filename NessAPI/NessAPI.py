import requests,json

class NessesAPI:
    def __init__(self,ServerURL:str,Account:str,Pwd:str) -> None:
        self.ServerURL = ServerURL
        self.Token = self.GetToken(account=Account,pwd=Pwd)

    def GetToken(self,account:str,pwd:str) -> str: 
        Path = '/session'
        Header = {'Content-type':'application/json'}
        Data = {'username':account,'password':pwd}
        r = requests.post(self.ServerURL+Path,headers=Header,data=json.dumps(Data),verify=False)
        r = json.loads(r.text)
        return r['token']

    def GetscanDetail(self,scanID:int=5) -> dict:
        Path = f'/scans/{scanID}'
        Header = {'Content-type':'application/json','X-Cookie':f'token={self.Token}'}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return r

    def GetHostDetailbyScan(self,HostID:int,scanID:int=5) -> dict:
        Path = f'/scans/{scanID}/hosts/{HostID}'
        Header = {'Content-type':'application/json','X-Cookie':f'token={self.Token}'}
        r = requests.get(self.ServerURL+Path,headers=Header,verify=False)
        r = json.loads(r.text)
        return r

NessAPI12 = NessesAPI(ServerURL='https://192.168.10.12:8834',Account='admin',Pwd='111aaaBBB')
scanDetail = NessAPI12.GetscanDetail()

with open('NessAPI/scanDetail.json','w') as f:
    f.write(json.dumps(scanDetail,indent=4,ensure_ascii=False))

HostIDs = [x['host_id'] for x in [i for i in scanDetail['hosts']]]
for i in HostIDs:
    hostDetail =NessAPI12.GetHostDetailbyScan(HostID=i)
    with open(f'NessAPI/scanHost_{i}_Detail.json','w') as f:
        f.write(json.dumps(hostDetail,indent=4,ensure_ascii=False))

