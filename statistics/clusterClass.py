import sklearn
from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import csv
import math
from matplotlib import rcParams
import bisect
from keras.utils.vis_utils import plot_model
import collections
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np

from PyQt5 import QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

def simpleCluster(guybrush, gui):
    data = guybrush.getDataset()
    
    #simple Clustering
    for i in range(len(guybrush.getLabels())):
        if "delay" in guybrush.getLabels()[i] or "Delay" in guybrush.getLabels()[i]:
            df = pd.DataFrame(data[0][i])
            desc = df.describe()
            print(len(desc))
            for k in range(len(data)):
                for j in range(len(data[k][i])):
                    if(data[k][i][j] < 2):
                        data[k][i][j] = 1
                    elif(data[k][i][j] >= 2 and data[0][i][j] <= 4):
                        data[k][i][j] = 2
                    else:
                        data[k][i][j] = 3
    guybrush.updateDataset(data)


def kMean(gui,guybrush):
    def plot_kMeanclusters(data, algorithm, args, kwds):
        labels = algorithm(*args, **kwds).fit_predict(data)
        kmeans_model = sklearn.cluster.KMeans(n_clusters=nclust).fit(data)

        gui.figure = plt.figure()
        gui.canvas = FigureCanvas(gui.figure)
        gui.toolbar = NavigationToolbar(gui.canvas, gui)
        gui.tabWidget_4.insertTab(0, gui.canvas, "kMean ")
        
        ax = gui.figure.add_subplot(1,1,1)

        print(kmeans_model.cluster_centers_)
		#end_time = time.time()
        palette = sns.color_palette('deep', np.unique(labels).max() + 1)
        colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
        sns.set(font='serif')
        ax.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        ax.set_xlabel('$\Delta flights$')
        ax.set_ylabel('$|\overline{delay}|$ (min)')
        #plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        #plt.xlabel('$\Delta flights$')
        #plt.ylabel('$|\overline{delay}|$ (min)')
        #frame = plt.gca()
        #frame.axes.get_xaxis().set_visible(False)
        #frame.axes.get_yaxis().set_visible(False)
        #plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)
        #plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)
        
        print(len(labels))
        target_value = "kMean"
        #guybrush.mst_file.insert((labels.shape[1]),target_value,labels)
        counter=collections.Counter(labels)
        #print(counter)
        #labels = pd.DataFrame(labels)
        #mst_file.insert((labels.shape[1]),target_value,labels)
        # 3rd sept
        #print(labels[7442:7489])
        #plt.close()

    sns.set_context('poster')
    sns.set_color_codes()
    plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0.1}

    nclust = int(gui.lineEdit_Classes.text())

    labels = guybrush.getLabels()
    dataset = guybrush.mst_file

    indicators = [x.row() for x in gui.listClassification.selectedIndexes()]
    # = [gui.listClassification.item(i).text() for i in range(gui.listClassification.rowCount())]

    dataset1 = np.asarray(dataset[0][labels[int(indicators[0])]])
    dataset2 = np.asarray(dataset[0][labels[int(indicators[1])]])
    for i in range(1,len(dataset)):
        dataset1 = np.append(dataset1,np.asarray(dataset[i][labels[int(indicators[0])]]))
        dataset2 = np.append(dataset2,np.asarray(dataset[i][labels[int(indicators[1])]]))

    for k in range(len(dataset2)):
        if(dataset2[k] == np.inf or math.isnan(dataset2[k])):
            dataset2[k] = 0
        if(dataset2[k] > 100):
            dataset2[k] = 0

    #dataset2.append(dataset[1][labels[int(indicators[0])]])
    data = np.asarray(list(zip(dataset1, dataset2)))	
    plot_kMeanclusters(data, cluster.KMeans, (), {'n_clusters':nclust})
    


def SVM(guybrush, gui):
    print("SVM")
    print(guybrush.mst_file)