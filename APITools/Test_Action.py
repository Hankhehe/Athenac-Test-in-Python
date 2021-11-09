import json


#讀取 json 儲存 Filter  所有 API Path
with open('swagger.json',encoding='utf-8') as f:
    Data = json.load(f)
with open('APIPaths.txt','w') as f:
    for i in Data['paths'].keys():
        f.write('\''+i+'\''+'\n')