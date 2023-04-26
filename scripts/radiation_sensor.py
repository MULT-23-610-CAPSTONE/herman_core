#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String


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
        # os.system('sudo udevadm control --reload-rules')
        # os.system('sudo udevadm trigger')
        # os.system('python pyKromek_lib.py')
        os.system('python /home/nano/radition_ws/src/herman_core/scripts/pyKromek_lib.py')

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
        
      
def convertToString(channels, counts):
    out = ''
    for i, channel in enumerate(channels):
        out += str(channel) + '#' + str(counts[i]) + '%'
    return(out)

def readSensor():
    pub = rospy.Publisher('radiation_sensor', String, queue_size=10)
    rospy.init_node('readSensor', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # Run detector
        runDetect()

        # The following line runs the data aquisition functions from the sorted data
        channels, counts = readFile('sorted.txt')

        data = convertToString(channels, counts)
        
        # rospy.loginfo(data)

        pub.publish(data)
        rate.sleep()

if __name__ == '__main__':
    try:
        readSensor()
    except rospy.ROSInterruptException:
        pass