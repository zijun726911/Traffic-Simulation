from script.packetPreprocessing import *
from script.packetsHandler import *
import decimal
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
import random

if __name__ == '__main__':
    fileNum=10
    packets=readPcap(fileNum)
    timestamp=readTimestamp(fileNum*10000)
    packets=replaceTimestemp(packets,timestamp)
    timestamps,byteSlots0001, byteRates0001=splitToTimeSlot(packets, 0.0001)
    timestamps,byteSlots0002, byteRates0002 = splitToTimeSlot(packets, 0.0002)
    print("total bytes that get from every       packets:", getTotalBytes(packets))
    print("total bytes that get from every 0.0001s slots:", sum(byteSlots0001))
    print("total bytes that get from every 0.0002s slots:", sum(byteSlots0002))
    print("")

    print("average bytesPerSec get from every        packets:", getAvgByterate(packets))
    print("average bytesPerSec get from every   0.0001 slots:", np.mean(byteRates0001))
    print("average bytesPerSec get from every   0.0002 slots:", np.mean(byteRates0002))
    print("")

    print("variance bytesPerSec get from every  every 0.0001 slots:", np.std(byteRates0001))
    print("variance bytesPerSec get from every  every 0.0002 slots:", np.std(byteRates0002))

    fig=sns.lineplot(x=range(len(byteRates0001)), y=list(map(int,byteRates0001))) .get_figure()#.savefig('fig.png',dpi=1080);
    # sns.distplot(list(map(int,byteRates0001)))


    # pd.plotting.autocorrelation_plot(list(map(int,byteRates0001)))


    plt.show()
    # print(autocorr())