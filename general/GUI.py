'''
Created on Mar 9, 2017

@author: Reiti

'''
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QImage
import sys
from general import guyBrush
from output import tableSet, murray2D, murray3D
from input import slidedWindow

qtCreatorFile = "MainGUI.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Fenster(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #print(os.path.realpath(__file__))
        global guybrush              
        guybrush = guyBrush.guyBrush()
        
        #NEURO
        self.initneuroButton.clicked.connect(self.neuroInit)
        self.abortneuroButton.clicked.connect(self.abortInit)
        
        #DATAINPUT
        self.loadFileButton.clicked.connect(self.openFileDialog)        
        self.actionExit.triggered.connect(self.slotClose)
        self.prePlotButton.clicked.connect(self.prePlot)
        self.ButtonPrepData.clicked.connect(self.prepData)
        self.ButtonSlidedWindow.clicked.connect(self.slidedWindow)
            
    #---- Neuro Parameters ----    
    def neuroInit(self):
        #init neural network
        guybrush.initLSTM()
        
    #---- Neuro Parameters ----    
    def abortInit(self):
        #init neural network
        self.close()
        
    #---- Data Input -----
    def openFileDialog(self):
        global filename        
        filter = "csv-Files (*.csv)"
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home/reiti/Nextcloud/PhD/workspace/guybrushThreepwood/database", filter)[0]
        #filename = os.path.basename(str(filename))
        self.lineFile.setText(filename)
        self.pushOK.clicked.connect(self.setDataTable)
        
    def setDataTable(self):
        #lambda: guybrush.start_new_thread(threadDatabase,(filename,))
        print ("-> Start reading " + filename)
        guybrush.initDatabase(filename)
        tableSet.tableInit(self, guybrush)
        labels = guybrush.getLabels()
        for i in range(0, len(labels)):
            self.listInput.insertItem(i, labels[i])
            self.listOutput.insertItem(i, labels[i])  
        print ("<- Finished reading ")  
        self.checkLoaded.setChecked(True)
       
        
    def prePlot(self):
        print("-> Start pre-plotting " + filename)
        murray2D.prePlotting2D(self, guybrush)  
        #murray3D.prePlotting3D(self, guybrush)
        self.checkPrePlot.setChecked(True)
        print("<- Finished pre-plotting")
        
    def prepData(self):
        print("-> Start Dataset Limitation for DL")
        guybrush.setTrainSize(self.lineEdit_Train.text())
        print("Train: ", int((int(self.lineEdit_Train.text())/100) * guybrush.getNumData()))
        print("<- Finished Dataset Limitation for DL")
        
    def slidedWindow(self):
        print("-> Start Data Prep for DL ")
        guybrush.setWindowSizeDL(self.lineWindowSize.text())  
        #Get selected Items from Lists
        selIn = self.listInput.selectedIndexes()
        selOut = self.listOutput.selectedIndexes()
        input = []
        output = []
        for i in range(0,len(selIn)):
            input.append(selIn[i].row())
        for i in range(0,len(selOut)):
            output.append(selOut[i].row())              
        guybrush.setInputDL(input)
        guybrush.setOutputDL(output)
        guybrush.initDatabaseDL(self)
        #oImage = QImage("/home/reiti/Nextcloud/PhD/workspace/guybrushThreepwood/general/backgound.png")
        #self.tabWidget_Net.insertTab(0, oImage)
        print("<- Finished Data Prep for DL")
       
    def slotClose(self):
        self.close() 

def openWindow():
    app = QtWidgets.QApplication(sys.argv)
    window = Fenster()
    window.show()    
    sys.exit(app.exec_())  
    
#entry point
openWindow()
