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
time.sleep(5)
count = 1
while True:
    print(f'enable {count}')
    WebAPI.SwitchMACSiteSaveMode(enable=True,siteid=1)
    print(f'unable {count}')
    WebAPI.SwitchMACSiteSaveMode(enable=False,siteid=1)
pass
# WebAPI.SwitchSiteMonitMode(enable=False,siteid=1)