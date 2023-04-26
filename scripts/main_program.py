# This code is the property of Hubert E Coburn II

import os
from time import sleep
from datetime import datetime
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np
from pyKromek_lib import *
import signal
import sys 

def runDetect():
    """ The following function runs the Kromek supplied detection software and returns the input fie for the 
    Fortran program to run through"""
    try:
        os.system('sudo udevadm control --reload-rules')
        os.system('sudo udevadm trigger')
        os.system('python pyKromek_lib.py')

    except Exception:
        print('error: did not detect')
       
def readFile(filename):
    """The following program opens and reads the data from the previously created sorting data"""
    try:
        xdata = np.loadtxt(filename, usecols=[1], dtype=float)
        ydata = np.loadtxt(filename, usecols=[3], dtype=float)
        return xdata, ydata
        
    except Exception:
        print('error in file read x')
        
def plotData(x,y):
    """The following function plots the previously pulled data"""
    try:
        plt.plot(x,y,linewidth=0.5)
        plt.title('Radiation Counts', fontsize=18)
        plt.xlabel('Channel', fontsize=15)
        plt.ylabel('Counts', fontsize=15)
               
        storename  = datetime.now().time().strftime('%H%M%S%f')
        
        plt.savefig('Test_Data/'+str(storename)+'.png')
        
        plt.show(block = False)
        plt.pause(5)
        plt.close()
        
    except Exception:
        print('error in file plot')
        
def storeData(livetime,filename):
    """the following function stores the pulled data with a stamp"""
    try:
        data = np.loadtxt(filename, usecols=[1,3], dtype=float)
        np.savetxt('Background_Data/'+str(livetime)+'.txt',data,delimiter ='    ,    ')
        
    except Exception:
        print('error in file save')

def convertToString(channels, counts):
    out = ''
    for i, channel in enumerate(channels):
        out += str(channel) + '#' + str(counts[i]) + '\n'
    return(out)

#### Begin the main program here ####
# This code is the property of Hubert E Coburn II
# The following line runs the initial data aquisition function
# timeup = input('Enter live time in minutes:   ')
try:
    while True:
        # Run detector
        runDetect()

        # The following line runs the data aquisition functions from the sorted data
        channels, counts = readFile('sorted.txt')

        data = convertToString(channels, counts)
        
        print(data)

except KeyboardInterrupt:
    print('interrupted!')