from datawrapper import VFDataWrapper, VFDataWrapperExtraction
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from plot_bigpic import *
from plot_pvfioo3 import plot_pvfioo3
from plot_qpvf import plot_qpvf
from plot_barchart3 import plot_barchart3
from process_masking import *
from PVFplot import *

# INITIALIZE INPUT DATA, RESULT PROCESSING MODES
farm3264 = 'arm32vsarm64.csv'
farminorder = 'arm32inorder.csv'
farmqpvf = 'arm32inorderqpvf.csv'  # Input csv files
d3264 = VFDataWrapperExtraction('arm32vsarm64.csv', [])
d32io = VFDataWrapperExtraction('arm32inorder.csv', [])
d32qpvf = VFDataWrapperExtraction('arm32inorderqpvf.csv', [])  # Class objs
df3264 = d3264.readpvfbytime()
df32io = d32io.readpvfbytime()
df32qpvf = d32qpvf.readpvfbytime()  # DF objs contains vf data

# result processing modes
mode0, mode1 = '32hpi', '3264'
metrics = ''

# # # PLOT SECTION III
# plot_bigpic(df3264, (30, 17))  # FIG1: 32bit-64bit
# plot_barchart3(df32io, df3264)  # FIG2: beam-32bit-64bit
# plot_pvfioo3(df32io, df3264)  # FIG3: 32io-32o3
# plt.show()
# plot_qpvf(df32io, df32qpvf)  # FIG4: 32io-32qpvf
# # # FIG5: cumulative vf 32io, 32qpvf;





# # FIG6: QSORT VS QSORTiter
qsortvf = VFDataWrapperExtraction('qsort_cmp.csv', []).readpvfbytime()
print(qsortvf)
appname = ['QSORT_ITER', 'QSORT']
plot_linechartcmp(qsortvf, appname)
plt.show()
# PLOT SECTION IV
applist = ['susan_s3', 'matrixmult', 'sha', 'aes_d', 'gsm', 'dijkstra']  # What is masking factor sweep
plotPVF1(d32io, 3, [30, 15], applist)
plt.tight_layout()
plt.show()

# # # Plot return comparison
dfcostgain_bigpic1 = costreturngroup(d32io, ['susan_s3', 'susan_e', 'susan_c'])
dfcostgain_bigpic2 = costreturngroup(d32io, ['matrixmult', 'matrixmultb_'])
dfcostgain_bigpic3 = costreturngroup(d32io, ['aes_d', 'sha'])
dfcostgain_bigpic4 = costreturngroup(d32io, ['dijkstra', 'fft'])
plotPVF2(2, [20, 18], [dfcostgain_bigpic1, dfcostgain_bigpic2, dfcostgain_bigpic3, dfcostgain_bigpic4])
plt.show()

dfcostgain1 = costreturngroup(d32io, ['matrixmult', 'matrixmultunroll'], pvfen=True)  # M-Return
dfcostgain2 = costreturngroup(d32io, ['susan_s3', 'susan_s3unroll'], pvfen=True)
dfcostgain3 = costreturngroup(d32io, ['sha', 'shaunroll'], pvfen=True)
applist1 = [dfcostgain1, dfcostgain2, dfcostgain3]
plotPVFdualaxis(3, [20, 6], applist1)
plt.show()

# # Fig: return deprivation by loop depth
a = returnbydepth(d32io, ['qsortvec25', 'qsortvec50', 'qsortvec100', 'qsortvec150'], [25, 50, 100, 150])
b = returnbydepth(d32io, ['susan_s3', 'susan_s4', 'susan_s6', 'susan_s10'], [3, 4, 6, 10])
plotPVF3(2, [15, 6], [a, b])
plt.show()

# # # Fig: return optimization by algorithm selection:
dfcostgain_4 = costreturngroup(d32io, ['matrixmultb_', 'matrixmult'], pvfen=True)
dfcostgain_5 = costreturngroup(d32io, ['qsort_iter', 'qsort'], pvfen=True)
applist2 = [dfcostgain_4, dfcostgain_5]
plotPVFdualaxis(2, [12, 5], applist2)
plt.show()


# Fig: return - PVF comparison curve
# dfcostgain_bigpic5 = costreturngroup(d32io, ['qsort', 'qsort_iter'], pvfen=True)
# print(dfcostgain_bigpic5)
# fig, ax1 = plt.subplots()
# ax = dfcostgain_bigpic5.iloc[:, 0::2].plot(ax=ax1, marker='s')
# ax.set_ylabel('Return')
# ax.set_ylim(0, 1)
# ax.set_xlabel('Masking Level')
# dfcostgain_bigpic5.iloc[:, 1::2].plot(secondary_y=True, ax=ax1, style='--', marker='v')
# ax.legend(loc='upper left')
# plt.legend(loc='upper right')
# plt.ylabel('PVF')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.grid()
# plt.show()

#  Numerical analysis: correlation and distance
# res1 = d3264.getsimilaritylist('arm32inorder.csv', mode1, metrics)
# res2 = d3264.getsimilaritylist('arm32inorder.csv', mode1, metrics)
# corr1 = d3264.getcorrelationlist(farmbase, mode0)
# corr2 = d32io.getcorrelationlist(farmbase, mode1)
# print(corr1)
# print(corr2)

# Beam-PVF correlation
# pvffinal = [0.55635, 0.52368, 0.29094, 0.61494, 0.48335, 0.7, 0.58321, 0.597, 0.641, 0.66581, 0.69142, 0.568]
# beam = [166, 165, 100, 395, 342, 405, 345, 470, 373, 323, 353, 280]
# print(np.corrcoef(pvffinal, beam))

# # COST-RETURN ANALYSIS
# wrapped_dataqpvf = VFDataWrapper('arm32vsarm64.csv', [])
# infos30 = wrapped_dataqpvf.getsweepinfo('aes_d')
# cost_steps = np.round(np.linspace(0, 0.9, 10), decimals=1)
# print(cost_steps)
# gain = []
# for c in cost_steps:
#     gain_i = wrapped_dataqpvf.gain(infos30, [0.0, c])
#     gain.append(gain_i)
# costgain = np.column_stack((cost_steps, gain))
# plt.plot(costgain[:, 0], costgain[:, 1])
# plt.title("PVF reduction response to masking: aes_d")
# plt.xlabel("Overall Masking")
# plt.ylabel("PVF reduction")
# plt.xticks(np.arange(0, 1, 0.1))
# plt.yticks(np.arange(0, 0.9, 0.1))

# print(res)
