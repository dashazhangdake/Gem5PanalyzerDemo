import matplotlib.pyplot as plt
import math


def plot_pvfioo3(dio, do3, col=3, step=2):  # PLOT ARM32IO-PVF and ARM32O3-PVF
    pvfpair = dio
    pvfpairo3 = do3
    label32 = [col for col in pvfpairo3 if col.endswith('32')]
    labels = [x[:-2] for x in label32]
    labelst = labels[::2]
    labelsvf = labels[1::2]

    labelst = labelst[::step]
    row = math.ceil(len(labelst) / col)
    # plot line charts by label list
    plt.figure(figsize=(30, 20))
    for i in range(len(labelst)):
        plt.subplot(row, col, i + 1)
        plt.plot(pvfpairo3[labelst[i] + '32'][50:], pvfpairo3[labelsvf[i] + '32'][50:], label=labelsvf[i] + '-OoO', linewidth=4)
        plt.plot(pvfpair[labelst[i] + 'HPI'][50:], pvfpair[labelsvf[i] + 'HPI'][50:], label=labelsvf[i] + '-InOrder', linewidth=4)
        plt.title(labelsvf[i], fontsize=20)
        if i % col == 0:
            plt.ylabel('PVF', fontsize=18)
        plt.ylim([0, 1])
        if i >= (row - 1) * col:
            plt.xlabel('Time (Tick)', fontsize=18)
        # plt.xscale('log', base=10)
        plt.legend(fontsize=18, loc='upper right')
        plt.grid(axis='y')
    plt.show()


