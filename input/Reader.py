'''
Created on Mar 9, 2017

returns Datasets Structures

@author: Reiti
'''
import numpy as np
import csv
from datetime import datetime
import pandas
from sklearn.preprocessing import MinMaxScaler

num_devices = 0
num_data = 0

class Reader():
    def __init__(self, defs):
        file = open(defs.getFile(), 'r')
        global num_devices, num_data
        line = file.readline()
        defs.setNameDevices(line)
        defs.setNumDevices(len(line.split()))
        defs.setNumData(sum(1 for line in open(defs.getFile())))

def getNumDevices():
    return num_devices

def getNumData():
    return num_data

def readFile(gui, guybrush):
    delimiter = guybrush.delimiter
    filename = str(guybrush.file)
    n_simrepeats = guybrush.n_simrepeats

    if(gui.checkBoxComplDS.isChecked()):
        data = pandas.read_csv(filename)
    else:
        data = pandas.read_csv(filename)[0:n_simrepeats*delimiter]
    labels = list(data)

    data_new = []
    for i in range(n_simrepeats):
        data_new.append(data[i*delimiter:delimiter+i*delimiter])

    return data,data_new,labels

def readDatabase(gui, guybrush):
    global num_devices, num_data

    def MST_Reader():
        labels = ["k","P","$\Delta P$","1-$f_{sl}$"]
        max_len = 100000
        with open(guybrush.getFile()) as f:
            reader = csv.reader(f, delimiter="\t")
            for i in range((5+5*(n_simrepeats-1))):
                line = next(reader)                
                if (i%5) != 0 and i != 0:
                    line_new = []
                    if max_len > len(line):
                        max_len = len(line)
                    for j in range(1,max_len):
                        line_new.append(line[j])
                        data[int(i/5)][(i-1)-(int(i/5)*5)][j-1] = float(line[j])
        return data,labels

    filename = str(guybrush.mst_file)
    n_simrepeats = guybrush.n_simrepeats

    if filename.endswith('.dat'):
        # MST Files
        
        guybrush.setNumData(2000) # !!!!!! wegen max len
        guybrush.setNumDevices(4)
        #data = np.zeros((n_simrepeats,defs.getNumDevices(),defs.getNumData()))
        data = np.zeros((n_simrepeats,guybrush.getNumDevices(),guybrush.getNumData()))
        #data = np.empty((defs.getNumData(),defs.getNumDevices()))
        data,labels = MST_Reader()
        
    elif filename.endswith('.csv'):
        # Flight Stats, DDR2 
        #labels = np.genfromtxt(str(defs.getFile()), delimiter=',', dtype=str, max_rows=1)

        dateparse = lambda dates: pandas.datetime.strptime(dates, '%Y-%m-%d')
        dataset = pandas.read_csv(guybrush.mst_file, parse_dates=['Datum'], index_col='Datum',date_parser=dateparse)
        dataset.index

        data = []

        for i in range(n_simrepeats):
            data.append(dataset[i*guybrush.delimiter:i*guybrush.delimiter+guybrush.delimiter])




        '''
        for i in range(1, n_simrepeats * 35, 35):
            data.append([])

        for i in range(len(data)):
            for j in range(len(dataset.columns)):
                data[i].append([])

        if( "Flights" in guybrush.getFile()):
            # Flight related ATMAP                       
            k_old = 0 
            for i in range(len(data)):
                k = 0
                last = 0 
                while(last <= int(dataset.iloc[k+k_old,5])):
                    last = int(dataset.iloc[k+k_old,5])
                    for j in range(len(data[i])):
                        data[i][j].append([])
                        data[i][j][k] = dataset.iloc[k_old + k,j]
                    k+=1
                k_old += k + 1

        else:
            for i in range(len(data)):
                for j in range(len(data[i])):
                    # ATMAP related Flights
                    for k in range(35):
                        data[i][j].append([])
                        data[i][j][k] = dataset.iloc[k + i * 35,j]

               
        k_old = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if( "Flights" in defs.getFile()):
                    # Flight related ATMAP
                    k = 0
                    last = 0   
                    while(last <= int(dataset.iloc[k+k_old,5])):
                        last = int(dataset.iloc[k+k_old,5])
                        data[i][j].append([])
                        data[i][j][k] = dataset.iloc[k_old + k,j]
                        k+=1
                    k_old += k

                else:
                    # ATMAP related Flights
                    for k in range(35):
                        data[i][j].append([])
                        data[i][j][k] = dataset.iloc[k + i * 35,j]
        '''
                
        #guybrush.num_data = 35 
        devices = (len(dataset.columns))
        #guybrush.mst_labels = list(dataset.columns.values)
        #guybrush.sources.append(data)

        labels = dataset.columns.values
    
    return data, labels, devices

