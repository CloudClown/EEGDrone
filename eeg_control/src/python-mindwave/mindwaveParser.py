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
            'gamma':0,
            'delta':0
            }
        self.capVal = 50
        self.spectra = []
        
    def parse(self):
        while not rospy.is_shutdown():
            self.eegParser.update()
            if self.eegParser.sending_data:
                #print >> sys.stdout, "meditation:", self.eegParser.current_meditation
                #print >> sys.stdout, "attention:", self.eegParser.current_attention
                if len(self.eegParser.raw_values) >= 500:
                    self.outputMap['attention'] = self.eegParser.current_attention
                    self.outputMap['meditation'] = self.eegParser.current_meditation
               
                    #retrieve spectrum from the bin power function
                    spectrum,relativeSpectrum = bin_power(self.eegParser.raw_values[-self.eegParser.buffer_len:], range(self.capVal), 512)
                    self.spectra.append(array(relativeSpectrum))
                    if len(self.spectra) > 30:
                        self.spectra.pop(0)
                    spectrum = mean(array(self.spectra),axis=0)
                    #temp variables
                    delta = []
                    theta = []
                    alpha = []
                    beta = []
                    gamma = []
                    for i in range((self.capVal) - 1):
                        #print >> sys.stdout, "spectrum:",spectrum[i]
                        #print >> sys.stdout, "i value:",i
                        if i < 3:
                            delta.append(spectrum[i])
                        elif i < 8:
                            theta.append(spectrum[i])
                        elif i < 13:
                            alpha.append(spectrum[i])
                        elif i < 30:
                            beta.append(spectrum[i])
                        else:
                            gamma.append(spectrum[i])
                            
                    self.outputMap['delta'] = mean(delta, axis=0)*1000
                    self.outputMap['theta'] = mean(theta, axis=0)*1000
                    self.outputMap['alpha'] = mean(alpha, axis=0)*1000
                    self.outputMap['beta'] = mean(beta, axis=0)*1000
                    self.outputMap['gamma'] = mean(gamma, axis=0)*1000
                    self.publish()
            else:
                print >> sys.stdout, "no data sent...reconnecting......"
                self.eegParser.write_serial("\xc2")
                
    def publish(self):
        self.controlOutput.attention = self.outputMap['attention']
        self.controlOutput.meditation = self.outputMap['meditation']
        self.controlOutput.alpha = self.outputMap['alpha']
        self.controlOutput.beta = self.outputMap['beta']
        self.controlOutput.theta = self.outputMap['theta']
        self.controlOutput.gamma = self.outputMap['gamma']
        self.controlOutput.delta = self.outputMap['delta']
        print >> sys.stdout, "BrainWave Data", self.outputMap
        self.controlPublisher.publish(self.controlOutput)

if __name__ == '__main__':
    try:
        control = Mindwave()
        control.parse()
    except rospy.ROSInterruptException:
        pass
