import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path


def plot_maskingsweep(appname):
    top_dir = Path(__file__).resolve().parent
    steps = np.round(np.linspace(0, 0.9, 10), decimals=1)
    dirlist = [appname + 'baseline' + str(ele) for ele in steps]
    dflist = []
    for name in dirlist:
        sweepvfdir = top_dir / 'maskingsweep' / appname / name
        df_vf = pd.read_csv(sweepvfdir / (appname + 'baseline_pvf.csv'))
        dflist.append(df_vf)
    print(dflist)

    plt.figure(figsize=(20, 16))
    for i, frame in enumerate(dflist):
        mf = (i/10)
        plt.plot(frame.iloc[:, 0], frame.iloc[:, 1], label='Masking = ' + str(mf), linewidth=4)
        plt.legend(fontsize=18, loc=4)
    plt.title(appname + ': Logic Masking Sweep', fontsize=20)
    plt.ylabel('PVF', fontsize=18)
    plt.ylim([0, 0.5])
    plt.xlabel('Time (Tick)', fontsize=18)

    plt.show()


plot_maskingsweep('prime')
