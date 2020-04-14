'''
Created on Apr 4, 2017

Creation of DL datasets

@author: reiti
'''

import numpy
from PyQt5 import QtWidgets
from sklearn.preprocessing import MinMaxScaler
from random import shuffle
from collections import OrderedDict
from sklearn.preprocessing import MinMaxScaler

### DATA CHOICE ###

def addFilter(gui,guybrush,feature,filtertype,filtervalue):
    gui.listWidget_Filter2.clear()
    guybrush.mst_dict.clear()
    def addtoList(i,j,source):
        gui.listWidget_Filter2.insertItem(i*len(guybrush.sources[i])+j, "Source " + str(i+1) + ": Dataset " + str(j+1))
        guybrush.mst_dict["Source " + str(i+1) + ": Dataset " + str(j+1)] = source
        #gui.listWidget_testingdata.insertItem(i*len(guybrush.sources[i])+j, "Source " + str(i+1) + ": Dataset " + str(j+1))
    #def addtoList_none(i,j):
    #    gui.listWidget_trainingdata.insertItem(i*len(guybrush.sources[i])+j, "Source " + str(i+1) + ": Dataset " + str(j+1))

    dataset = numpy.asarray(guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()])
    labels = guybrush.getLabels()

    for i in range(len(guybrush.sources)):
        for j in range(len(guybrush.sources[i])):
            data = guybrush.sources[i][j][labels[feature]]
            if(filtertype == 0):
                if(max(data) < filtervalue):
                    addtoList(i,j,guybrush.sources[i][j])
                # =
            elif(filtertype == 1):
                if(max(data) < filtervalue):
                    addtoList(i,j,guybrush.sources[i][j])
                # <
            elif(filtertype == 2):
                if(min(data) > filtervalue):
                    addtoList(i,j,guybrush.sources[i][j])
                # >
            elif(filtertype == 3):
                if(max(data) <= filtervalue):
                    addtoList(i,j,guybrush.sources[i][j])
                # <=
            elif(filtertype == 4):
                if(min(data) >= filtervalue):
                    addtoList(i,j,guybrush.sources[i][j])

    print(len(guybrush.mst_dict.values()))

### DATA SPLIT ###

def splitAdder(gui,guybrush,split):
    # random permutation
    if(gui.checkBox_MixSplit.isChecked()):
        temp = list(guybrush.mst_dict.items())
        shuffle(temp)
        guybrush.mst_dict = OrderedDict(temp) #Or just stay with b

    i = 0
    for num in guybrush.mst_dict:
        i+= 1
        if (i <= split):
            gui.listWidget_trainingdata.insertItem(i, str(num)) 
            guybrush.mst_dict_train[num] = guybrush.mst_dict[num]               
        else:
            gui.listWidget_testingdata.insertItem(i-split, str(num))  
            guybrush.mst_dict_test[num] = guybrush.mst_dict[num]

    gui.label_trainingdata.setText(str(gui.listWidget_trainingdata.count()))
    gui.label_testingdata.setText(str(gui.listWidget_testingdata.count())) 

def filterSplit(gui,guybrush):
    gui.listWidget_trainingdata.clear()
    gui.listWidget_ValidData.clear()
    gui.listWidget_testingdata.clear()
    guybrush.mst_dict_train.clear()
    guybrush.mst_dict_test.clear()

    split = int((guybrush.setsize[0]/100) * len(guybrush.mst_dict))
    splitAdder(gui,guybrush,split)

def manuDataSplitDL(guybrush, gui):
    gui.listWidget_trainingdata.clear()
    gui.listWidget_ValidData.clear()
    gui.listWidget_testingdata.clear()
    guybrush.mst_dict.clear()
    guybrush.mst_dict_train.clear()
    guybrush.mst_dict_test.clear()

    sources = guybrush.sources
    for i in range(len(sources)):
        for j in range(len(sources[i])):
            guybrush.mst_dict["Source " + str(i+1) + ": Dataset " + str(j+1)] = sources[i][j] 
    split = int((guybrush.train_size/100) * len(guybrush.mst_dict.values()))
    splitAdder(gui,guybrush,split)

def addTrain(gui,guybrush):
    i = 0
    gui.listWidget_trainingdata.clear()
    guybrush.mst_dict_train.clear()
    # random permutation
    if(gui.checkBox_MixSplit.isChecked()):
        temp = list(guybrush.mst_dict.items())
        shuffle(temp)
        guybrush.mst_dict = OrderedDict(temp) #Or just stay with b
    for num in guybrush.mst_dict:
        i+= 1
        gui.listWidget_trainingdata.insertItem(i, str(num)) 
        guybrush.mst_dict_train[num] = guybrush.mst_dict[num] 

def addTest(gui,guybrush):
    i = 0
    gui.listWidget_testingdata.clear()
    guybrush.mst_dict_test.clear()
    # random permutation
    if(gui.checkBox_MixSplit.isChecked()):
        temp = list(guybrush.mst_dict.items())
        shuffle(temp)
        guybrush.mst_dict = OrderedDict(temp) #Or just stay with b
    for num in guybrush.mst_dict:
        i+= 1
        gui.listWidget_testingdata.insertItem(i, str(num)) 
        guybrush.mst_dict_test[num] = guybrush.mst_dict[num] 

### SLIDED WINDOW ###
def DLWindow(gui, guybrush):
    def create_Window(keys, labels_in, labels_out, look_back):
        dataset = guybrush.mst_dict_train[keys]
        data_in = numpy.asarray(dataset[labels_in])
        data_out = numpy.asarray(dataset[labels_out])
        
        dataX = list()
        dataY = list()
        row = list()

        for i in range(len(data_in)-look_back-1):
            for j in range(look_back):                
                for k in range(len(labels_in)):
                    row.append(data_in[i+j][k])
            #row = guybrush.scaler.fit_transform(row)
            #out = guybrush.scaler.fit_transform(data_out[i])
            dataX.append(row)
            dataY.append(data_out[i])            
            
            print(row)
            print(data_out[i])
            row = []
        
        guybrush.mst_file_DL.append([dataX,dataY])

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
    
    guybrush.scaler = MinMaxScaler(feature_range=(0, 1))
    look_back = guybrush.window_size
    labels_in = list()
    for i in range(len(guybrush.inputList)):
        labels_in.append(guybrush.mst_labels[guybrush.inputList[i]])
    labels_out = list()
    for i in range(len(guybrush.outputList)):
        labels_out.append(guybrush.mst_labels[guybrush.outputList[i]])

    for keys in guybrush.mst_dict_train:
        create_Window(keys,labels_in,labels_out,look_back)


    '''






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
    '''
    
