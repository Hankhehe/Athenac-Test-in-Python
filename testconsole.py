import time
import datetime
from scapy import *
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest
import threading
import hashlib

# cryptokey = b'WeArePIXIS_WeArePIXIS_WeArePIXIS'
# key = hashlib.sha256(cryptokey).digest()
# iv =  hashlib.md5(cryptokey).digest()
# print(type(key))
# print(type(iv))
# print(key.decode())
# print(iv.decode())
# pass

Action = AthenacCoreAPILibry('https://192.168.21.180:18000')
Action.AuthMACFromApply()
pass

# CoATest= PacketActionTest()
# CoATest.SendRadiusCoARequest()
# CoATest.CalculateHashFromPacket()
# pass


# listen = PacketListenFromFilter('Ethernet1')
# # listen.Sniffer('udp and port 3799')
# t1 = threading.Thread(target=listen.Sniffer,args=['udp and port 3799',1700])
# t1.start()
# time.sleep(5)
# while listen.radiuspackets:
#     listen.radiuspackets.pop(0)


# a= radiuspacket[0]['packet'].attributes[1].value
# print(a)




# while True:
#     print('TCP Total : ',len(listen.tcp))
#     print('UDP Total : ',len(listen.udp))
#     print('ICMP Total : ',len(listen.icmp))
#     print('Other Total : ',len(listen.other))
#     time.sleep(5)
#     pass





# AthenacAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
# time.sleep(3)
# AthenacAPI.ClearAllMappingatSite()

