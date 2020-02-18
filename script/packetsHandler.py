from decimal import Decimal
from typing import List
from typing import Tuple
import numpy as np
import  statsmodels.api as sm
import pandas as pd
def splitToTimeSlot(timestampsAndWirelens: pd.Series
                    ,timeInterval:float)-> [List,List[Decimal],List,List]:

    '''
    :param timestampsAndWirelens: tuple list of timestamp and ccorresponding packet length.
    sample: timestampsAndWirelens=[(1521118800.000005990,185),(1521118800.000007272,202),(1521118800.000008553,56)]

    :param timeInterval: number of second per time unit

    :returns: packNums: packets number of every time unit
            timestamps: timestamps of every time unit (use the timestamp of last packet of this time unit as the timestamp of this time unit )
            byteSlots: byte number of every time unit
            byteRates: byte rate of every time unit

    '''
    timeInterval=Decimal(str(timeInterval))
    startTime = Decimal(timestampsAndWirelens['timestamp'].iloc[0])  #get the timestamp of the first packet
    print("startTime:",str(startTime))
    byteRates = []
    byteSlots = []
    timestamps=[]
    packNums=[]
    thisPackNum=0
    thisBytes=0
    startThisSlot = startTime
    endThisSlot = startThisSlot + timeInterval
    print("endThisSlot:",str(endThisSlot))
    for timestamp, wirelen in \
            zip(timestampsAndWirelens['timestamp'],timestampsAndWirelens['wirelen']):
        timestamp=Decimal(timestamp)
        if startThisSlot <= timestamp < endThisSlot:
            thisBytes += wirelen
            thisPackNum+=1
        else:
            #when step into this  branch, it must  iterate to the fist packet of the next slot
            # start next slot
            startThisSlot=endThisSlot
            endThisSlot= startThisSlot + timeInterval
            timestamps.append(startThisSlot)
            byteSlots.append(thisBytes)
            byteRates.append(thisBytes/timeInterval)
            packNums.append(thisPackNum)
            thisBytes=wirelen   #add first packet to the next slot
            thisPackNum=1

    #add last slot
    timestamps.append(startThisSlot+timeInterval)
    byteSlots.append(thisBytes)
    packNums.append(thisPackNum)
    byteRates.append(thisBytes / timeInterval)

    return packNums,timestamps,byteSlots,byteRates

def getTotalBytes(packets):
    return sum(map(lambda packet:Decimal(packet.wirelen),packets))

def getAvgByterate(packets):
    return getTotalBytes(packets)/(packets[-1].time-packets[0].time)

def autocorr(x):
    '''numpy.correlate, non partial'''
    x=np.array(x)
    mean=x.mean()
    var=np.var(x)
    xp=x-mean
    corr = np.correlate(xp, xp, mode='full')
    result=corr[corr.size//2:]/(var*x.size)

    return result

 # result=sm.tsa.acf(x)


