'''
Created on Mar 9, 2017

RNN - all about the Neural Networks

@author: Reiti
'''
import numpy as np
import pandas
from datetime import date
from PyQt5.QtGui import QPixmap

import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input
from keras.layers import LSTM, Input, Bidirectional, Embedding, RNN
from keras.layers import Dropout
from keras.layers import Concatenate, Embedding, Add, concatenate
from keras.layers import add, concatenate, merge
from keras.utils import plot_model
from keras.optimizers import Adagrad
from keras.callbacks import TensorBoard

from sklearn.preprocessing import MinMaxScaler

def RNNBuild(guybrush):
    print("Vanilla RNN")

def BLSTMBuild(guybrush):
    print("BLSTM")

def LSTMInit(guybrush,gui):

    def getKerasLayer(former_layer,name_layer):
        if (name_layer == "LSTM"):
            layer = LSTM(1)(former_layer)
        elif (name_layer == "Dense"):
            layer = Dense(mst_dense, )(former_layer)
        elif (name_layer == "Dropout"):
            layer = Dropout(mst_dropout)(former_layer)
        elif (name_layer == "Flatten"):
            branch.add(Dropout(mst_flatten))        
        return layer

    net_filename = 'results/model_' + str(date.today()) + '_lstm.png'
    guybrush.model_name = net_filename

    #########################
    ### RNN Konfiguration ###
    #########################

    num_inputs = len(gui.listInput.selectedIndexes())
    #look_back = guybrush.window_size
    look_back = 5
    mst_optimizer = gui.comboOpti.currentText()
    mst_batch = int(gui.lineEdit_Batch.text()) #samples pro Gradientenupdate
    mst_verbose = 2 # 0 - silent, 1 - Fortschrittsbalken, 2 - Zeile
    mst_dropout = float(gui.lineEdit_dropout.text()) # Dropout-Rate
    mst_layer = int(gui.lineEdit_layer.text())
    mst_dense = int(gui.lineEdit_dense.text())
    mst_merge = gui.comboBox_Merge.currentText()
    mst_loss = gui.comboBox_Loss.currentText()
    n_epochs = int(gui.lineEdit_nepochs.text())
   
    #### Build Network Structure ####
    inputs = []
    branches = []
    lstm = []
    merge_layer = []
    branch_layer = []

    items_branches = gui.listWidget_Branches.count()
    items_merge = gui.listWidget_Merge.count()

    for j in range(items_branches):
        branch_layer.append([])
        for i in range(num_inputs):
            if(j == 0):      
                branch_layer[j].append(Input(shape=(None, look_back))) 
            else:
                branch_layer[j].append(getKerasLayer(branch_layer[j-1][i], str(gui.listWidget_Branches.item(j).text())))     

    merge = Concatenate(axis=-1)(branch_layer[len(branch_layer)-1])
    
    for i in range(items_merge):
        if(i == 0):
            merge_layer.append(getKerasLayer(merge, str(gui.listWidget_Merge.item(i).text())))
        else:
            merge_layer.append(getKerasLayer(merge_layer[i-1], str(gui.listWidget_Merge.item(i).text())))

    model = Model(inputs=branch_layer[0],outputs=merge_layer[len(merge_layer)-1])

    plot_model(model,to_file=guybrush.model_name,show_shapes=True) #,show_shapes=True
    pixmap = QPixmap(net_filename)
    gui.label_Network.setPixmap(pixmap)
   
    #tensorboard = TensorBoard(log_dir='./logs', histogram_freq=1, batch_size=32, write_graph=True, write_grads=True, write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
    
    ### Learning ###############################################
    model.compile(loss=mst_loss, optimizer=mst_optimizer, metrics=['accuracy', 'mae'])

    return model


