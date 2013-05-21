#!/usr/bin/python
#Author: Jackie Jin
#This python interface is based on Mr.Andreas Klostermann's interface
#with PyEEG and Pygame
#This is the project link:https://github.com/akloster/python-mindwave
#License: MIT

from numpy import *
import scipy
from pyeeg import bin_power
from parser import Parser
import rospy

class MindWaveControl():
    def __init__(self):
        
