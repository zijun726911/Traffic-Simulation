import matplotlib.pylab as plt
import statsmodels.tsa.api as smt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.axes import Axes
from pandas import Series
from statsmodels.tsa.seasonal import seasonal_decompose

def tsplot(y: pd.Series, lags=None, title='', figsize=(10, 20)):
    fig = plt.figure(figsize=figsize) #type: plt.Figure

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ts_ax = plt.subplot(4, 1, 1) #type:plt.Axes
    hist_ax = plt.subplot(4, 1, 2) #type:plt.Axes
    acf_ax = plt.subplot(4, 1, 3) #type:plt.Axes
    pacf_ax = plt.subplot(4, 1, 4) #type:plt.Axes

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    ts_ax.set_ylabel("Traffic rate (Bytes/s)")
    sns.distplot(y,ax=hist_ax)
    # y.plot(ax=hist_ax, kind='hist',bins=30)
    hist_ax.set_title('Histogram')
    hist_ax.set_xlabel("Traffic rate (Bytes/s)")
    hist_ax.set_ylabel("Probability")


    acf_ax.set_ylabel("ACF")
    acf_ax.set_xlabel("Times Shift (Lags)")
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)

    pacf_ax.set_ylabel("PACF")
    pacf_ax.set_xlabel("Times Shift (Lags)")
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    fig.tight_layout()
    fig.savefig("../graph/tsplot_"+title.replace(".","p"),dpi=100)
    return ts_ax, acf_ax, pacf_ax


from statsmodels.tsa.stattools import adfuller


def test_stationarity(timeseries: Series):
    movingAverage = timeseries.rolling(window=50).mean()
    movingSTD = timeseries.rolling(window=50).std()
    plt.figure(figsize=(15, 10))
    orig = plt.plot(timeseries, color='c', label='Original')
    mean = plt.plot(movingAverage, color='red', label='Rolling Mean')
    std = plt.plot(movingSTD, color='black', label='Rolling Std')

    plt.legend(loc='best')
    plt.title("Rolling Mean & Standard Deviation")
    plt.show(block=False)
    plt.savefig("../graph/test_stationarity")

    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value(%s)' % key] = value

    print(dfoutput)





# def decompose(timeseries,  freq = None):
#
#     # 返回包含三个部分 trend（趋势部分） ， seasonal（季节性部分） 和residual (残留部分)
#     decomposition = seasonal_decompose(timeseries, freq=freq)
#
#     trend = decomposition.trend
#     seasonal = decomposition.seasonal
#     residual = decomposition.resid
#     plt.figure(figsize=(30, 30))
#     plt.subplot(411)
#     plt.plot(timeseries, label='Original')
#     plt.legend(loc='best')
#     plt.subplot(412)
#     plt.plot(trend, label='Trend')
#     plt.legend(loc='best')
#     plt.subplot(413)
#     plt.plot(seasonal, label='Seasonality')
#     plt.legend(loc='best')
#     plt.subplot(414)
#     plt.plot(residual, label='Residuals')
#     plt.legend(loc='best')
#     plt.tight_layout()
#     plt.show()
#     return trend, seasonal, residual

def plotTrainTestPredict(data_train,data_test,data_predict):
    plt.figure(figsize=(40, 8))
    plt.xticks(rotation=45)

    plt.plot(data_train.iloc[4000:])
    plt.plot(data_test)
    plt.plot(data_predict.iloc[4000:])
    plt.legend([ "train set","test set", "pred"], loc="best")
    plt.title("test set &train set & prediction")
    plt.savefig("test set &train set & prediction")


