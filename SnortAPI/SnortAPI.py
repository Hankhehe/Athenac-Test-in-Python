import requests,json


Files = {'file': open('SnortAPI/1.pcap', 'rb')}
Header = {'Content-type': 'application/json'}
r = requests.post('http://192.168.10.12:8009/api/submit',files=Files,verify=False)
r = json.loads(r.text)
resultdata = {'Data':[]}
ay = r['analyses'][0]['alerts']
for i in ay:
    if i['priority'] == 2:
        resultdata['Data'].append(i)
with open('SnortAPI/snortData.json','w') as f:
    f.write(json.dumps(resultdata,indent=4,ensure_ascii=False)) 
pass