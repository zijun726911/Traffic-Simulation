from decimal import Decimal
import numpy as np
import  statsmodels.api as sm

def splitToTimeSlot(packets,timeInterval):
    timeSlotInterval=Decimal(timeInterval)
    startTime = Decimal(packets[0].time)
    byteRates = []
    byteSlots = []
    timestamps=[]
    packNums=[]
    thisPackNum=0
    thisBytes=Decimal(0)
    startThisSlot = startTime
    endThisSlot = startThisSlot + timeSlotInterval
    for packet in packets:

        if startThisSlot <= packet.time < endThisSlot:
            thisBytes += packet.wirelen
            thisPackNum+=1
        else:
            #when step into this  branch, it must  iterate to the fist packet of the next slot
            # start next slot

            startThisSlot=endThisSlot
            endThisSlot= startThisSlot + timeSlotInterval
            timestamps.append(packet.time)
            byteSlots.append(thisBytes)
            byteRates.append(thisBytes/timeSlotInterval)
            packNums.append(thisPackNum)
            thisBytes=Decimal(packet.wirelen) #add first packet to the next slot
            thisPackNum=1
    #add last slot
    timestamps.append(packet.time)
    byteSlots.append(thisBytes)
    packNums.append(thisPackNum)
    byteRates.append(thisBytes / timeSlotInterval)

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


