import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from process_masking import *


def plotPVF1(classname, cols, figsize, applist):
    data_series = []
    for app in applist:
        data_series.append(plotmasking(classname, app))
    rows = len(data_series) // cols
    figs, axs = plt.subplots(rows, cols, sharey=True, figsize=figsize)
    for irow in range(axs.shape[0]):
        for icol in range(axs.shape[1]):
            idx = icol + cols * irow
            appname = applist[idx]
            if irow == 0 and icol == 0:
                ax = data_series[idx].plot(x='Tick', ax=axs[irow][icol])
            else:
                ax = data_series[idx].plot(x='Tick', legend=False, ax=axs[irow][icol])
            ax.text(.5, .95, appname,
                    horizontalalignment='center',
                    transform=ax.transAxes, fontsize=18)
            ax.grid(axis='y')
            ax.set_ylabel('PVF', fontsize=18)
            ax.set_xlabel('Time(Tick)', fontsize=14)


def plotPVF2(cols, figsize, dflist):
    rows = len(dflist) // cols
    print(cols, rows)
    figs, axs = plt.subplots(rows, cols, sharey=True, figsize=figsize)
    if rows == 1:
        axs = axs.reshape(1, -1)
    print(axs.shape)
    for irow in range(axs.shape[0]):
        for icol in range(axs.shape[1]):
            idx = icol + cols * irow
            ax = dflist[idx].plot(ax=axs[irow][icol], marker='o')
            ax.set_ylim(0, 0.9)
            # ax.set_xlim(0, 1)
            ax.set_ylabel('PVF Reduction', fontsize=18)
            ax.set_xlabel('Masking Level', fontsize=18)
            ax.legend(loc='upper left', fontsize=18)
            ax.grid()


def plotPVF3(cols, figsize, dflist):
    rows = len(dflist) // cols
    print(cols, rows)
    figs, axs = plt.subplots(rows, cols, sharey=True, figsize=figsize)
    if rows == 1:
        axs = axs.reshape(1, -1)
    print(axs.shape)
    for irow in range(axs.shape[0]):
        for icol in range(axs.shape[1]):
            idx = icol + cols * irow
            ax = dflist[idx].plot(ax=axs[irow][icol], marker='o')
            ax.set_ylim(0, 0.55)
            # ax.set_xlim(0, 1)
            ax.set_ylabel('PVF Reduction', fontsize=16)
            if idx == 0:
                ax.set_title('Vectorized Qsort', fontsize=18)
                ax.set_xlabel('Redundant Array Size', fontsize=16)
            else:
                ax.set_title('SUSAN Smoothing', fontsize=18)
                ax.set_xlabel('SUSAN Filter Radius', fontsize=16)
            ax.legend(loc='upper right', fontsize=12)
            ax.grid()

def plotPVFdualaxis(cols, figsize, dflist, ftsize=12):
    rows = len(dflist) // cols
    print(cols, rows)
    figs, axs = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1:
        axs = axs.reshape(1, -1)
    for irow in range(axs.shape[0]):
        for icol in range(axs.shape[1]):
            idx = icol + cols * irow
            ax = dflist[idx].iloc[:, 0::2].plot(ax=axs[irow][icol], marker='s')
            if idx == 0:
                ax.set_ylabel('Return', fontsize=ftsize)
                ax.set_ylim(0, 1)
                ax.set_xlim(0, 0.9)
                ax.set_xlabel('Masking Level', fontsize=ftsize)
            else:
                ax.set_ylim(0, 1)
                ax.set_xlim(0, 0.9)
                ax.set_xlabel('Masking Level', fontsize=ftsize)

            dflist[idx].iloc[:, 1::2].plot(ax=axs[irow][icol], secondary_y=True, style='--', marker='v')
            ax.legend(loc='upper left', fontsize=ftsize-2)
            plt.legend(loc='upper right', fontsize=ftsize-2)
            plt.ylim(0, 1)
            ax.grid()
            if idx == len(dflist) - 1:
                plt.ylabel('PVF')
