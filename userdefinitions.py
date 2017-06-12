'''
Created on Mar 9, 2017

@author: Reiti
'''
#Path to inputfile
path = ''
num_devices = 0
num_data = 0
name_devices =''


class parameters():
    def __init__(self):
        print("Parameters initialized") 
        
    def getFile(self):
        return path       
    
    def getNumDevices(self):
        return num_devices

    def getNumData(self):
        return num_data
    
    def getNameDevices(self):
        return name_devices
    
    def setFile(self, filename):
        global path
        path = filename
        
    def setNumDevices(self, num):
        global num_devices
        num_devices = num

    def setNumData(self, num):
        global num_data
        num_data = num
        
    def setNameDevices(self, line):
        global name_devices
        name_devices = line