def plot_diff_timescales(scale1: Series,
                         scale0p1: Series,
                         scale0p01: Series,
                         scale0p001: Series):
    plt.figure(figsize=(10, 10))
    figure = plt.figure(1)

    plt.subplots_adjust(hspace=1)


    plt.suptitle("Traffic Rate at Different Timescales",y=5 ,weight='bold')
    # plt.suptitle("") y=0.93

    axes1 = plt.subplot(411)  # type: Axes
    axes1.set_title("1s Timescale")
    axes1.set_xlabel("Time (second)",)
    axes1.set_ylabel("Traffic rate (Bytes/s)")
    axes1.plot(scale1.index, scale1, linestyle='solid')

    axes2 = plt.subplot(412)  # type: Axes
    axes2.plot(scale0p1.index, scale0p1, linestyle='dotted')
    axes2.set_title("0.1s Timescale",)
    axes2.set_xlabel("Time (second)", )
    axes2.set_ylabel("Traffic rate (Bytes/s)", )

    axes3 = plt.subplot(413)  # type: Axes
    axes3.plot(scale0p01.index, scale0p01, linestyle='dashed')
    axes3.set_title("0.01s Timescale", )
    axes3.set_xlabel("Time (second)")
    axes3.set_ylabel("Traffic rate (Bytes/s)", )

    axes4 = plt.subplot(414)  # type: Axes
    axes4.plot(scale0p001.index, scale0p001, linestyle='dashdot')
    axes4.set_title("0.001s Timescale", )
    axes4.set_xlabel("Time (second)", )
    axes4.set_ylabel("Traffic rate (Bytes/s)", )
    figure.tight_layout()
    figure.savefig("../graph/Traffic Rate at Different Timescales2",dpi=200)
    plt.close('all')


def plot_packet_len_dist(timestampsAndWirelensPD: Series):
    plt.tight_layout()
    plt.figure(figsize=(20, 15))
    plt.title("Packet Length Distrbution", fontsize=50)
    axes = sns.distplot(timestampsAndWirelensPD["wirelen"]) #type: Axes
    axes.set_xticks(np.arange(0, 1700, 100),)
    axes.set_xticklabels(np.arange(0, 1700, 100))

    plt.xticks(rotation='40')
    axes.tick_params(axis="x", labelsize=30)
    axes.tick_params(axis="y", labelsize=30)
    plt.ylabel("PDF", fontsize=40)
    plt.xlabel("Packet Length (Bytes)", fontsize=40)

    plt.savefig("../graph/Packet Length Distrbution")
    plt.close('all')


def plot_packet_len_cdf(timestampsAndWirelensPD: Series):
    plt.tight_layout()
    plt.figure(figsize=(20, 15))
    plt.title("Packet Length Cumulative Distrbution", fontsize=50)
    axes = sns.distplot(timestampsAndWirelensPD["wirelen"],
                        hist_kws={'cumulative':True}) #type: Axes

    axes.set_xticks(np.arange(0, 1700, 100))
    axes.set_xticklabels(np.arange(0, 1700, 100))

    plt.xticks(rotation='40')
    axes.tick_params(axis="x", labelsize=30)
    axes.tick_params(axis="y", labelsize=30)
    plt.ylabel("CDF", fontsize=40)
    plt.xlabel("Packet Length (Bytes)", fontsize=40)

    plt.savefig("../graph/Packet Length CDF")
    plt.close('all')


def plot_arrival_time_diff(timestampsAndWirelensPD_origin:Series): 
    arrival_time_diff = timestampsAndWirelensPD_origin['timestamp'].diff(1).dropna()
    plt.figure(figsize=(25, 15))
    
    plt.title("Packets Arrival Time Difference Distribution",fontsize=30)
    axes = sns.distplot(arrival_time_diff)  # type:Axes
    plt.xticks(fontsize=20, rotation='40')
    axes.set_xticks(np.arange(0, 0.00007, 0.000005))
    axes.set_xticklabels(np.arange(0, 0.07, 0.005))
    plt.yticks(fontsize=20)
    plt.ylabel("Numbers of Interarrival Time that Fall in to Each Bin", fontsize=20)
    plt.xlabel("Packets Arrival Time Difference (ms)", fontsize=20)
    plt.savefig("../graph/Arrival Time Difference")
    plt.close('all')
