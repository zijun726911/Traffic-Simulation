import matplotlib.pylab as plt
import statsmodels.tsa.api as smt
import seaborn as sns
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

def tsplot(y, lags=None, title='', figsize=(10, 15)):
    fig = plt.figure(figsize=figsize)

    ts_ax = plt.subplot(4, 1, 1)
    hist_ax = plt.subplot(4, 1, 2)
    acf_ax = plt.subplot(4, 1, 3)
    pacf_ax = plt.subplot(4, 1, 4)

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    sns.distplot(y,ax=hist_ax)
    # y.plot(ax=hist_ax, kind='hist',bins=30)
    hist_ax.set_title('Histogram')
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    fig.tight_layout()
    return ts_ax, acf_ax, pacf_ax


from statsmodels.tsa.stattools import adfuller


def test_stationarity(timeseries):
    movingAverage = timeseries.rolling(window=50).mean()
    movingSTD = timeseries.rolling(window=50).std()
    plt.figure(figsize=(15, 10))
    orig = plt.plot(timeseries, color='c', label='Original')
    mean = plt.plot(movingAverage, color='red', label='Rolling Mean')
    std = plt.plot(movingSTD, color='black', label='Rolling Std')

    plt.legend(loc='best')
    plt.title("Rolling Mean & Standard Deviation")
    plt.show(block=False)

    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value(%s)' % key] = value

    print(dfoutput)





def decompose(timeseries,  freq = None):

    # 返回包含三个部分 trend（趋势部分） ， seasonal（季节性部分） 和residual (残留部分)
    decomposition = seasonal_decompose(timeseries, freq=freq)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    plt.figure(figsize=(30, 30))
    plt.subplot(411)
    plt.plot(timeseries, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    return trend, seasonal, residual

def plotTrainTestPredict(data_train,data_test,data_predict):
    plt.figure(figsize=(40, 8))
    plt.xticks(rotation=45)

    plt.plot(data_train.iloc[4000:])
    plt.plot(data_test)
    plt.plot(data_predict.iloc[4000:])
    plt.legend([ "train set","test set", "pred"], loc="best")
    plt.title("test set &train set & prediction")
    plt.savefig("test set &train set & prediction")
