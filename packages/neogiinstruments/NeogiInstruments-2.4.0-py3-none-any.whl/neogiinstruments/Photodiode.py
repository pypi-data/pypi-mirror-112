# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:21:23 2020

@author: Mai Tai
"""

import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import numpy as np

'''Needs to be rewritten in class structure'''

name = "Photodiode"
hwid = ["software"]

class instrument():
    def __init__(self,port):
        pass
    def gather_data(self):
        with nidaqmx.Task() as task:
            self.ai_channel = task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
            r = task.read(number_of_samples_per_channel=100)
            m = np.mean(r)
            delta = np.std(r)
            return m, delta
