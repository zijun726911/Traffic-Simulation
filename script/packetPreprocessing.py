from functools import reduce

from scapy.all import rdpcap, RawPcapReader
import numpy as np
import scipy.stats as st
from scapy.packet import Packet
from scipy.stats import norm
from scipy.stats import kstest
import libpcap

from decimal import Decimal
import time
def readPcap(fileName):
    fileName = "..\dataset\equinix-nyc.dirA.20180315-130000.UTC.anon.pcap\equinix-nyc.dirA.20180315-130000.UTC.anon.pcap"

    packets = RawPcapReader(fileName)


    return packets

def readTimestamp(timestampsFileName):

    timestampsPath = "..\dataset\equinix-nyc.dirA.20180315-130000.UTC.anon.times"
    timestampsFileName = "\equinix-nyc.dirA.20180315-130000.UTC.anon.times"
    timestampsFile = open(timestampsPath + timestampsFileName)

    timestamps = timestampsFile.readlines()

    timestampsDecimal = list(map(lambda line: Decimal(line.strip()), timestamps))
    return timestampsDecimal


def getwirelen(packets):
    return list(map(lambda packet: packet[1].wirelen, packets))

















#
#
#
# timeSlotInterval = Decimal('0.000001')
# startTime = Decimal('0')
# bitRates = []
#
# timeSlots = [0] * 1000
# startPacketIndex = 0
# i = 0
# for timeSlot in timeSlots:
#     startThisSlot = startTime
#     endThisSlot = startThisSlot + timeSlotInterval
#     for index, packet in enumerate(packets[startPacketIndex:]):
#         if startThisSlot <= packet.time < endThisSlot:
#             timeSlot += packet.wirelen
#             print("index" + index)
#         else:
#             startPacketIndex += index
#             break;
#
#
#
