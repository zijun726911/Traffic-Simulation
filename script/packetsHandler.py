from decimal import Decimal
import numpy as np
import  statsmodels.api as sm

def splitToTimeSlot(timestampsAndWirelens,timeInterval):
    timeInterval=Decimal(str(timeInterval))
    startTime = Decimal(str(timestampsAndWirelens[0][0]))  #get the timestamp of the first packet
    byteRates = []
    byteSlots = []
    timestamps=[]
    packNums=[]
    thisPackNum=0
    thisBytes=0
    startThisSlot = startTime
    endThisSlot = startThisSlot + timeInterval
    for timestamp, wirelen in timestampsAndWirelens:

        if startThisSlot <= timestamp < endThisSlot:
            thisBytes += wirelen
            thisPackNum+=1
        else:
            #when step into this  branch, it must  iterate to the fist packet of the next slot
            # start next slot
            startThisSlot=endThisSlot
            endThisSlot= startThisSlot + timeInterval
            timestamps.append(timestamp)
            byteSlots.append(thisBytes)
            byteRates.append(thisBytes/timeInterval)
            packNums.append(thisPackNum)
            thisBytes=wirelen   #add first packet to the next slot
            thisPackNum=1


    #add last slot
    timestamps.append(timestamp)
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


