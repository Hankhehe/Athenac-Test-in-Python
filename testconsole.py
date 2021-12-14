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

WebAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
coreaction = AthenacCoreAPILibry('https://192.168.21.180:18000','7467117531','6922375401')
# lan2 = PacketAction('Ethernet2')
time.sleep(5)
# WebAPI.UpdateBlockMessage(enable=True,ADverify=True,DBverify=True,LDAPverify=True,siteid=1)
WebAPI.GetMACDetail('005056AEAA69',2)
coreaction.AuthMACFromUserApply('172.18.255.11','005056AEAA69','RAJ','AgRAu+JjydaLEw3me8kTxA==')

#AD account = Hank pwd = QkIHIDPyeiIALps4IKGH+w==
#DB account = admin pwd = 36IqJwCHVwl9IS4w4b1mMw==
#LDAP account = RAJ pwd = AgRAu+JjydaLEw3me8kTxA==
pass
# check =   lan2.NDPBlockCheck(srcIP=lan2.linklocalIp,dstIP=lan2.gatewatIpv6,ProbeMAC='00:aa:ff:ae:2b:a1')
# print(check)


# WebAPI.SwitchSiteMonitMode(enable=False,siteid=1)