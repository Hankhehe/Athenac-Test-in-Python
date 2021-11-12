import time
from AthenacWebAPILibry import AthenacWebAPILibry

ServerIP='https://192.168.21.180:8001'
Action = AthenacWebAPILibry(ServerIP)

#Get login Token
token,refretoken = Action.GetLoginToken('admin','admin')

#Get MAC Detail and Block/Unblock MAC
# MacData = Action.GetMACDetail(MAC='005056AEAA69',Token=token,Isonline= True,SiteId=1)
# Action.BlockMAC(Token=token,MacID=MacData[0][0],Block=True)
# Action.BlockMAC(Token=token,MacID=MacData[0][0],Block=False)

#Get IP Detial and Block/Unblock IP
# IPData = Action.GetIPv4Detail(IP='192.168.21.11',Token=token,Isonline= True)
# Action.BlockIPv4(Token=token,HostID=IPData[0][1],Block=True)
# Action.BlockIPv4(Token=token,HostID=IPData[0][1],Block=False)


#Print i['MacAddressId'],i['IsRegisteded'],i['HostName'],i['HostWorkgroup'],i['IsPrivileged'],i['OSType']
# for macid,regist,HostName,HostWorkgroup,IsPrivileged,OSType in MacData:
#     print(f'MacID : {macid} | Regist : {regist} | HostName : {HostName} | HostWorkgroup : {HostWorkgroup} | IsPrivileged : {IsPrivileged} | OSType : {OSType}')

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




