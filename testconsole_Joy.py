import csv,time,json,base64
from NetPacketTools.packet_action import PacketAction
from APITools.athenac_web_API_libry import AthenacWebAPILibry
from APITools.athenac_core_API_libry import AthenacCoreAPILibry
from APITools.athenac_probe_API_libry import AthenacProbeAPILibry
from NetPacketTools.packet_listen_RadiusProxy import PacketListenRadiusProxy
from CreateData import iprelated,macrelated
from NetPacketTools.packet_action_DHCPasync import PacketActionDHCPasync
from multiprocessing import Pool


if __name__ == '__main__':
    # 可以把程式寫在這
    pass