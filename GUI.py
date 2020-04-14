'''
            .;ldkO0000Okdl;.                 reiti@linux-nfkh
         .;d00xl:^''''''^:ok00d;.            OS: openSUSE 42.3
       .d00l'                'o00d.          Kernel: x86_64 Linux 4.4.87-25-default
     .d0Kd'  Okxol:;,.          :O0d.        Uptime: 2d 5h 54m
    .OKKKK0kOKKKKKKKKKKOxo:,      lKO.       Packages: 5259
   ,0KKKKKKKKKKKKKKKK0P^,,,^dx:    ;00,      Shell: zsh 5.0.5
  .OKKKKKKKKKKKKKKKKk'.oOPPb.'0k.   cKO.     Resolution: 1920x1080
  :KKKKKKKKKKKKKKKKK: kKx..dd lKd   'OK:     DE: KDE 5.32.0 / Plasma 5.8.7
  dKKKKKKKKKKKOx0KKKd ^0KKKO' kKKc   dKd     WM: KWin
  dKKKKKKKKKKKK;.;oOKx,..^..;kKKK0.  dKd     WM Theme: Breeze Dark
  :KKKKKKKKKKKK0o;...^cdxxOK0O/^^'  .0K:     GTK Theme: Breeze-Dark [GTK2/3]
   kKKKKKKKKKKKKKKK0x;,,......,;od  lKk      Icon Theme: breeze-dark
   '0KKKKKKKKKKKKKKKKKKKKK00KKOo^  c00'      Font: Noto Sans Regular
    'kKKKOxddxkOO00000Okxoc;''   .dKk'       CPU: Intel Core i7-5600U CPU @ 4x3.2GHz
      l0Ko.                    .c00l'        RAM: 4749MiB / 15920MiB
       'l0Kk:.              .;xK0l'
          'lkK0xl:;,,,,;:ldO0kl'
              '^:ldxkkkkxdl:^'

'''

from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
from general import guyBrush
from output import dataView, murray2D, murray3D, radarPlot
from input import MLData, Reader
from statistics import TSStat, descrStats, featureEngineering, clusterClass
from matplotlib import rcParams

__author__ = 'Reiti Reitmann'

# Default Plot Font
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12

qtCreatorFile = "MainGUI_Layout.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass

