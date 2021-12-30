import threading,time,pytest_check as check,asyncio
from scapy import *
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType,SiteVerifyModule
from NetPacketTools.packet_listen import PacketListenFromFilter
from NetPacketTools.packet_action_test import PacketActionTest

macint = 186916976721920
threads = []
results = []
lan = PacketAction('Ethernet1')
pass
for i in range(10):
    threads.append(threading.Thread(target=lan.GetIPfromDHCPv6,args=[i,hex(macint+i)[2::1],results]))
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()

print(f'count : ---------{len(results)}')
pass

# async def DHCPv4(tranId:int,mac:str)-> dict:
#     a = lan1_.GetIPfromDHCPv4(mac=mac,tranId=tranId)
#     return a

# result = []
# macint = 186916976721920
# lan1_ = PacketAction('Ethernet1')
# tasks =[DHCPv4(tranId=i,mac=hex(macint+i)[2::]) for i in range(10)]
# result.append( asyncio.run(asyncio.wait(tasks)))
# pass