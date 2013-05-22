#!/usr/bin/python
#Author: Jackie Jin
#This python controller is based on Mr.Andreas Klostermann's interface
#with PyEEG and Pygame
#This is the project link:https://github.com/akloster/python-mindwave
#License: MIT

from numpy import *
import scipy
from pyeeg import bin_power
from parser import Parser
import rospy
import sys
import roslib; roslib.load_manifest('EEGControlMsgs')
from EEGControlMsgs.msgs import *

class Mindwave():
    def __init__(self):
        rospy.init_node('MindwaveControl')
        rospy.loginfo("Initializing Control")
        self.eegParser = Parser()
        self.controlPublisher = rospy.Publisher('eeg/control', MindwaveControl)
        self.controlOutput = MindwaveControl()
        self.outputMap = {
            'attention':0,
            'meditation':0
            }
        
    def control(self):
        pass

    def publish(self):
        self.controlOutput.attention = outputMap['attention']
        self.controlOutput.meditation = outputMap['meditation']
        self.controlPublisher.publish(self.controlOutput)

if __name__ == '__main__':
    try:
        control = Mindwave()
        control.control()
    except rospy.ROSInterruptException:
        pass
