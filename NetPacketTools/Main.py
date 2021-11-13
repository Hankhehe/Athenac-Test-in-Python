import time
# from PacketAction import PacketAction
# from PacketListen import PacketListen


# PacketListen('Wi-Fi')
try:
    a = input('Please input Name')
    print(a)
    time.sleep(10)
    # Device1 = PacketAction('Ethernet1')
    # Device2 = PacketAction('Ethernet2')

    #執行 DHCPv4 壓力測試

    # log1 = Device1.DHCPv4ClientTest(1)
    # log2 =Device1.DHCPv6ClientTest(1)
    # print(log1)
    # print(log2)
    # print('Done')
finally:
    time.sleep(3000)

#執行 DHCPv6 壓力測試
# Device1.DHCPv6ClientTest()
# Device2.DHCPv6ClientTest(3)

#檢查是否收到 NDP 的 IP、MAC 資料
# ipv6blocktag = Device2.NDPBlockCheck('2001:b030:2133:815::21:254','00:aa:ff:ae:09:cc')

#檢查是否收到 ARP 的 IP、MAC 資料
# blocktag = Device2.ARPBlockCheck('192.168.21.231','00:aa:ff:ae:09:cc')
# print(blocktag)

#Send DHCPv4 Offer
# Device1.SendDHCPv4Offer()
# Device2.SendDHCPv4Offer()

#Send DHCPv6 Advertise
# Device1.SendDHCPv6Advertise()
# Device2.SendDHCPv6Advertise()

#SendARP Reply
# Device1.SendARPReply('192.168.21.90')
# Device2.SendARPReply('192.168.21.5')

#Send SLAAC

# Device1.SendRA()


#SendNA
# Device1.SendNA('2001:b030:2133:80b::11:90')
# Device2.SendNA('2001:b030:2133:80b::11:90')

#Send lot ARP and NDP Packet
# while True:
#     Device2.SendARPReply('192.168.21.1')
#     Device2.SendNA('2001:b030:2133:815::1')

#Send OutofVLAN Packet
# Device2.SendARPReply('10.10.1.1')
# Device2.SendNA('2001:b000:111:1::1')


#Create Ipv4 and IPv6 conflict
# while True:
#     Device2.SendARPReply('192.168.21.5')
#     Device2.SendNA('2001:b030:2133:815::3')
#     time.sleep(5)


