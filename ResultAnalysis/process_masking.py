from datawrapper import VFDataWrapper, VFDataWrapperExtraction
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plotmasking(classname, appname):
    dfmasking_app = classname.getsweepinfo(appname)
    return dfmasking_app[20:]


def costreturn(classname, appname, cost_steps=np.round(np.linspace(0, 0.9, 10), decimals=1), en_pvf=False):
    dfmasking_app = classname.getsweepinfo(appname)
    gain = []
    pvf = dfmasking_app.tail(1)
    for c in cost_steps:
        gain_i = classname.gain(dfmasking_app, [0.0, c])
        gain.append(gain_i)
    if en_pvf is True:
        gain = [gain, pvf.values[0, 1:]]
        gain = np.array(gain)
    return gain


def costreturngroup(classname, applist, pvfen=False):
    gainarray = []
    for app in applist:
        gaini = costreturn(classname, app, en_pvf=pvfen)
        gainarray.append(gaini)
    gainarray = np.array(gainarray)
    cost_steps = np.round(np.linspace(0, 0.9, 10), decimals=1)
    if pvfen is True:
        pvflist = [app + 'pvf' for app in applist]
        gainarray = gainarray.reshape(4, 10)
        dfgain = pd.DataFrame(gainarray.transpose(), columns=[val for pair in zip(applist, pvflist) for val in pair], index=cost_steps)
    else:
        dfgain = pd.DataFrame(gainarray.transpose(), columns=applist, index=cost_steps)
    return dfgain


def returnbydepth(classname, applist, depth):
    gainarray = []
    costsample = np.array([0.3, 0.5, 0.7, 0.9])
    columnlabel = ['Masking=' + mystr for mystr in [str(ele) for ele in list(costsample)]]
    print(columnlabel)
    for app in applist:
        gaini = costreturn(classname, app, costsample)
        gainarray.append(gaini)
    gainarray = np.array(gainarray)
    dfgainbydepth = pd.DataFrame(gainarray, columns=columnlabel, index=depth)
    return dfgainbydepth

