from decimal import Decimal
import numpy as np
import  statsmodels.api as sm

def splitToTimeSlot(packets,timeInterval):
    timeSlotInterval=Decimal(timeInterval)
    startTime = Decimal(packets[0].time)
    byteRates = []
    byteSlots = []
    timestamps=[]
    thisBytes=Decimal(0)
    startThisSlot = startTime
    endThisSlot = startThisSlot + timeSlotInterval
    for packet in packets:

        if startThisSlot <= packet.time < endThisSlot:
            thisBytes += packet.wirelen

        else:
            #when step into this  branch, it must  iterate to the fist packet of the next slot
            # start next slot

            startThisSlot=endThisSlot
            endThisSlot= startThisSlot + timeSlotInterval
            timestamps.append(packet.time)
            byteSlots.append(thisBytes)
            byteRates.append(thisBytes/timeSlotInterval)
            thisBytes=Decimal(packet.wirelen) #add first packet to the next slot

    #add last slot
    timestamps.append(packet.time)
    byteSlots.append(thisBytes)
    byteRates.append(thisBytes / timeSlotInterval)

    return timestamps,byteSlots,byteRates

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

    # result=sm.tsa.acf(x)
    return result


