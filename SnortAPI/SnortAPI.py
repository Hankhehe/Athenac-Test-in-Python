import requests,json,os

pcapfiles = os.listdir('./SnortAPI/Pcap')
APIPath = 'http://192.168.10.12:8009/api/submit'
resultdata = {'Data':[]}

for pcapfile in pcapfiles:
    Files = {'file': open(f'SnortAPI/Pcap/{pcapfile}', 'rb')}
    Header = {'Content-type': 'application/json'}
    r = requests.post(APIPath,files=Files,verify=False)
    r = json.loads(r.text)
    r = r['analyses'][0]['alerts']
    print(f'Get {pcapfile} finished')

    for i in r:
        if i['priority'] == 1 :
            resultdata['Data'].append(i)
    print(f'filter {pcapfile} data finished')

with open('SnortAPI/ResultData.json','w') as f:
    f.write(json.dumps(resultdata,indent=4,ensure_ascii=False)) 
    pass