import matplotlib.pylab as plt
import statsmodels.tsa.api as smt
import seaborn as sns
import pandas as pd

def tsplot(y, lags=None, title='', figsize=(10, 15)):
    fig = plt.figure(figsize=figsize)

    ts_ax = plt.subplot(4, 1, 1)
    hist_ax = plt.subplot(4, 1, 2)
    acf_ax = plt.subplot(4, 1, 3)
    pacf_ax = plt.subplot(4, 1, 4)

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind='hist', bins=25)
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