import matplotlib.pyplot as plt
import numpy as np
import math


def plot_qpvf(dpvf, dqpvf, col=5):  # Figure Q-PVF vs PVF
    pvfpair = dpvf
    label32 = [col for col in pvfpair if col.endswith('HPI')]
    labels = [x[:-3] for x in label32][1::2]
    row = math.ceil(len(labels) / col)
    qpvfpair = dqpvf

    plt.figure(figsize=(50, 30))
    for i in range(len(labels)):
        plt.subplot(row, col, i + 1)
        plt.plot(qpvfpair['TQ' + labels[i]], qpvfpair['Q' + labels[i]], label=labels[i] + '-QPVF', linewidth=4)
        plt.plot(pvfpair['T' + labels[i] + 'HPI'][50:], pvfpair[labels[i] + 'HPI'][50:], label=labels[i] + '-PVF', linewidth=4)
        plt.title(labels[i] + ': PVF and Q-PVF', fontsize=20)
        plt.ylabel('PVF', fontsize=18)
        plt.ylim([0, 1])
        plt.xlabel('Time (Tick)', fontsize=18)
        # plt.xscale('log', base=10)
        plt.legend(fontsize=18, loc=4)
    plt.show()
