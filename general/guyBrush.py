'''
Created on Mar 9, 2017
@author: Reiti
'''
from general import userdefinitions
from input import Reader
from systemident import leChuck
from input import slidedWindow
from statistics import clusterClass
from keras.models import Model

class guyBrush():
    def __init__(self):
        global defs
        print("Guybrush initialized...")
        #create parameter object
        defs = userdefinitions.parameters()
        #defs.sources = []
        global mst_file #new raw loaded data
        global mst_labels
        global mst_dict
        global datasetRaw
        global sources
        global dataset #raw loaded data
        global delimiter
        global datasetDL #adjusted ML data
        global train_size
        global test_size
        global labels
        global inputList, outputList
        global window_size
        global model_name
        global optimizer
        global n_simrepeats
        global model
        global scaler    
        global num_devices, num_data
        self.sources = list()
        self.mst_dict = []

    ##############
    ### GETTER ###
    ##############

    def getFile(self):
        return defs.getFile()

    def getNumDevices(self):
        return defs.getNumDevices()

    def getNumData(self):
        return defs.getNumData()

    def getNameDevices(self):
        return defs.getNameDevices()

    def getColData(self, col):
        return defs.dataset[:][col]

    def getDataset(self):
        return defs.dataset

    def getDatasetDL(self):
        return defs.datasetDL

    def getTrainSize(self):
        return defs.train_size

    def getWindowSize(self):
        return defs.window_size

    def getLabels(self):
        return defs.labels

    def getInputDL(self):
        return defs.inputList

    def getOutputDL(self):
        return defs.outputList

    def getModelName(self):
        return defs.model_name

    def getSetSizes(self):
        return defs.getSetSizes()
        #return [defs.getTrainSize(),2]
    
    def getSimReps(self):
        return defs.n_simrepeats

    def getModel(self):
        return defs.getModel()

    def getScaler(self):
        return defs.getScaler()
    
    def getSources(self):
        return defs.sources

    ##############
    ### SETTER ###
    ##############

    def setTrainSize(self, TrainEdit):
        defs.setSetSizes(TrainEdit)

    def setWindowSizeDL(self, window_size):
        defs.window_size = int(window_size)

    def setInputDL(self, selIn):
        input=[]
        for i in range(0,len(selIn)):
            input.append(selIn[i].row())
        defs.inputList = input

    def setOutputDL(self, selOut):
        output = []
        for i in range(0,len(selOut)):
            output.append(selOut[i].row())
        defs.outputList = output

    def setModelName(self, name):
        defs.model_name = name
    
    def setOptimizer(self, optimizer_name):
        defs.setOptimizer(optimizer_name)

    def setSimReps(self, n):
        self.n_simrepeats = n

    def setNumData(self, n):
        defs.setNumData(n)

    def setNumDevices(self, n):
        defs.num_devices = n

    def setModel(self, model):
        defs.setModel(model)

    def setScaler(self, scaler):
        defs.setScaler(scaler)

    def updateDataset(self, data):
        defs.dataset = data



    ######################
    ### DATA FUNCTIONS ###
    ######################

    def initDatabase(self, gui, filename):
        #load database
        self.mst_file = filename   
        self.delimiter = 35     
        #defs.dataset = []
        #ReaderManager = input.Reader(defs)
        
        data, labels, devices = Reader.readDatabase(gui, self)
        #if(not defs.sources):
        #    defs.labels = labels
        #self.datasetRaw = self.dataset

        self.num_data = 35 
        self.num_devices = devices
        self.mst_labels = labels
        self.sources.append(data)
        self.datasetRaw = data


    def initDatabaseDL(self, gui):
        #Database Generator for DL
        defs.datasetDL = slidedWindow.DLWindow(self, gui)

    def clusterData(self, gui):
        clusterClass.simpleCluster(self, gui)
    
    def kmeanCluster(self, gui):
        clusterclass.kMean(self, gui)

    def SVMClassification(self,gui):
        clusterclass.SVM(self, gui)

    ##########################
    ### GRAPHICS FUNCTIONS ###
    ##########################

    def prePlotting2D(self, tabtest):
        tabtest.removeTab(0)
        #return comboBox_ANNOpti

    #######################
    ### MODEL FUNCTIONS ###
    #######################

    def initRNN(self, RNNtype, tb, gui):
        trainPredict,trainY = [],[]
        if RNNtype == 'LSTM':
            print("LSTM")
            trainPredict,trainY = leChuck.LSTMBuild(self,gui)
        elif RNNtype == 'Vanilla RNN':
            print("Vanilla RNN")
            #leChuck.RNNBuild(self)
        elif RNNtype == 'BLSTM':
            print("Bidirectional LSTM")
            #leChuck.BLSTMBuild(self)

        return trainPredict,trainY

    def buildRNN(self, RNNtype, tb, gui):
        if RNNtype == 'LSTM':            
            defs.setModel(leChuck.LSTMInit(self,gui))
        elif RNNtype == 'Vanilla RNN':
            print("Vanilla")
            #leChuck.RNNBuild(self)
        elif RNNtype == 'BLSTM':
            print("BLSTM")
            #leChuck.BLSTMBuild(self)
        