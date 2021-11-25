import time
import datetime
from NetPacketTools.packet_action import PacketAction
from NetPacketTools.packet_listen import PacketListen
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.Enums.enum_flag import RadiusVLANMappingType

AthenacAPI = AthenacWebAPILibry('http://192.168.21.180:8000','admin','admin')
time.sleep(3)
AthenacAPI.DelVLANMapping('005056AEAA69',RadiusVLANMappingType.MAC.value)


if target := AthenacAPI.GetVLANMapping('AAAAAAAAAAAB',RadiusVLANMappingType.MAC.value):
    print('True')
    print(target)
else: 
    print('False')
    print(target)
pass