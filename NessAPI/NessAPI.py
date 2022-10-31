import requests,json

def GetToken(account:str,pwd:str) -> str: 
    Url = 'https://192.168.10.12:8834/session'
    Header = {'Content-type':'application/json'}
    Data = {'username':account,'password':pwd}
    r = requests.post(Url,headers=Header,data=json.dumps(Data),verify=False)
    r = json.loads(r.text)
    return r['token']

def GetscanDetail(token:str,scanID:int=5) -> dict:
    Url = f'https://192.168.10.12:8834/scans/{scanID}'
    Header = {'Content-type':'application/json','X-Cookie':f'token={token}'}
    r = requests.get(Url,headers=Header,verify=False)
    r = json.loads(r.text)
    return r

def GetHostDetailbyScan(token:str,HostID:int,scanID:int=5) -> dict:
    Url = f'https://192.168.10.12:8834/scans/{scanID}/hosts/{HostID}'
    Header = {'Content-type':'application/json','X-Cookie':f'token={token}'}
    r = requests.get(Url,headers=Header,verify=False)
    r = json.loads(r.text)
    return r

tokenkey = GetToken(account='admin',pwd='111aaaBBB')
scanDetail = GetscanDetail(token=tokenkey)
with open('NessAPI/scanDetail.json','w') as f:
    f.write(json.dumps(scanDetail,indent=4,ensure_ascii=False))

HostIDs = [x['host_id'] for x in [i for i in scanDetail['hosts']]]

for i in HostIDs:
    hostDetail =GetHostDetailbyScan(token=tokenkey,HostID=i)
    with open(f'NessAPI/scanHost_{i}_Detail.json','w') as f:
        f.write(json.dumps(hostDetail,indent=4,ensure_ascii=False))

