import time
from AthenacWebAPILibry import AthenacWebAPILibry

ServerIP='https://192.168.21.180:8001'
Action = AthenacWebAPILibry(ServerIP)

#Get login Token
token,refretoken = Action.GetLoginToken('admin','admin')

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




