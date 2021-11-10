import time
from AthenacWebAPILibry import AthenacWebAPILibry

ServerIP='https://192.168.21.180:8001'
Action = AthenacWebAPILibry(ServerIP)

#Get login Token
token,refretoken = Action.GetLoginToken('admin','admin')

#get MAC Detail
MacData = Action.GetIPv4Detail(IP='192.168.21.189',Token=token,Isonline= False)
#Action.AuthMAC(token,MacData[0][0],True)
pass
#i['MacAddressId'],i['IsRegisteded'],i['HostName'],i['HostWorkgroup'],i['IsPrivileged'],i['OSType']
for macid,regist,HostName,HostWorkgroup,IsPrivileged,OSType in MacData:
    print(f'MacID : {macid} | Regist : {regist} | HostName : {HostName} | HostWorkgroup : {HostWorkgroup} | IsPrivileged : {IsPrivileged} | OSType : {OSType}')

#Get OutofVLAN DeviceList
# OutofVLANData = Action.GetOutofVLANList(token)


#Get Ip conflict
# print(Action.GetIPconflictDeviceList(token))

#Get lot Broadcast and Multcast DeviceList 
#print(Action.GetBrocastDeviceList(token))
#print(Action.GetMulicastDeviceList(token))

#print(Action.GetCustomerFieldInfo(token))

#Get IP、MAC From UnknownDHCPList
# print(Action.GetUnknowDHCPList(token))

#Action.DumpJson(Token=token,Path='/api/VerifyModule/AdVerify')

time.sleep(300)