class Fenster(QtWidgets.QMainWindow, Ui_MainWindow):
    def welcome(self):
        longstring = """\
         ____
        Welcome to Guybrush Threepwood - the Artificial Data Tool!
        WIP since Mar 9, 2017
        v0.311
        @author: Reiti
        ----
                \   ^__^
                 \  (oo)\_______
                     (__) \             )\/
                            ||--------w |
                            ||           ||        
        """
        print(longstring)
            
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.showFullScreen()

        #Console Output
        self.textEdit_Console.setStyleSheet("color: rgb(26, 255, 128);")
        sys.stdout = Stream(newText=self.onUpdateText)
        self.welcome()    

        # --- Guybrush + Parameter Init ---
        global guybrush
        guybrush = guyBrush.guyBrush()
		

        ###############
        ### Buttons ###
        ###############
        self.actionAbout.triggered.connect(self.aboutMessageBox)
        self.actionExit_2.triggered.connect(self.close)
        # --- NEURO ---
        self.initneuroButton.clicked.connect(self.neuroInit)
        self.trainneuroButton.clicked.connect(self.trainInit)
        self.comboOpti.currentIndexChanged.connect(self.optimizerSet)
        self.dialDataset.valueChanged.connect(self.adjustSetSize)
        # --- DATAINPUT ---
        self.loadFileButton.clicked.connect(self.openFileDialog)
        self.actionExit.triggered.connect(self.slotClose)
        self.prePlotButton.clicked.connect(self.prePlot)        
        self.ButtonSlidedWindow.clicked.connect(self.slidedWindow) 
        self.checkBox_ValidData.clicked.connect(self.setValidData)
        self.checkBoxComplDS.clicked.connect(self.setCompleteDataset)
        self.ButtonSimpleCluster.clicked.connect(self.setSimpleCluster) 
        self.comboBox_Source2.currentIndexChanged.connect(self.adjustDataBox)
        self.comboBox_Source.currentIndexChanged.connect(self.adjustDataBox2)
        # --- DATASPLIT ---
        self.pushButton_AddFilter.clicked.connect(self.addFilter)
        self.pushButton_Filter.clicked.connect(self.filterSplit)
        self.pushButton_ManualSplit.clicked.connect(self.manuSplit)
        self.pushButton_Pareto.clicked.connect(self.pareto)
        self.pushButton_addTrain.clicked.connect(self.addTrain)
        self.pushButton_addTest.clicked.connect(self.addTest)
        self.pushButton_addValid.clicked.connect(self.addValid)
        # --- FEATURES ---
        self.pushButton_kBest.clicked.connect(self.kBest)
        self.ButtonkMean.clicked.connect(self.kMean)
        self.ButtonSVM.clicked.connect(self.SVM)
        self.pushButton_ExtraTree.clicked.connect(self.extraTreeClass)
        # --- STATISTICS ---
        self.descrButton.clicked.connect(self.descriptiveStats)
        self.ButtonGrandTour.clicked.connect(self.GrandTour)  
        self.ButtonMovAv.clicked.connect(self.MovAv)
        self.ButtonDickeyFuller.clicked.connect(self.Dickey)
        self.ButtonACF.clicked.connect(self.ACF)
        self.ButtonDecomp.clicked.connect(self.Decomp)
        self.ButtonCorrmatrix.clicked.connect(self.CorrMatrix)
        #0self.listInput_Dickey.itemClicked.connect(self.setStatFocus)
        self.pushOK.clicked.connect(self.setDataViews)
    
    def onUpdateText(self, text):
        cursor = self.textEdit_Console.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_Console.setTextCursor(cursor)
        self.textEdit_Console.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__

    #################
    ### Interface ###
    #################
    def aboutMessageBox(self):
        QtWidgets.QMessageBox.about(self, "My name is Guybrush Threepwood!", 
        "Guybrush Ulysses Threepwood is the main protagonist of the Monkey <p> Island series of computer adventure games by LucasArts. Guybrush <p> is voiced by actor Dominic Armato in the third, fourth and fifth <p> games, as well as the enhanced remakes of The Secret of Monkey <p> Island and Monkey Island 2: LeChuck's Revenge. Though a mighty pirate <p> by his own account, it is a running joke throughout the games for <p> characters to garble Guybrush Threepwood's unusual name, either <p> deliberately or accidentally.")

    ###########
    ### ANN ###
    ###########
    def neuroInit(self):
        print ("-> Init Neural Network, Start Training")
        #init neural network
        #testPredict,testY = guybrush.initRNN(self.comboRNN_2.currentText(), self.checkTensorboard.isChecked(),self)
        #murray2D.plotPredict(guybrush,self,testPredict,testY)
        
        guybrush.buildRNN(self.comboRNN_2.currentText(), self.checkTensorboard.isChecked(),self)
        self.trainneuroButton.setEnabled(True)
        print ("<- Finished Neural Network Training and Testing")

    def trainInit(self):
        print ("-> Init Neural Network")
        #init neural network
        #testPredict,testY = guybrush.initRNN(self.comboRNN_2.currentText(), self.checkTensorboard.isChecked(),self)
        guybrush.initRNN(self.comboRNN_2.currentText(), self.checkTensorboard.isChecked(),self)
        
        #for i in range(len(testPredict)):
        #    print(testPredict[i])
        #murray2D.plotPredict(guybrush,self,testPredict,testY)
        print ("<- Finished Neural Network")
        #abort neural network
        #self.close()

    def optimizerSet(self):
        guybrush.setOptimizer(str(self.comboOpti.currentText()))

    def adjustSetSize(self):
        #guybrush.setTrainSize(self.dialDataset.value())
        guybrush.setsize[0] = self.dialDataset.value()
        guybrush.setsize[2] = 100 - guybrush.setsize[0]
        if(self.checkBox_ValidData.isChecked()):
            # with valid data
            self.lineEdit_Train.setText(str(guybrush.setsize[0]))
            self.lineEdit_Test.setText(str(int(0.7 * guybrush.setsize[2])))
            self.lineEdit_Valid.setText(str(int(0.3 * guybrush.setsize[1])))

        else:
            # no valid data
            self.lineEdit_Train.setText(str(guybrush.setsize[0]))
            self.lineEdit_Test.setText(str(guybrush.setsize[2]))

    ############
    ### Data ###
    ############

    def openFileDialog(self):
        # Auswahl der Datei ############################################
        #global filename
        filter = "csv-Files (*.csv);;dat-files(*.dat)"
        guybrush.mst_file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "../../Modell/FlightStatsHAM", filter)[0]
        self.lineFile.setText(guybrush.mst_file)        

    def setDataViews(self):
        # Datenanzeige in GUI ############################################
        print ("-> Start reading " + guybrush.mst_file)
        self.prePlotButton.setEnabled(True)
        self.descrButton.setEnabled(True)
        self.exportStatsButton.setEnabled(True)
        self.tabDataPre.setEnabled(True)
        self.tabDataML.setEnabled(True)
        self.tabANN.setEnabled(True)
        self.tabOthers.setEnabled(True)
        self.initneuroButton.setEnabled(True)
        
        guybrush.n_simrepeats = ((int(self.lineEdit_simrepeats.text())))
        # LOAD FILE
        guybrush.initDatabase(self, guybrush.mst_file)
        #Reader.readDatabase(self, guybrush)
        dataView.tableInit(self, guybrush)
        #dataView.treeInit(self, guybrush)
        dataView.treeBuild(self, guybrush)
        #labels = guybrush.mst_labels
        # Update Source Fields
        self.listWidgetSources.clear()
        for j in range(0, len(guybrush.sources)):
            self.listWidgetSources.insertItem(j, "Source " + str(j+1))
        self.listWidget_Filter.clear()
        self.listWidget_Filter2.clear()
        for j in range(len(guybrush.sources)):
            for i in range(len(guybrush.sources[j])):
                self.listWidget_Filter.insertItem(j*len(guybrush.sources[j])+i, "Source " + str(j+1) + ": Dataset " + str(i+1))
                self.listWidget_Filter2.insertItem(j*len(guybrush.sources[j])+i, "Source " + str(j+1) + ": Dataset " + str(i+1))
        
        print ("<- Finished reading ")
        self.checkLoaded.setChecked(True)

    def setValidData(self):
        self.label_ValidData.setEnabled(self.checkBox_ValidData.isChecked())
        self.lineEdit_Valid.setEnabled(self.checkBox_ValidData.isChecked())
        if(self.checkBox_ValidData.isChecked()):
            self.lineEdit_Train.setText(str(60))
            self.lineEdit_Valid.setText(str(10))
            self.lineEdit_Test.setText(str(30))
        else:
            self.lineEdit_Train.setText(str(67))
            self.lineEdit_Valid.setText(str(0))
            self.lineEdit_Test.setText(str(33))

    def setCompleteDataset(self):
        self.lineEdit_simrepeats.setEnabled(not self.checkBoxComplDS.isChecked())

    def adjustDataBox(self):
        self.comboBox_DS_2.clear()
        for i in range(int(len(guybrush.sources[self.comboBox_Source2.currentIndex()]))):
            self.comboBox_DS_2.addItem("Dataset " + str(i+1))       
    
    def adjustDataBox2(self):
        self.comboBox_DS.clear()
        for i in range(int(len(guybrush.sources[self.comboBox_Source.currentIndex()]))):
            self.comboBox_DS.addItem("Dataset " + str(i+1)) 

    ###############
    ### ML Data ###
    ############### 

    # Clustering
    def setSimpleCluster(self):
        print("-> Start simple clustering")
        guybrush.clusterData(guybrush)
        print("<- Finished simple clustering")

    def kMean(self):
        print("-> Start kMean Clustering")
        clusterClass.kMean(self, guybrush)
        print(guybrush.mst_file)
        print("<- Finished kMean Clustering")
    
    def SVM(self):
        print("-> Start SVM Classification")
        guybrush.SVMClassification(guybrush)
        print("<- Finished SVM Classification")

    # Data Choice
    def addFilter(self):
        feature = self.comboBox_SplitFeatures.currentIndex()
        filtertype = self.comboBox_FilterType.currentIndex()
        filtervalue = float(self.lineEdit_FilterValue.text())
        MLData.addFilter(self, guybrush, feature, filtertype, filtervalue)
        #self.listWidget_Filter.insertItem(1, "Filter: " + str(feature) + str(filtertype) + filtervalue)
    def filterSplit(self):
        print("-> Start filter splitting")
        MLData.filterSplit(self,guybrush)

    def addTrain(self):
        print("-> Add Filter to Train")
        MLData.addTrain(self,guybrush)

    def addTest(self):
        print("-> Add Filter to Test")
        MLData.addTest(self,guybrush)

    def addValid(self):
        print("-> Add Filter to Valid")


    # Splitting
    def manuSplit(self):
        print("-> Start Manual Dataset Splitting for DL")
        self.tabFeature.setEnabled(True)
        guybrush.train_size = (int(self.dialDataset.value()))
        MLData.manuDataSplitDL(guybrush,self)
        print("<- Finished Dataset Limitation for DL")

    def pareto(self):
        print("-> Start Pareto Dataset Splitting for DL")
        self.tabFeature.setEnabled(True)

    # Slided Window
    def slidedWindow(self):
        print("-> Start slided Window Data Prep for DL ")
        guybrush.window_size = int(self.lineWindowSize.text())
        #Get selected Items from Lists
        guybrush.inputList = [x.row() for x in self.listInput.selectedIndexes()]
        guybrush.outputList = [x.row() for x in self.listOutput.selectedIndexes()]
        #guybrush.initDatabaseDL(self)
        MLData.DLWindow(self, guybrush)
        print("<- Finished slided Window Data Prep for DL")

    ###########################
    ### Feature Engineering ###
    ###########################

    def kBest(self):
        print("-> Start kBest feature selection")
        featureEngineering.kBest(self, guybrush)
        print("<- Finished kBest feature selection")        

    def RFE(self):
        print("-> Start Recursive Feature Elimination (RFE)")
        featureEngineering.RFE(self, guybrush)
        print("<- Finished Recursive Feature Elimination (RFE)")

    def PCA_feat(self):
        print("-> Start PCA feature selection")
        featureEngineering.PCA_feature(self, guybrush)     
        print("<- Finished PCA feature selection")   

    def extraTreeClass(self):
        print("-> Start Extra Trees Classifier")
        featureEngineering.featureImportance(self, guybrush)
        print("<- Finished Extra Trees Classifier")

    ################
    ### Plotting ###
    ################

    def prePlot(self):
        print("-> Start pre-plotting " + guybrush.mst_file)
        #murray2D.prePlotting2D(self, guybrush)
        murray2D.prePlot(self, guybrush)
        #murray3D.prePlotting3D(self, guybrush)
        self.checkPrePlot.setChecked(True)
        #radarPlot.radarPlotTest(self)
        print("<- Finished pre-plotting")

    def setStatFocus(self):
        dataset = guybrush.getDataset()[:,self.listInput_Dickey.selectedIndexes()[0].row()]
        murray2D.plotFocusSelect(self,guybrush,dataset)

    def slotClose(self):
        self.close()

    ################
    ### Stats ###
    ################

    def descriptiveStats(self):
        print("-> Start Descriptive Statistics")
        descrStats.Stats(self, guybrush)
        print("<- Finished Descriptive Statistics")

    def GrandTour(self):
        print("-> Start Grand Tour for " + guybrush.mst_labels[self.listInput_GT.selectedIndexes()[0].row()] + ", " + guybrush.mst_labels[self.listInput_GT_2.selectedIndexes()[0].row()] + ", " + guybrush.mst_labels[self.listInput_GT_3.selectedIndexes()[0].row()])
        murray3D.GrandTour(self, guybrush, self.listInput_GT.selectedIndexes()[0].row(), self.listInput_GT_2.selectedIndexes()[0].row(), self.listInput_GT_3.selectedIndexes()[0].row())
        print("<- Finished Grand Tour")

    def MovAv(self):
        print("-> Start Smoothing for " + guybrush.mst_labels[self.comboBox_PI.currentIndex()])
        TSStat.test_rollingstat(self, guybrush, self.comboBox_DS.currentIndex(), int(self.lineACFWindow.text()))
        print("<- Finished Smoothing")

    def Dickey(self):
        print("-> Start Dickey Fuller Test for " + guybrush.mst_labels[self.comboBox_PI.currentIndex()])
        TSStat.test_stationarity(self, guybrush, self.comboBox_PI.currentIndex())
        print("<- Finished Dickey Fuller Test")
    
    def ACF(self):
        print("-> Start Autocorrelation Test for " + guybrush.getLabels()[self.comboBox_PI.currentIndex()])
        TSStat.test_correlation(self, guybrush, self.comboBox_PI.currentIndex(), int(self.lineACFWindow.text()))
        print("<- Finished Autocorrelation")

    def Decomp(self):
        print("-> Start Decomposition for " + guybrush.getLabels()[self.comboBox_PI.currentIndex()])
        TSStat.test_decomp(self, guybrush, self.comboBox_PI.currentIndex(), int(self.lineACFWindow.text()))
        print("<- Finished Decomposition")

    def CorrMatrix(self):
        print("-> Start Corr Matrix")
        TSStat.test_corrmatrix(self, guybrush, self.comboBox_PI.currentIndex())
        print("<- Finished Corr Matrix")

def openWindow():
    app = QtWidgets.QApplication(sys.argv)
    window = Fenster()
    window.show()
    sys.exit(app.exec_())

#entry point
openWindow()
