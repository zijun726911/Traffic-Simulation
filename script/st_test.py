import numpy as np
import scipy.stats as st
import scipy
import seaborn as sns
import pandas as pd
import matplotlib.pylab as plt



if __name__ == '__main__':
    # data = np.random.random(10000)
    size = 5000000
    timestampsAndWirelensPD = pd.read_csv("timestampsAndWirelens", dtype={'timestamp': 'float64'})
    arr_time_diff = timestampsAndWirelensPD['timestamp'].diff(1).dropna()

    data = arr_time_diff.sample(n=size)  # type: Series


    # data.plot(bins=size/10,kind='hist',label='original data' )

    def get_best_fit() -> st.rv_continuous:
        pass


    distributions = [st.expon,  # loc, scale
                     st.norm,  # loc, scale
                     st.halfnorm,
                     st.powerlaw,  # loc, scale
                     st.weibull_min  # a, loc, scale
                     ]

    mles = []

    plt.show()
    for distribution in distributions:
        x = scipy.arange(data.min(), data.max(), 0.0001)

        param = distribution.fit(data)
        data_gen = distribution.rvs(size=size, *param[:-2], loc=param[-2], scale=param[-1])
        data_gen = pd.Series(data_gen)  # type:Series
        axi = sns.kdeplot(data_gen, label=distribution.name)  # type: plt.Axes
        mle = distribution.nnlf(param, data)
        print(distribution.name + " " + str(mle) + " pars:" + str(param))
        mles.append(mle)

    # axi=sns.kdeplot(data, label="original data") #type: plt.Axes
    sns.distplot(data, hist=True, kde=False, label="original data", ax=axi);
    axi.set_title("Inter-Arrival Time Distribution")
    axi.set_ylabel("Frequency")
    axi.set_xlabel("Packets Arrival Time Difference (second)")
    plt.legend(loc='upper right')
    # plt.figure(figsize=(20,20))
    axi.get_figure().savefig("../graph/Arrival Time Fitting4", dpi=200)
    plt.show()

    results = [(distribution.name, mle) for distribution, mle in zip(distributions, mles)]
    best_fit = sorted(zip(distributions, mles), key=lambda d: d[1])[0]
    print('Best fit reached using {}, MLE value: {}'.format(best_fit[0].name, best_fit[1]))