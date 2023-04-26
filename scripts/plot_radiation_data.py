#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import matplotlib.pyplot as plt
import numpy as np


# def plotData(x, y):
#     """The following function plots the previously pulled data"""
#     try:
#         plt.plot(x,y,linewidth=0.5)
#         plt.title('Radiation Counts', fontsize=18)
#         plt.xlabel('Channel', fontsize=15)
#         plt.ylabel('Counts', fontsize=15)
               
#         # storename  = datetime.now().time().strftime('%H%M%S%f')
        
#         # plt.savefig('Test_Data/'+str(storename)+'.png')
        
#         plt.show(block = False)
    
#     except Exception:
#         print('error in file plot')

# def callback(data):
#     channels = []
#     counts = []    
#     measurements = data.data.split("%")
#     for i in range(0, len(measurements) - 1):
#         single_data =  measurements[i].split("#")
#         print(single_data)
#         channels.append(float(single_data[0]))
#         counts.append(float(single_data[1]))

#     # plotData(np.array(channels), np.array(counts))
#     plt.plot(np.array(channels),np.array(counts),linewidth=0.5)
    
    
# def plotter():

#     plt.title('Radiation Counts', fontsize=18)
#     plt.xlabel('Channel', fontsize=15)
#     plt.ylabel('Counts', fontsize=15)
#     plt.show()
  
#     rospy.init_node('plotter', anonymous=True)

#     rospy.Subscriber("radiation_sensor", String, callback)

#     # spin() simply keeps python from exiting until this node is stopped
#     rospy.spin()


class RadiationSensorPlotter:
    def __init__(self):
        # self.measurements = []
        self.channels = []
        self.counts = []  
        self.fig, self.ax = plt.subplots()

    def radiation_sensor_callback(self, msg):
        # Split the string into a list of measurements
        self.channels = []
        self.counts = []
        measurements = msg.data.split("%")
        for i in range(0, len(measurements) - 1):
            single_data =  measurements[i].split("#")
            # print(single_data)
            self.channels.append(float(single_data[0]))
            self.counts.append(float(single_data[1]))


        # Update the measurements and plot the new data
        self.ax.clear()
        self.ax.plot(self.channels,self.counts,linewidth=0.5)
        self.ax.set_xlabel('Channel', fontsize=15)
        self.ax.set_ylabel('Counts', fontsize=15)
        self.ax.set_title('Radiation Counts', fontsize=18)

        # Draw the plot
        self.fig.canvas.draw()

    def run(self):
        rospy.init_node('radiation_sensor_plotter')

        # Subscribe to the radiation_sensor topic
        rospy.Subscriber('radiation_sensor', String, self.radiation_sensor_callback)

        plt.show()

if __name__ == '__main__':
    node = RadiationSensorPlotter()
    node.run()