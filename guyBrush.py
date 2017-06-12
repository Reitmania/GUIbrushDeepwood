'''
Created on Mar 9, 2017

@author: Reiti
'''
from general import userdefinitions
from input import Reader
from systemident import leChuck
from input import slidedWindow

class guyBrush():
    
    def __init__(self):
        #create parameter object
        global dataset
        global datasetDL
        global train_size
        global labels
        global inputList, outputList
        global defs
        global window_size        
        defs = userdefinitions.parameters()
        
    # GETTER       
    def getNumDevices(self):
        return defs.getNumDevices()
    def getNumData(self):
        return defs.getNumData()
    
    def getNameDevices(self):
        return defs.getNameDevices()
    
    def getColData(self, col):
        return self.dataset[:][col]
    
    def getDataset(self):
        return self.dataset
    
    def getDatasetDL(self):
        return self.datasetDL
    
    def getTrainSize(self):
        return self.train_size
    
    def getWindowSize(self):
        return self.window_size
    
    def getLabels(self):
        return self.labels
    
    def getInputDL(self):
        return self.inputList
    
    def getOutputDL(self):
        return self.outputList
    
    # SETTER
    
    def setTrainSize(self, TrainEdit):
        self.train_size = float(TrainEdit)
        
    def setWindowSizeDL(self, window_size):
        self.window_size = int(window_size)
    
    def setInputDL(self, input):
        self.inputList = input
        
    def setOutputDL(self, output):
        self.outputList = output        
       
    # DATA FUNCTIONS    
    def initDatabase(self, filename):
        #load database  
        defs.setFile(filename)        
        #ReaderManager = input.Reader(defs)
        self.dataset, self.labels = Reader.readDatabase(defs) 
        
    def initDatabaseDL(self, gui):
        self.datasetDL = slidedWindow.DLWindow(self, gui)             
    
    # GRAPHICS FUNCTIONS 
    def prePlotting2D(self, tabtest):       
        tabtest.removeTab(0)
        return 1
        
    def initLSTM(self):
        leChuck.LSTMBuild(self)
        
        
        
        