'''
Created on Mar 13, 2017
@author: Reiti
'''

from PyQt5 import QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D #@UnresolvedImport
from matplotlib import cm, rcParams
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import matplotlib.dates as mdates
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from sklearn.ensemble import ExtraTreesClassifier

import seaborn as sns
import pandas as pd

#plt.style.use('dark_background')

def prePlot(gui, guybrush):
    dataset = guybrush.sources[gui.comboBox_Source2.currentIndex()]
    
    #print(dataset)
    #delimiter = guybrush.delimiter
    delimiter = guybrush.delimiter
    mult = int(gui.comboBox_DS_2.currentIndex())

    gui.tabWidget_4.clear()

    a = ["Datum","Zeit","AC","Origin","Destination","Flight NR","type"]
    # how many atmap scores and kpi?
    if(not(guybrush.mst_file.endswith('.dat'))):
        # non-boarding
        matches = guybrush.num_devices
        for item in a:    
            if item in guybrush.mst_labels:
                matches -= 1
        for item in guybrush.mst_labels:
            if "score" in item:
                atmap_count = 6
                break
            else:
                atmap_count = 0 
    else:
        # boarding
        matches = 4
        atmap_count = 0

    matches -= atmap_count

    gui.figure = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]
    gui.canvas = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]
    gui.toolbar = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]

    for i in range (int(matches/4) + 1 + int(atmap_count/6)):
        gui.figure[i] = plt.figure()
        gui.canvas[i] = FigureCanvas(gui.figure[i])
        gui.toolbar[i] = NavigationToolbar(gui.canvas[i], gui)

    for i in range(int(matches/4) + 1 + int(atmap_count/6)):
        gui.tabWidget_4.insertTab(i, gui.canvas[i], "Pre-Plot Dataset KPI " + str(gui.comboBox_DS_2.currentIndex()+1))
    
    if(not(guybrush.mst_file.endswith('.dat'))):
        # all non-dat files here comprise ATMAP data     
        gui.tabWidget_4.insertTab(int(matches/4), gui.canvas[int(matches/4)+1], "Pre-Plot Dataset ATMAP " + str(gui.comboBox_DS_2.currentIndex()+1))
    
    # plot prep
    offset = np.zeros(guybrush.num_data)
    colors = plt.cm.BuPu(np.linspace(0, 0.5, 6))
    cell_text = []
    rlabels = []
    clabels = np.linspace(0,guybrush.num_data,1)

    ax = [None]*guybrush.num_devices
    count = 0
    count2 = 0
    for i in range(0, guybrush.num_devices):    
        if(not(any(x in guybrush.mst_labels[i] for x in a)) and not "score" in guybrush.mst_labels[i]):
            # ATM or Boarding Plots
            ax[i] = (gui.figure[int(count2/4)].add_subplot(count2%4 + 411))
            sns.lineplot(x="Zeit", y=guybrush.mst_labels[i], data=dataset[0], ax=ax[i])
            #ax[i].plot(dataset[0][i])
            ax[i].set_ylabel(guybrush.mst_labels[i])
            count2 += 1            
        elif("score" in guybrush.mst_labels[i]):
            # ATMAP plots
            ax[i] = (gui.figure[int(matches/4)+1].add_subplot(count+611))
            sns.lineplot(x="Zeit", y=guybrush.mst_labels[i], data=dataset[0], ax=ax[i])
            #ax[i].plot(dataset[0][i])
            ax[i].set_ylabel(guybrush.mst_labels[i])
            count += 1        

