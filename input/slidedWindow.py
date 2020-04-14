'''
Created on Apr 4, 2017

Creation of DL datasets

@author: reiti
'''

import numpy
from PyQt5 import QtWidgets
from sklearn.preprocessing import MinMaxScaler



def manuDataSplitDL(guybrush, gui):
    gui.listWidget_trainingdata.clear()
    gui.listWidget_ValidData.clear()
    gui.listWidget_testingdata.clear()

    dataset = guybrush.sources[gui.comboBox_SourceSplit.currentIndex()]

    split = int((guybrush.getSetSizes()[0]/100) * len(data))

    for i in range(len(data)):
        if (i <= split):
            gui.listWidget_trainingdata.insertItem(i, "Dataset " + str(i+1))                
        else:
            gui.listWidget_testingdata.insertItem(i-split, "Dataset " + str(i+1))   


### SLIDED WINDOW ###


def DLWindow(gui, guybrush):
    def create_dataset(dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back)]
            dataX.append(a)
            dataY.append(dataset[i + look_back])
        return numpy.array(dataX), numpy.array(dataY)

    def create_Dataset_DL(dataset, look_back):
        inputID = guybrush.getInputDL()
        outputID = guybrush.getOutputDL()

        dataX, dataY, inX = [], [], []

        for i in range(len(dataset)-look_back-1):
            for k in range(i,i+look_back):
                for j in range(len(inputID)):
                    #INPUT
                    inX.append(dataset[k, inputID[j]])
            dataX.append(inX)
            inX=[]
            #OUTPUT
            outY=[]
            for l in range(len(outputID)):
                outY.append(dataset[i + look_back, outputID[l]])
            dataY.append(outY)
            outY=[]
        return numpy.array(dataX), numpy.array(dataY)

    dataset = guybrush.getDataset()
    
    look_back = guybrush.getWindowSize()
    #dataset = scaler.fit_transform(dataset)

    # DATASET DL PREP ---------------------------------------------------
    trainX = []
    trainY = []
    for i in range(0,gui.listWidget_trainingdata.count()): #Anzahl der Blöcke, z.B. 3 Tage
        trainX.append([])
        trainY.append([])
        for j in range(0,guybrush.getNumDevices()):
            trainX1, trainY1 = create_dataset(dataset[i][j], look_back)
            trainX[i].append(trainX1)
            trainY[i].append(trainY1)
    
    testX = []
    testY = []
    for i in range(0,gui.listWidget_testingdata.count()):
        testX.append([])
        testY.append([])
        for j in range(0,guybrush.getNumDevices()):
            testX1, testY1 = create_dataset(dataset[i+gui.listWidget_trainingdata.count()][j], look_back)
            testX[i].append(testX1)
            testY[i].append(testY1)
        
    ###########
    ### GUI ###
    ###########
    
    gui.tableDatasetDL.setRowCount(len(trainX[0][0]))
    gui.tableDatasetDL.setColumnCount(len(guybrush.getInputDL())*look_back + len(guybrush.getOutputDL()))

    for i in range(0, len(trainX[0][0])):
        for j in range (0, len(guybrush.getInputDL())*look_back):
            gui.tableDatasetDL.setItem(i, j, QtWidgets.QTableWidgetItem(str(trainX[0][guybrush.getInputDL()[j%len(guybrush.getInputDL())]][i][int(j/look_back)])))
        for k in range (0, len(guybrush.getOutputDL())):
            gui.tableDatasetDL.setItem(i, len(guybrush.getInputDL())*look_back+k, QtWidgets.QTableWidgetItem(str(trainY[0][guybrush.getOutputDL()[k]][i])))

    ### LABELS ###        
    labels = guybrush.getLabels()
    labelsDL = []
    for i in range(0, look_back):
        for j in range(0, len(guybrush.getInputDL())):
            labelsDL.append(labels[guybrush.getInputDL()[j]]+"(t-"+str(look_back-i)+")")
    for k in range(0, len(guybrush.getOutputDL())):
        labelsDL.append(labels[guybrush.getOutputDL()[k]]+"(t)")

    gui.tableDatasetDL.setHorizontalHeaderLabels(labelsDL)

    #print(dataset)
    return [trainX,trainY,testX,testY]
    
