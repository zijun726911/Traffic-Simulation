from functools import reduce

from scapy.all import rdpcap, RawPcapReader


from decimal import Decimal
import time

graph_path_prefix='..\graph'
data_path_prefix='..\dataset'

def readPcap(fileName):

    packets = RawPcapReader(fileName)

    return packets

def readTimestamp(timestampsFileName):


    if timestampsFileName.split('.')[-1]!='times':
        raise Exception('Not timestamp file!')

    timestampsFile = open(timestampsFileName)
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
