'''
Created on Mar 29, 2017

@author: reiti
'''
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem
import numpy as np

def tableInit(gui, guybrush):    
    gui.tableData.clear()
    '''
    dataset = guybrush.getDataset() 

    guybrush.setNumData(len(dataset[0][0]))
    
    gui.tableData.setColumnCount(guybrush.getNumDevices())
    gui.tableData.setRowCount(guybrush.getNumData())
    gui.tableData.setHorizontalHeaderLabels(guybrush.getLabels())
    #self.tableData.setHorizontalHeaderLabels(str(guybrush.getNameDevices()))
       
    for i in range(0, guybrush.getNumDevices()):
        for j in range (0, guybrush.getNumData()):
            gui.tableData.setItem(j, i, QtWidgets.QTableWidgetItem(str(dataset[0][i][j])))
    '''                    
    gui.tableDep.setColumnCount(guybrush.num_devices)
    gui.tableDep.setRowCount(guybrush.num_devices)
    gui.tableDep.setHorizontalHeaderLabels(guybrush.mst_labels)
    gui.tableDep.setVerticalHeaderLabels(guybrush.mst_labels)
        
    for i in range(0, guybrush.num_devices):
        for j in range (0, guybrush.num_devices):
            gui.tableDep.setItem(j, i, QtWidgets.QTableWidgetItem("N/D"))
    
    gui.tableNeuroW.setColumnCount(guybrush.num_devices)
    gui.tableNeuroW.setRowCount(10)
    gui.tableNeuroW.setHorizontalHeaderLabels(guybrush.mst_labels) 

def treeBuild(gui, guybrush):
    gui.treeData.clear()    
    #self.treeData.setHeaderLabel("World")
    gui.treeData.setColumnCount(guybrush.num_devices + 1)
    gui.treeData.setColumnWidth(0,180)
    #gui.treeData.setHeaderLabels(["t"] + guybrush.getLabels())
    gui.treeData.setHeaderLabels(guybrush.mst_labels)
    gui.comboBox_DS_2.clear()
    gui.comboBox_DS.clear()

    for m in range(len(guybrush.sources)):
        l0 = QTreeWidgetItem(["Source " + str(m+1)])
        gui.treeData.addTopLevelItem(l0)
        for k in range(len(guybrush.sources[m])): 
            data = guybrush.sources[m][k]       
            l1 = QTreeWidgetItem(["Dataset " + str(k+1)])
            l0.addChild(l1) 
            # Combo Boxes 
            gui.comboBox_DS.addItem("Dataset " + str(k+1))
            gui.comboBox_DS_2.addItem("Dataset " + str(k+1))
            for i in range(guybrush.num_data): 
                temp = list()
                for j in range(len(guybrush.mst_labels)): 
                    temp.append(str(data[guybrush.mst_labels[j]][i]))
                l1_child = QTreeWidgetItem(temp) 
                l1.addChild(l1_child)
                temp.clear()

    labels = guybrush.mst_labels
    if(len(guybrush.sources) < 2):
        for i in range(0, len(labels)):
            gui.comboBox_PI.addItem(labels[i])
            gui.comboBox_SplitFeatures.addItem(labels[i])
            gui.listInput.insertItem(i, labels[i])
            gui.listOutput.insertItem(i, labels[i])
            # Grand Tour:
            gui.listInput_GT.insertItem(i, labels[i])
            gui.listInput_GT_2.insertItem(i, labels[i])
            gui.listInput_GT_3.insertItem(i, labels[i])
            gui.listClassification.insertItem(i, labels[i])
    
    ####### Source Combo Boxes
    gui.comboBox_Source.clear()
    gui.comboBox_Source2.clear()
    gui.comboBox_SourceSplit.clear()
    for k in range(len(guybrush.sources)):
        gui.comboBox_Source.addItem("Source " + str(k+1))
        gui.comboBox_Source2.addItem("Source " + str(k+1))
        gui.comboBox_SourceSplit.addItem("Source " + str(k+1))

##### OLD AND SOLD ########

def treeInit(gui, guybrush):
    gui.treeData.clear()    
    #self.treeData.setHeaderLabel("World")
    gui.treeData.setColumnCount(guybrush.getNumDevices() + 1)
    gui.treeData.setColumnWidth(0,180)
    gui.treeData.setHeaderLabels(["t"] + guybrush.getLabels())

    gui.comboBox_DS_2.clear()
    gui.comboBox_DS.clear()
    #combo boxes
    for m in range(len(guybrush.getSources())):
        l0 = QTreeWidgetItem(["Source " + str(m+1)])
        gui.treeData.addTopLevelItem(l0)
        data = guybrush.sources[m]
        for k in range(len(data)):            
            l1 = QTreeWidgetItem(["Dataset " + str(k+1)])
            # Combo Boxes 
            gui.comboBox_DS.addItem("Dataset " + str(k+1))
            gui.comboBox_DS_2.addItem("Dataset " + str(k+1))
            l0.addChild(l1)
            #data = guybrush.getDataset()
            #data = guybrush.getSources()[m]
            guybrush.setNumData(len(data[k][0]))            
            for i in range(guybrush.getNumData()):
                data_items = []
                data_items.append(str(i))
                for j in range(guybrush.getNumDevices()):
                    data_items.append(str(data[k][j][i]))
                l1_child = QTreeWidgetItem(data_items) 
                l1.addChild(l1_child)
    #self.treeData.addTopLevelItems(l1)
    
    labels = guybrush.getLabels()
    if(len(guybrush.getSources()) < 2):
        for i in range(0, len(labels)):
            gui.comboBox_PI.addItem(labels[i])
            gui.comboBox_SplitFeatures.addItem(labels[i])

            gui.listInput.insertItem(i, labels[i])
            gui.listOutput.insertItem(i, labels[i])
            # Grand Tour:
            gui.listInput_GT.insertItem(i, labels[i])
            gui.listInput_GT_2.insertItem(i, labels[i])
            gui.listInput_GT_3.insertItem(i, labels[i])
            gui.listClassification.insertItem(i, labels[i])
    
    ####### Source Combo Boxes

    gui.comboBox_Source.clear()
    gui.comboBox_Source2.clear()
    gui.comboBox_SourceSplit.clear()
    for k in range(len(guybrush.getSources())):
        gui.comboBox_Source.addItem("Source " + str(k+1))
        gui.comboBox_Source2.addItem("Source " + str(k+1))
        gui.comboBox_SourceSplit.addItem("Source " + str(k+1))
