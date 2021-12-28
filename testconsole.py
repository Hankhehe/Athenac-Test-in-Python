import time
import socket
import datetime
from scapy import *
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest
import threading
import hashlib

for retriescount in range(3):
    print(f'aa')


WebAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
time.sleep(5)
WebAPI.Token = ''
WebAPI.AuthMAC(mac='005056AEAA69',auth=False,siteid=2)

print('Stop')