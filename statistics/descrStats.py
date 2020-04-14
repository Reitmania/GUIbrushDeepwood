import pandas as pd
import numpy as np 
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem


def Stats(gui, guybrush):
    delimiter = guybrush.delimiter
    #single dataset
    #data = pd.DataFrame(guybrush.getSources()[gui.comboBox_Source2.currentIndex()][gui.comboBox_DS_2.currentIndex()])
    mult = int(gui.comboBox_DS_2.currentIndex())
    #data = guybrush.sources[gui.comboBox_Source2.currentIndex()][mult*delimiter:delimiter+mult*delimiter].values    
    data = guybrush.sources[gui.comboBox_Source2.currentIndex()]
    #data = guybrush.datasetRaw
    #data = data[guybrush.mst_labels].iloc[mult*delimiter:delimiter+mult*delimiter]
    data = data[mult]
    description = data.describe()
    description = np.asarray(description)   
    
    #data = pd.DataFrame(guybrush.getDataset()[gui.comboBox_DS_2.currentIndex()])
    #description = data.apply(pd.Series.describe, axis=1)
    #description = data.describe()
    #description = np.asarray(description)
    gui.tableData.clear()

    label = ["count","mean","std", "min","25.00","50.00","75.00","max"]
    
    #gui.tableData.setColumnCount(len(description[gui.comboBox_DS_2.currentIndex()]))
    gui.tableData.setColumnCount(len(label))
    gui.tableData.setRowCount(guybrush.num_devices-1)
    gui.tableData.setVerticalHeaderLabels(guybrush.mst_labels[1:])
    gui.tableData.setHorizontalHeaderLabels(label)

    #print(description)

    #for i in range(len(description[gui.comboBox_DS_2.currentIndex()])):
    for i in range(len(label)):
        for j in range(guybrush.num_devices-1):
            gui.tableData.setItem(j, i, QtWidgets.QTableWidgetItem(str(description[i][j])))

    #np.savetxt("Descr.csv", description, delimiter=",")