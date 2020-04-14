'''
Created on Mar 22, 2017

@author: reiti
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.stattools import grangercausalitytests
import SALib

from output import murray2D

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def test_corrmatrix(gui, guybrush, nX):
    dataset = np.asarray(guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()])
    labels = guybrush.getLabels()
    df = pd.DataFrame(dataset)
    df1 = df.transpose()
    #print(df1)
    corrmethod = str(gui.comboBox_corrMethod.currentText())
    cax = df1.corr(method=corrmethod, min_periods=1)
    plt.matshow(df1.corr())
    print(cax)
    plt.savefig("results/matrix_test.png")
    pixmap = QPixmap("results/matrix_test.png")
    gui.label_CorrMatrix.setPixmap(pixmap)

    for i in range(0, guybrush.getNumDevices()):
        for j in range (0, guybrush.getNumDevices()):
            gui.tableDep.setItem(j, i, QtWidgets.QTableWidgetItem(str(cax[i][j])))

def test_rollingstat(gui, guybrush, nX, window):

    def smooth(y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    data = np.asarray(guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()][guybrush.mst_labels[gui.comboBox_PI.currentIndex()]])
    
    rolmean = smooth(data, window)
    murray2D.plotFocusSelect(gui, guybrush, data, rolmean)

def test_correlation(gui, guybrush, nX, window):
    #ACF PACF

    def acf(x):
        length=20
        return numpy.array([1]+[numpy.corrcoef(x[:-i], x[i:]) \
            for i in range(1, length)])

    data = guybrush.getDataset()
    dataset = data[gui.comboBox_DS.currentIndex()][nX][:]
    '''
    #plt.rc('font', size=16)
    ts_log = numpy.log(dataset)
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)
    lag_acf = acf(ts_log_diff, nlags=window)
    lag_pacf = pacf(ts_log_diff, nlags=window, method='ols')

    #plt.subplot(121)
    plt.plot(lag_acf)
    plt.xlabel("Lag of Auto Correlation")
    plt.ylabel("ACF")
    plt.legend(loc=2, fontsize='xx-large')
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/numpy.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/numpy.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    #plt.title('Autokorrelation Delay-Zeitreihe')
    #Plot PACF:
    #plt.subplot(122)
    #plt.plot(lag_pacf)
    #plt.axhline(y=0,linestyle='--',color='gray')
    #plt.axhline(y=-1.96/numpy.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    #plt.axhline(y=1.96/numpy.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    #plt.title('Partial Autocorrelation Function')
    #plt.tight_layout()
    plt.savefig("/home/reiti/Nextcloud/PhD/Paper/CEAS_Journal_Framework/results/autocorr.pdf")
    #plt.show()
    '''

    #print(acf(dataset))

def test_decomp(gui, guybrush, nX, window):
    # TREND SAISONALITY

    data = guybrush.getDataset()
    dataset = data[gui.comboBox_DS.currentIndex()][nX][:]
    
    result = seasonal_decompose(dataset, model='additive')
    print(result.trend)
    print(result.seasonal)
    print(result.resid)
    print(result.observed)

    '''
    ts_log = numpy.log(dataset)
    decomposition = seasonal_decompose(ts_log, freq=window)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    ts_log_decompose = residual
    ts_log_decompose.dropna(inplace=True)
    test_stationarity(ts_log_decompose)
    plt.subplot(311)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(312)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(313)
    plt.plot(seasonal,label='Seasonality')
    plt.legend(loc='best')
    #plt.subplot(414)
    #plt.plot(residual, label='Residuals')
    #plt.legend(loc='best')
    #plt.tight_layout()
    '''
    #plt.savefig("/home/reiti/Documents/PhD/Paper/DLRK2017/LaTex/Graphics/results/decomp.eps")
    #plt.show()

def test_stationarity(gui, guybrush, nX):
    #dataset = guybrush.getDataset()[:,nX]

    labels = guybrush.mst_labels
    dataset = np.asarray(guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()][guybrush.mst_labels[gui.comboBox_PI.currentIndex()]])
    #Perform Dickey-Fuller test:
    dftest = adfuller(dataset, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    #print (dfoutput)
    gui.label_DF4.setText(str(dfoutput[0])[0:6])
    gui.label_DF5.setText(str(dfoutput[1])[0:6])
    gui.label_DF1.setText(str(dfoutput[5])[0:6])
    gui.label_DF2.setText(str(dfoutput[4])[0:6])
    gui.label_DF3.setText(str(dfoutput[6])[0:6])