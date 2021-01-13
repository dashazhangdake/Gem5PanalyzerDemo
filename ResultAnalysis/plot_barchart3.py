import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_barchart3(dfio, dfo3, dfbeam='beam_fit.csv'):  # Figure Cumulative PVFs by apps and configs – FIT rate
    finaltick_pvf1 = dfio.tail(1).iloc[:, 1::2]

    finaltick_pvf2 = dfo3.tail(1).iloc[:, 1::2]
    label32 = [col for col in finaltick_pvf2 if col.endswith('32')]
    label64 = [col for col in finaltick_pvf2 if col.endswith('64')]
    finaltick_pvf32 = finaltick_pvf2[label32]
    finaltick_pvf64 = finaltick_pvf2[label64]

    T3 = pd.read_csv(dfbeam)
    finaltick_beam = T3.tail(1)

    grouplabels = [x[:-2] for x in label32]
    pvf32 = np.round(finaltick_pvf32.values[0], decimals=2)
    pvf64 = np.round(finaltick_pvf64.values[0], decimals=2)
    labelinorder = [col + 'HPI' for col in grouplabels]

    finaltick_pvfinorder = finaltick_pvf1[labelinorder]
    finaltick_pvfbeam = finaltick_beam[grouplabels]
    # normalized_beam = finaltick_pvfbeam.div(finaltick_pvfbeam.max(axis=1) * 1.25, axis=0)
    normalized_beam = np.round(finaltick_pvfbeam[grouplabels].values[0], decimals=2)
    pvfinorder = np.round(finaltick_pvfinorder.values[0], decimals=2)

    # finaltick_pvfio = finaltick_pvf1.filter(like=str([x for x in grouplabels]), axis=1)
    # print(finaltick_pvfio)

    x = 1.5 * np.arange(len(grouplabels))  # the label locations
    width = 0.3  # the width of the bars
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(20, 16))
    ax2 = ax[0, 0].twinx()
    rects1 = ax[0, 0].bar(x - 1.5 * width, pvf32, width, label='32bit, Out-of-Order')
    rects2 = ax[0, 0].bar(x - 0.5 * width, pvfinorder, width, label='32bit, In-Order')
    rects3 = ax[0, 0].bar(x + 0.5 * width, pvf64, width, label='64bit, Out-of-Order')
    rects4 = ax2.bar(x + 1.5 * width, normalized_beam, width, label='Beam,32bit Out-of-Order', color='red')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax[0, 0].set_ylabel('CumulativePVF', fontsize=18)
    ax[0, 0].set_title('Cumulative PVFs by applications and configs', fontsize=20)
    ax[0, 0].set_xticks(x)
    ax[0, 0].set_xticklabels(grouplabels, fontsize=18)
    ax[0, 0].legend(fontsize=18)
    ax2.legend(fontsize=18)
    ax2.set_ylabel('FIT Rates', fontsize=18)

    # autolabel(ax, rects1)
    # autolabel(ax, rects2)
    # autolabel(ax, rects3)
    fig.tight_layout()
    plt.show()

