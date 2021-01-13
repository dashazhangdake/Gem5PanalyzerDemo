import matplotlib.pyplot as plt
import numpy as np


def plot_linechart6432(datain, labels, skip=7):  # Figure PVFs by time and ISAs
    pvfpair = datain
    # plot line charts by label list
    for lname in labels:
        plt.plot(pvfpair['T' + lname + '32'][skip:], pvfpair[lname + '32'][skip:], label=lname + '-ARM32', linewidth=2)
        plt.plot(pvfpair['T' + lname + '64'][skip:], pvfpair[lname + '64'][skip:], label=lname + '-ARM64', linewidth=2)
    # plt.title('Architectural Integer Register File PVF', fontsize=20)
    plt.ylabel('Int Arch Register PVF', fontsize=18)
    plt.xlabel('Time (Tick)', fontsize=18)
    plt.xscale('log', base=10)
    plt.xlim(1e7, 2e10)
    plt.ylim([0, 1])
    plt.legend(fontsize=18, loc=1)
    plt.grid()


def plot_linechartcmp(datain, labels, skip=5):  # Figure PVFs by time and ISAs
    pvfpair = datain
    plt.figure(figsize=[10, 6.7])
    # plot line charts by label list
    for lname in labels:
        plt.plot(pvfpair['T' + lname][skip:], pvfpair['PVF' + lname][skip:], label=lname, linewidth=2)
    # plt.title('Architectural Integer Register File PVF', fontsize=20)
    plt.ylabel('Int Arch Register PVF', fontsize=18)
    plt.xlabel('Time (Tick)', fontsize=18)
    # plt.xscale('log', base=10)
    # plt.xlim(1e7, 2e10)
    plt.ylim([0, 1])
    plt.legend(fontsize=18, loc=1)
    plt.grid()


def plot_time_barchart6432(datain):  # Figure PVFs by time and ISAs
    pvfpair_time = datain.tail(1).iloc[:, ::2]
    label32 = [col for col in pvfpair_time if col.endswith('32')]
    label64 = [col for col in pvfpair_time if col.endswith('64')]
    finaltick_pvf32 = pvfpair_time[label32].values[0]
    finaltick_pvf64 = pvfpair_time[label64].values[0]
    # plot line charts by label list
    width = 0.3
    x = np.arange((len(label32)))
    labels = [x[1:-2] for x in label32]
    plt.bar(x - width / 2, finaltick_pvf32, width, label='ARM32')
    plt.bar(x + width / 2, finaltick_pvf64, width, label='ARM64')
    # plt.title('Execution time of selected benchmarks', fontsize=20)
    plt.ylabel('Execution Time (Ticks)', fontsize=18, labelpad=-15)
    plt.xlabel('Applications', fontsize=18)
    plt.xticks(x, labels=labels)
    plt.yscale('log', base=10)
    plt.legend(fontsize=18, loc=1)


def plot_bigpic(datain, figuresize):  # Figure PVFs by time and ISAs
    plt.figure(figsize=figuresize)
    ax1 = plt.subplot(231)
    plot_linechart6432(datain, ['DIJK', 'FFT'])
    x_axis = ax1.axes.get_xaxis()
    x_axis.set_label_text(' ')
    ax2 = plt.subplot(232)
    plot_linechart6432(datain, ['AESD', 'AESE'])
    x_axis = ax2.axes.get_xaxis()
    x_axis.set_label_text(' ')
    y_axis = ax2.axes.get_yaxis()
    y_axis.set_label_text(' ')
    ax3 = plt.subplot(233)
    plot_linechart6432(datain, ['SUSANC', 'SUSANE'])
    x_axis = ax3.axes.get_xaxis()
    x_axis.set_label_text(' ')
    y_axis = ax3.axes.get_yaxis()
    y_axis.set_label_text(' ')
    plt.subplot(234)
    plot_linechart6432(datain, ['CRC', 'FFT'])
    ax4 = plt.subplot(235)
    plot_linechart6432(datain, ['QSORT', 'SUSANS'])
    y_axis = ax4.axes.get_yaxis()
    y_axis.set_label_text(' ')
    ax5 = plt.subplot(236)
    plot_linechart6432(datain, ['MXM', 'SSEARCH'])
    y_axis = ax5.axes.get_yaxis()
    y_axis.set_label_text(' ')
    # plot_time_barchart6432(datain)
    plt.tight_layout()
