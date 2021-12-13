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




WebAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
lan2 = PacketAction('Ethernet2')
time.sleep(5)
check =   lan2.NDPBlockCheck(srcIP=lan2.linklocalIp,dstIP=lan2.gatewatIpv6,ProbeMAC='00:aa:ff:ae:2b:a1')
print(check)


# WebAPI.SwitchSiteMonitMode(enable=False,siteid=1)