def prePlotting2D(gui, guybrush):
    '''
    def seabornplot():

        tips = sns.load_dataset("tips")
        g = sns.FacetGrid(tips, col="sex", hue="time", palette="Set1",
                                hue_order=["Dinner", "Lunch"])
        g.map(plt.scatter, "total_bill", "tip", edgecolor="w")
        return g.fig

    gui.figure = seabornplot()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    #gui.tabWidget_3.removeTab(0)
    #gui.tabWidget_3.removeTab(0)
    gui.tabWidget_3.insertTab(0, gui.canvas, "Radar Plot")
    #dataset = guybrush.getDataset()               
    '''

    dataset = guybrush.getDataset()
    gui.tabWidget_4.clear()

    data = pd.DataFrame(dataset[0])
    data = data.transpose()

    a = ["Zeit","AC","Origin","Destination","Flight NR","type"]
    # how many atmap scores and kpi?
    if(not(guybrush.getFile().endswith('.dat'))):
        # non-boarding
        matches = guybrush.getNumDevices()
        for item in a:    
            if item in guybrush.getLabels():
                matches -= 1
        for item in guybrush.getLabels():
            if "score" in item:
                atmap_count = 6
                break
            else:
                atmap_count = 0 
    else:
        # boarding
        matches = 4
        atmap_count = 0

    matches -= atmap_count

    gui.figure = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]
    gui.canvas = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]
    gui.toolbar = [0 for x in range(int(matches/4) + 1 + int(atmap_count/6))]

    for i in range (int(matches/4) + 1 + int(atmap_count/6)):
        gui.figure[i] = plt.figure()
        gui.canvas[i] = FigureCanvas(gui.figure[i])
        gui.toolbar[i] = NavigationToolbar(gui.canvas[i], gui)

    for i in range(int(matches/4) + 1 + int(atmap_count/6)):
        gui.tabWidget_4.insertTab(i, gui.canvas[i], "Pre-Plot Dataset KPI " + str(gui.comboBox_DS_2.currentIndex()+1))
    
    if(not(guybrush.getFile().endswith('.dat'))):
        # all non-dat files here comprise ATMAP data     
        gui.tabWidget_4.insertTab(int(matches/4), gui.canvas[int(matches/4)+1], "Pre-Plot Dataset ATMAP " + str(gui.comboBox_DS_2.currentIndex()+1))
    
    # plot prep
    offset = np.zeros(guybrush.getNumData())
    colors = plt.cm.BuPu(np.linspace(0, 0.5, 6))
    cell_text = []
    rlabels = []
    clabels = np.linspace(0,guybrush.getNumData(),1)
   
    #plot2D_new(gui, guybrush)
    count = 0
    count2 = 0
    for i in range(0, guybrush.getNumDevices()):    
        if(not(any(x in guybrush.getLabels()[i] for x in a)) and not "score" in guybrush.getLabels()[i]):
            # ATM or Boarding Plots
            ax2 = gui.figure[int(count2/4)].add_subplot(4,1,count2%4 + 1,facecolor='white')
            #ax.plot(dataset[:,i],color="black",lw=0.3)
            #ax.plot(dataset[0][i,:],color="black",lw=0.3)
            ax2.plot(dataset[gui.comboBox_DS_2.currentIndex()][i][0:guybrush.getNumData()],color="black",lw=0.3, marker="+")
            ax2.axhline(y=0.0, color='r', linestyle=':',lw=1.0)
            ax2.set_ylabel(guybrush.getLabels()[i])
            if(not(guybrush.getFile().endswith('.dat'))):
                ax2.set_xlabel("t (30min)")
            else:
                ax2.set_xlabel("t (s)")  
            gui.figure[int(count2/4)].subplots_adjust(hspace = 1.0)
            count2 += 1
        elif("score" in guybrush.getLabels()[i]):
            # ATMAP plots
            ax = gui.figure[int(matches/4)+1].add_subplot(6,1,count+1,facecolor='white')
            #x = np.array([datetime.datetime(2016, 1, 1, j, i) for j in range(6,22,1) for i in range(0,60,30)])
            ax.plot(dataset[gui.comboBox_DS_2.currentIndex()][i][0:guybrush.getNumData()],color="black",lw=0.3, marker="+")
            ax.axhline(y=0.0, color='r', linestyle=':',lw=1.0)
            ax.set_ylabel(guybrush.getLabels()[i])
            ax.set_xlabel("t (30min)")
            gui.figure[int(matches/4)+1].subplots_adjust(hspace = 1.0)
            count += 1
        
