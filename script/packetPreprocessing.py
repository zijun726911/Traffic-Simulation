from functools import reduce

from scapy.all import rdpcap
import numpy as np
import scipy.stats as st
from scapy.packet import Packet
from scipy.stats import norm
from scipy.stats import kstest


from decimal import Decimal
import time
def readPcap(fileNum):
    packetsFile=(packet for i in range(fileNum)
                            for packet in rdpcap("..\dataset\equinix-nyc.dirA.20180315-130000.UTC.anon.pcap"
                                                 "\splitted(10000 packets per file)"
                                                 "\out_" + str(i).zfill(5) + "_20180315210000.pcap")
                 )

    return packetsFile

def readTimestamp(lines):

    BYTES_PER_LINE=21
    timestampsPath = "..\dataset\equinix-nyc.dirA.20180315-130000.UTC.anon.times"
    timestampsFileName = "\equinix-nyc.dirA.20180315-130000.UTC.anon.times"
    timestampsFile = open(timestampsPath + timestampsFileName)
    if isinstance(lines,int):
        timestamps = timestampsFile.readlines(lines*BYTES_PER_LINE-1)

    timestampsDecimal = map(lambda line: Decimal(line.strip()), timestamps)
    return timestampsDecimal


def replaceTimestemp(packets,timestampsDecimal):
    def _replaceTimestemp(packet, timestamp):
        packet.time = timestamp
        return packet

    packets = [_replaceTimestemp(packet, timestamp)
               for packet,timestamp in zip(packets,timestampsDecimal)]

    return packets














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