def LSTMBuild(guybrush, gui):

    def predictSequence(dataX, dataY):
        predSeq = []
        dataPredict = []
        for i in range(len(guybrush.getInputDL())):
            predSeq.append([])       
        for i in range(look_back):
            for j in range(len(predSeq)):
                predSeq[j].append(dataX[j][0][0][i])
        for i in range(len(predSeq)):
            predSeq[i] = np.array([[predSeq[i]]])
        for i in range(1,len(dataY)):
            predict = model.predict(predSeq)
            for j in range(1,look_back):
                for k in range(len(predSeq)):
                    predSeq[k][0][0][j-1] = predSeq[k][0][0][j]
            predSeq[2][0][0][look_back-1] = predict[0]

            #for p in range(1,len(predSeq)):
            #    predSeq[p][0][0][j-1] = dataX[p][0][0]
            dataPredict.append(predict)    
        predict = model.predict(predSeq)
        dataPredict.append(predict)
        dataPredict = np.asarray(dataPredict)
        dataPredict = dataPredict.reshape((len(dataPredict),1))
        return dataPredict

    model = guybrush.model
    datasetDL = guybrush.mst_file_DL

    num_inputs = len(gui.listInput.selectedIndexes())
    look_back = guybrush.window_size
    mst_optimizer = gui.comboOpti.currentText()
    mst_batch = int(gui.lineEdit_Batch.text()) #samples pro Gradientenupdate
    mst_loss = gui.comboBox_Loss.currentText()
    n_epochs = int(gui.lineEdit_nepochs.text())    
    mst_verbose = 2 # 0 - silent, 1 - Fortschrittsbalken, 2 - Zeile
   
    for i in range(len(datasetDL)): # wieviele Simulationsdurchgänge zum Training
        trainX = np.asarray(datasetDL[i][0])
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        trainY = datasetDL[i][1]

        print(trainX[0])
        print(trainY) 

        for k in range(n_epochs):
            #model.fit(trainX, trainY, epochs=1, verbose=mst_verbose, batch_size=mst_batch)         
            gui.progressBarRNN.setValue(int((k/n_epochs) * 100) + 1)
            #gui.progressBarRNN_2.setValue(int(((i)/len(datasetDL[0])) * 100) + ((k/n_epochs)) * (int(((i)/len(datasetDL[0])) * 100))        )
        gui.progressBarRNN_2.setValue(int(((i+1)/len(datasetDL[0])) * 100) + 1)
    gui.progressBarRNN.setValue(100)
    gui.progressBarRNN_2.setValue(100)






    #scaler = []
    #for i in range(5):
    #    scaler.append(MinMaxScaler(feature_range=(-1, 1))) #Normalisierer)

    # Standardisierung der Daten ###############################################

    #datasetDL[0][0][0] = scaler[0].fit_transform(datasetDL[0][0][0]) # Indikator 1
    #datasetDL[0][0][1] = scaler[1].fit_transform(datasetDL[0][0][1]) # Indikator 2
    #datasetDL[0][0][2] = scaler[2].fit_transform(datasetDL[0][0][2]) # Indikator 3
    #datasetDL[0][0][3] = scaler[3].fit_transform(datasetDL[0][0][3]) # Indikator 4
    #datasetDL[1][0][3] = scaler[4].fit_transform(datasetDL[1][0][3]) # Y # Indikator 4

    '''
    datasetDL[0] trainX
    datasetDL[1] trainY
    datasetDL[2] testX
    datasetDL[3] testY
    '''
    #if(gui.checkTensorboard.isChecked()):
    #    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=1, batch_size=32, write_graph=True, write_grads=True, write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)

    # Training ####
    '''
    trainXset = []
    for i in range(len(datasetDL[0])): # wieviele Simulationsdurchgänge zum Training
        for j in range(len(guybrush.inputList)): # 
            trainXset.append(datasetDL[0][i][guybrush.outputList[j]])
            trainXset[j] = np.reshape(trainXset[j], (trainXset[j].shape[0], 1, trainXset[j].shape[1]))
            trainY = datasetDL[1][i][3] # die 3 ist hier immer 1-SL - muss noch weg!
        for k in range(n_epochs):
            model.fit(trainXset, trainY, epochs=1, verbose=mst_verbose, batch_size=mst_batch)         
            gui.progressBarRNN.setValue(int((k/n_epochs) * 100) + 1)
            #gui.progressBarRNN_2.setValue(int(((i)/len(datasetDL[0])) * 100) + ((k/n_epochs)) * (int(((i)/len(datasetDL[0])) * 100))        )
        trainXset = []
        gui.progressBarRNN_2.setValue(int(((i+1)/len(datasetDL[0])) * 100) + 1)
    gui.progressBarRNN.setValue(100)
    gui.progressBarRNN_2.setValue(100)

    # Testing ####
    testXset = []
    for i in range(len(datasetDL[2])): # Simultationsdurchgänge für tests
        for j in range(len(guybrush.getInputDL())): # 
            testXset.append(datasetDL[2][i][guybrush.getInputDL()[j]])
            testXset[j] = np.reshape(testXset[j], (testXset[j].shape[0], 1, testXset[j].shape[1]))
            testY = datasetDL[3][i][3] # die 3 ist hier immer 1-SL - muss noch weg!
        #predict -----
        dataPredict = predictSequence(testXset, testY)
        testscore = model.evaluate(testXset,testY,verbose=0,batch_size=mst_batch)
        testXset = []


    
    #scaler = guybrush.getScaler()
    #dataPredict = scaler[len(scaler)-1].inverse_transform(dataPredict)
    #testY = scaler[len(scaler)-1].inverse_transform(testY)
    '''

    # --- LSTM Prediction -------------------------------
    '''
    predSeq = []
    predSeq2 = []
    predSeq3 = []
    trainPredict = []

    for i in range(look_back):
        predSeq.append(trainX[0][0][i])
        predSeq2.append(trainX1[0][0][i])
        predSeq3.append(trainX2[0][0][i])
    predSeq = np.array([[predSeq]])
    predSeq2 = np.array([[predSeq2]])
    predSeq3 = np.array([[predSeq3]])

    for i in range(1,len(trainY)):
        predict = model.predict([predSeq,predSeq2,predSeq3])
        #predict = model.predict(predSeq)
        for j in range(1,look_back):
            predSeq[0][0][j-1] = predSeq[0][0][j]
            predSeq2[0][0][j-1] = predSeq2[0][0][j]
            predSeq3[0][0][j-1] = predSeq3[0][0][j]
        predSeq[0][0][look_back-1] = predict[0]
        predSeq2[0][0][look_back-1] = trainX1[i][0][0]
        predSeq3[0][0][look_back-1] = trainX2[i][0][0]
        print(predict, " zu ", trainY[i])
        trainPredict.append(predict)    
    predict = model.predict([predSeq,predSeq2,predSeq3])
    #predict = model.predict(predSeq)
    trainPredict.append(predict)
    trainPredict = np.asarray(trainPredict)
    trainPredict = trainPredict.reshape((len(trainPredict),1))
    '''
    #return dataPredict,testY