def plot2D(gui, dataset, guybrush):  
    gui.tabWidget_4.clear()
    if(not(guybrush.getFile().endswith('.dat'))):
        # all non-dat files here comprise ATMAP data
        gui.figure2 = plt.figure()    
        gui.canvas = FigureCanvas(gui.figure2)
        gui.toolbar = NavigationToolbar(gui.canvas, gui)        
        gui.tabWidget_4.insertTab(0, gui.canvas, "Pre-Plot Dataset KPI " + str(gui.comboBox_DS_2.currentIndex()+1))
    gui.figure = plt.figure()    
    gui.canvas2 = FigureCanvas(gui.figure)
    gui.toolbar2 = NavigationToolbar(gui.canvas2, gui)
    gui.tabWidget_4.insertTab(1, gui.canvas2, "Pre-Plot Dataset ATMAP " + str(gui.comboBox_DS_2.currentIndex()+1))
    count = 0
    count2 = 0

    # how many atmap scores?
    a = ["Zeit","AC","Origin","Destination","Flight NR","type"]
    matches = 0
    for item in a:    
        if item in guybrush.getLabels():
            matches += 1
    for item in guybrush.getLabels():
        if "score" in item:
            atmap_count = 6
            break
        else:
            atmap_count = 0 

    # plot prep
    offset = np.zeros(guybrush.getNumData())
    ax = gui.figure.add_subplot(2,1,1,facecolor='white')
    colors = plt.cm.BuPu(np.linspace(0, 0.5, 6))
    cell_text = []
    rlabels = []
    clabels = np.linspace(0,guybrush.getNumData(),1)

    # plotting
    for i in range(0, guybrush.getNumDevices()):
        if("score" in guybrush.getLabels()[i]):
            # ATMAP plots
            #ax = gui.figure.add_subplot(6,1,count+1,facecolor='white')
            '''
            for j in range(guybrush.getNumData()):
                pltlab = ax.bar(j,dataset[gui.comboBox_DS_2.currentIndex()][i][j] + offset[j], bottom=offset[j], color=colors[count])
                offset[j] += dataset[gui.comboBox_DS_2.currentIndex()][i][j]              
            rlabels.append(guybrush.getLabels()[i])    
            count += 1

            '''
            ax = gui.figure.add_subplot(6,1,count+1,facecolor='white')
            ax.plot(dataset[gui.comboBox_DS_2.currentIndex()][i][0:guybrush.getNumData()],color="black",lw=0.3)
            ax.axhline(y=0.0, color='r', linestyle=':',lw=1.0)
            ax.set_ylabel(guybrush.getLabels()[i])
            ax.set_xlabel("t (30min)")
            gui.figure.subplots_adjust(hspace = 1.0)
            count += 1
            
        #elif("Zeit" not in guybrush.getLabels()[i] and "AC" not in guybrush.getLabels()[i]):
        elif(not(any(x in guybrush.getLabels()[i] for x in a))):
            # ATM or Boarding Plots
            ax2 = gui.figure2.add_subplot(guybrush.getNumDevices()-matches-atmap_count,1,count2+1,facecolor='white')
            #ax.plot(dataset[:,i],color="black",lw=0.3)
            #ax.plot(dataset[0][i,:],color="black",lw=0.3)
            ax2.plot(dataset[gui.comboBox_DS_2.currentIndex()][i][0:guybrush.getNumData()],color="black",lw=0.3)
            ax2.axhline(y=0.0, color='r', linestyle=':',lw=1.0)
            ax2.set_ylabel(guybrush.getLabels()[i])
            ax2.set_xlabel("t (s)")
            gui.figure2.subplots_adjust(hspace = 1.0)
            count2 += 1
    '''
    colors = colors[::-1]
    cell_text.reverse()
    ax = gui.figure.add_subplot(2,1,2,facecolor='white')
    ax.table(cellText=cell_text,rowLabels=rlabels,
                      rowColours=colors,
                      colLabels=clabels,
                      loc='bottom')
    '''    
    
