import time
from packet_action import PacketAction
from packet_action_test import PacketActionTest
# from PacketListen import PacketListen


testaction = PacketActionTest('Ethernet1')
testaction.SendRadiusCoARequest()
testaction.CalculateHashFromPacket()
# testaction.CalculateHashFromCustomerPacket()




# Action = PacketAction('Ethernet1')
# vlanid = Action.GetRadiusReply('192.168.21.180','192.168.10.249')
# print(vlanid)

pass