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
from EEGControlMsgs.msg import *
import time

class Mindwave():
    def __init__(self):
        rospy.init_node('MindwaveControl')
        rospy.loginfo("Initializing Control")
        self.eegParser = Parser()
        self.controlPublisher = rospy.Publisher('eeg/control', MindwaveControl)
        self.controlOutput = MindwaveControl()
        self.outputMap = {
            'attention':0,
            'meditation':0,
            'alpha':0,
            'beta':0,
            'theta':0,
            'gamma':0
            }
        
    def control(self):
        while not rospy.is_shutdown():
            self.eegParser.update()
            if self.eegParser.sending_data:
                print >> sys.stdout, "meditation:", self.eegParser.current_meditation
                print >> sys.stdout, "attention:", self.eegParser.current_attention
                self.outputMap['attention'] = self.eegParser.current_attention
                self.outputMap['meditation'] = self.eegParser.current_meditation
                self.publish()
            else:
                print >> sys.stdout, "no data sent...reconnecting......"
                eegParser.write_serial("\xc2")
                
    def publish(self):
        self.controlOutput.attention = self.outputMap['attention']
        self.controlOutput.meditation = self.outputMap['meditation']
        self.controlOutput.alpha = self.outputMap['alpha']
        self.controlOutput.beta = self.outputMap['beta']
        self.controlOutput.theta = self.outputMap['theta']
        self.controlOutput.gamma = self.outputMap['gamma']
        self.controluPblisher.publish(self.controlOutput)

if __name__ == '__main__':
    try:
        control = Mindwave()
        control.control()
    except rospy.ROSInterruptException:
        pass
