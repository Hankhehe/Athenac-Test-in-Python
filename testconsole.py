import time,pytest_check as check
from scapy import *
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest

lan1_ = PacketAction('Ethernet1')
macint = 186916976721920        
for tranId in range(70):
    result =  lan1_.GetIPfromDHCPv4(tranId=tranId,mac=hex(macint)[2::])
    assert result['Status'],f'Result False from tranid : {result["TranId"]}'
    macint +=1
pass

WebAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
time.sleep(5)
WebAPI.Token = ''
WebAPI.AuthMAC(mac='005056AEAA69',auth=False,siteid=2)

print('Stop')