def plotXY(gui, dataset, guybrush, n):
    gui.figure = plt.figure()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    gui.tabWidget_4.insertTab(n, gui.canvas, "Dataset " + str(gui.comboBox_DS_2.currentIndex()+1) + " XY " + guybrush.getLabels()[n])
    
    for i in range(0, guybrush.getNumDevices()-1):
        if i != n: 
            ax = gui.figure.add_subplot(guybrush.getNumDevices(),1,i+1)
            ax.plot(dataset[gui.comboBox_DS_2.currentIndex()][n,:],dataset[0][i,:],linewidth=0.1, marker="o", markersize=0.5, color="black")
            ax.set_ylabel(guybrush.getLabels()[i])
            ax.set_xlabel(guybrush.getLabels()[n])    
            
def plotModel(guybrush, gui):
    gui.label = QtWidgets.QLabel()
    gui.preview = QtGui.QPixmap(guybrush.getModelName()) 
    gui.label.setPixmap(gui.preview)   
    gui.tabWidget_4.insertTab(0, gui.label, "Neural Network Conception Plot")

def plotPredict(guybrush,gui,trainPredict,trainY):  
    look_back = 5
    gui.figure = plt.figure()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    gui.tabWidget_4.insertTab(0, gui.canvas, "trainPredict")
    ax = gui.figure.add_subplot(1,1,1)

    #trainY = trainY.reshape((len(trainY), 1))

    #testPredictPlot = np.empty_like(trainY)
    #testPredictPlot[:, :] = np.nan
    #testPredictPlot[len(trainPredict)+(look_back*2)+1:len(trainY)-1, :] = trainPredict
    

    ax.plot(trainPredict, linewidth=1.0, alpha=0.3, color="grey")
    ax.plot(trainY, linewidth=1.0, linestyle='-.', color="green")
    #plt.axvline(x=len(trainPredict)+look_back, lw=1.0, linestyle=':')
    #plt.axvline(x=len(trainPredict)+(look_back*2)+1, lw=1.0, linestyle=':')
    

def plotFocusSelect(gui, guybrush, dataset, dataset2):
    def onselect(xmin, xmax):
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x) - 1, indmax)

        thisx = x[indmin:indmax]
        thisy = y[indmin:indmax]
        line2.set_data(thisx, thisy)
        ax2.set_xlim(thisx[0], thisx[-1])
        ax2.set_ylim(thisy.min(), thisy.max())
        gui.canvas.draw()
    
    gui.figure = plt.figure()    
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    gui.tabWidget_4.insertTab(0, gui.canvas, "Focus-Plot")

    x = []
    for i in range(len(dataset)):
        x.append(i)
    y = np.asarray(dataset)

    ### PLOTTING ####################################################

    ax = gui.figure.add_subplot(211)
    ax.plot(x,y, color="black",lw=0.3, marker="+", label='Original')
    ax.plot(dataset2, color="grey",lw=1.0, linestyle=":", label='Smoothed Component', marker="p")
    #ax.plot(dataset2)
    ax.set_ylabel(guybrush.mst_labels[gui.comboBox_PI.currentIndex()])
    ax.set_xlabel("t")
    ax.legend()

    ax2 = gui.figure.add_subplot(212)
    line2, = ax2.plot(x,y, label='Original', color="black",lw=0.3, marker="+")
    ax2.plot(dataset2, color='grey', label='Smoothed Component',lw=1.0, linestyle=":", marker="p")
    ax2.set_ylabel(guybrush.mst_labels[gui.comboBox_PI.currentIndex()])
    ax2.set_xlabel("t")
    ax2.legend()
    # set useblit True on gtkagg for enhanced performance
    gui.figure.span = SpanSelector(ax, onselect, 'horizontal', useblit=True,rectprops=dict(alpha=0.3, facecolor='red'))
    
