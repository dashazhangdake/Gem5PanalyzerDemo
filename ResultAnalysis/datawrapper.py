import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import hmean
from scipy.stats import gmean
import scipy
from pathlib import Path
from scipy.spatial.distance import euclidean
from tslearn.metrics import dtw, dtw_path
import similaritymeasures


class VFDataWrapper:
    def __init__(self, filename, program_list):
        self.fname = filename
        self.nprogram = program_list

    # METHOD GROUP I : File manipulation methods
    def getbaselabel(self, basefile):  # When InOrder is the baseline, we call this function to get a list of
        # Apps to analyze
        data = pd.read_csv(basefile)
        labelinorder = data.columns.values[1::2]
        label = [lb[:-3] for lb in labelinorder]
        return label

    def label_gen(self, basefile):
        if not self.nprogram:
            print('empty program list, get basename from basefile please !')
            baselabel = self.getbaselabel(basefile)
        else:
            baselabel = self.nprogram
        if 'vs' in self.fname:
            baselabel = list(np.repeat(baselabel, 2))
            labels32 = [n + '32' for n in baselabel]
            labels32[::2] = ['T' + n for n in labels32[::2]]
            labels64 = [n + '64' for n in baselabel]
            labels64[::2] = ['T' + n for n in labels64[::2]]
            labelres = labels32 + labels64
        elif 'qpvf' in self.fname:
            labelres = list(np.repeat(baselabel, 2))
            labelres = ['Q' + n for n in labelres]
            labelres[::2] = ['T' + n for n in labelres[::2]]
        else:
            labelres = list(np.repeat(baselabel, 2))
            labelres[::2] = ['T' + n for n in labelres[::2]]
        return labelres

    def readfile(self, fname=None):
        if fname is None:
            df_vf = pd.read_csv(self.fname)
        else:
            df_vf = pd.read_csv(fname)
        return df_vf

    def readlastrow(self):  # PVFs at the final tick within the sampled program execution time frame
        data = self.readfile()
        finaltick_data = data.tail(1).iloc[:, 1::2]
        return finaltick_data

    def readfinaltick(self):  # the Final Tick within the sampled program execution time frame
        data = self.readfile()
        finaltick = data.tail(1).iloc[:, ::2]
        return finaltick

    def readpvfbytime(self):  # Select interested Data by labels, this method retrieves label names
        # from the 'program_list' input argument
        if 'vs' in self.fname:
            data = self.readfile()
        elif 'qpvf' in self.fname:  # This branch should be called ONLY when analyzing Q-PVF, accumulate
            # Quanta-time at the vertical direction
            data = self.readfile()
            data.iloc[:, ::2] = data.iloc[:, ::2].cumsum(axis=0)
        else:
            data = self.readfile()
        return data

    def accumulatetick(self):  # This function should be called ONLY when analyzing Q-PVF, accumulate
        # Quanta-time at the vertical direction
        data = self.readfile()
        data.iloc[:, ::2] = data.iloc[:, ::2].cumsum(axis=0)
        return data

    def getsweepinfo(self, appname):
        datasweep = []
        top_dir = Path(__file__).resolve().parent
        steps = np.round(np.linspace(0, 0.9, 10), decimals=1)
        dirlist = [appname + 'baseline' + str(ele) for ele in steps]
        dflist = []
        for i, name in enumerate(dirlist):
            sweepvfdir = top_dir / 'maskingsweep' / appname / name
            df_vf = pd.read_csv(sweepvfdir / (''.join([i for i in appname]) + 'baseline_pvf.csv'))
            datai = df_vf.to_numpy()
            if i == 0:
                dflist.append(datai[:, 0])
                dflist.append(datai[:, 1])
            else:
                dflist.append(datai[:, 1])
            datasweep = np.array(dflist).transpose()
        dimensionsx, dimensionsy = datasweep.shape
        datasweepframe = pd.DataFrame(data=datasweep[0:, 0:], index=[i for i in range(dimensionsx)],
                                      columns=['Tick'] + ['Masking = ' + str(i) for i in steps])
        return datasweepframe

    # METHOD GROUP II: Data Processing Methods
    def similarity_label_gen(self, label, mode='3264'):
        sim_pairs = []
        if mode == '3264':
            for i, apps in enumerate(label):
                simpair = ['T' + apps + '32', apps + '32', 'T' + apps + '64', apps + '64']
                sim_pairs.append(simpair)
        elif mode == '32hpi':
            for i, apps in enumerate(label):
                simpair = ['T' + apps + '32', apps + '32', 'T' + apps + 'HPI', apps + 'HPI']
                sim_pairs.append(simpair)
        return sim_pairs

    def similarity(self, data, labelselector, metric, normalization=True):  # This method computes frechet distance between
        # [Tick1, PVF1] and [Tick2, PVF2]
        x1 = data.loc[50::10, labelselector[0]]
        x2 = data.loc[50::10, labelselector[2]]
        y1 = data.loc[50::10, labelselector[1]]
        y2 = data.loc[50::10, labelselector[3]]
        if normalization is True:
            d1 = np.column_stack((x1.div(x1.iloc[-1]), y1))
            d2 = np.column_stack((x2.div(x2.iloc[-1]), y2))
        else:
            d1 = np.column_stack((x1, y1))
            d2 = np.column_stack((x2, y2))
        if metric is 'euclidean':
            distance = scipy.spatial.distance.cdist(d1, d2, 'euclidean')
            distance = sum(np.diagonal(distance))
        elif metric is 'frechet':
            distance = similaritymeasures.frechet_dist(d1, d2)
        elif metric is 'dtw':
            distance = dtw(y1, y2)
        else:
            distance = scipy.spatial.distance.cdist(d1, d2, 'euclidean')
            distance = sum(np.diagonal(distance))
        # # print(distance)
        # return distance / gmean([x1.iloc[-1], x2.iloc[-1]])
        if normalization is True:
            distance = distance
        else:
            distance = distance / gmean([x1.iloc[-1], x2.iloc[-1]])
        distance = [ "{:.2e}".format(x1.iloc[-1]/500),  "{:.2e}".format(x2.iloc[-1]/500)]
        return distance

    def correlation(self, data, labelselector):  # This method computes correlation between PVF1 and PVF2
        x1 = data.loc[50:, labelselector[0]]
        x2 = data.loc[50:, labelselector[2]]
        y1 = data.loc[50:, labelselector[1]]
        y2 = data.loc[50:, labelselector[3]]
        corr = np.corrcoef(y1, y2)
        # return distance / gmean([x1.iloc[-1], x2.iloc[-1]])
        # return distance / max(x1.iloc[-1], x2.iloc[-1])
        return corr

    def norml2(self, data, maskingpair):  # Measure the distance between sweeping curves
        y1 = data.loc[5:, 'Masking = ' + str(maskingpair[0])]
        y2 = data.loc[5:, 'Masking = ' + str(maskingpair[1])]
        diff = y1 - y2
        norm_y1y2 = np.linalg.norm(diff)
        return norm_y1y2

    def gain(self, data, maskingpair):
        y0 = data.loc[5:, 'Masking = ' + str(maskingpair[0])]
        y1 = data.loc[5:, 'Masking = ' + str(maskingpair[1])]
        reduction = ((y1 - y0) / y0).to_numpy()
        return hmean(abs(reduction))


