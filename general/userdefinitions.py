'''
Created on Mar 9, 2017

Parameters and common used datasets

@author: Reiti
'''
#Path to inputfile
path = ''

#default values
num_devices = 0
num_data = 0
name_devices =''
modelname = ''
optimizer = 'SGD'
train_size = 67
test_size = 33
tensorboard = False

from keras.models import Sequential, Model

class parameters():
    def __init__(self):
        global datasetRaw
        global sources
        global dataset #raw loaded data
        global mst_file #new raw loaded data
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
        global num_devices

        print("Parameters initialized...")

    ##############
    ### GETTER ###
    ##############

    def getFile(self):
        return path

    def getNumDevices(self):
        return num_devices

    def getNumData(self):
        return num_data

    def getNameDevices(self):
        return name_devices

    def getModelName(self):
        return modelname

    def getOptimizer(self):
        return optimizer

    def getSetSizes(self):
        return [train_size, test_size]

    def getSimReps(self):
        return n_simrepeats

    def getDelimiter(self):
        return delimiter

    def getModel(self):
        return model

    def getScaler(self):
        return scaler

    ##############
    ### SETTER ###
    ##############

    def setModelName(self, name):
        modelname = name

    def setFile(self, filename):
        global path
        path = filename

    def setDelimiter(self, delim):
        global delimiter
        delimiter = delim

    def setNumDevices(self, num):
        num_devices = num

    def setNumData(self, num):
        global num_data
        num_data = num

    def setNameDevices(self, line):
        global name_devices
        name_devices = line

    def setOptimizer(self, optimizer_name):
        optimizer = optimizer_name

    def setSetSizes(self, train):
        global train_size, test_size
        train_size = train
        test_size = 100-train_size
    
    def setSimReps(self, n):
        global n_simrepeats
        n_simrepeats = n

    def setModel(self, m):
        global model
        model = m

    def setScaler(self, s):
        global scaler
        scaler = s