class VFDataWrapperExtraction(VFDataWrapper):
    def getsimilaritylist(self, basefile, mode, metric):
        baselabels = self.getbaselabel(basefile)
        labels = self.label_gen(basefile)
        if mode == '3264':
            data = self.readpvfbytime().loc[:, labels]
        elif mode == '32hpi':
            data1 = self.readpvfbytime().loc[:, labels]
            data2 = self.readfile(basefile)
            data = pd.concat([data1, data2], axis=1)
        else:
            data = pd.DataFrame()
        simpairlabels = self.similarity_label_gen(baselabels, mode)
        rowname = []
        similarity_list = []
        for i in simpairlabels:
            rowname.append(i[0][1:-2])
            similarityi = self.similarity(data, i, metric)
            similarity_list.append(similarityi)
        dfsimilarity = pd.DataFrame({'Pair': rowname, 'similarity measurement': similarity_list},
                                    columns=['Pair', 'similarity measurement'])
        return dfsimilarity

    def getcorrelationlist(self, basefile, mode):
        baselabels = self.getbaselabel(basefile)
        labels = self.label_gen(basefile)
        if mode == '3264':
            data = self.readpvfbytime().loc[:, labels]
        elif mode == '32hpi':
            data1 = self.readpvfbytime().loc[:, labels]
            data2 = self.readfile(basefile)
            data = pd.concat([data1, data2], axis=1)
        else:
            data = pd.DataFrame()
        simpairlabels = self.similarity_label_gen(baselabels, mode)
        rowname = []
        similarity_list = []
        for i in simpairlabels:
            rowname.append(i[0][1:-2])
            similarityi = self.correlation(data, i)[1, 0]
            similarity_list.append(similarityi)
        dfsimilarity = pd.DataFrame({'Pair': rowname, 'correlation measurement': similarity_list},
                                    columns=['Pair', 'correlation measurement'])
        return dfsimilarity


if __name__ == "__main__":
    wrapped_dataqpvf = VFDataWrapper('arm32vsarm64.csv', [])
    baselabelsr = wrapped_dataqpvf.getbaselabel('arm32inorder.csv')
    labelsr = wrapped_dataqpvf.label_gen('arm32inorder.csv')
    print(baselabelsr)
    print(labelsr)
    pvf3264 = wrapped_dataqpvf.readpvfbytime().loc[:, labelsr]
    # sim1 = wrapped_dataqpvf.similarity(pvf3264, ['TSUSANS32', 'SUSANS32', 'TSUSANS64', 'SUSANS64'])
    # print(sim1)
