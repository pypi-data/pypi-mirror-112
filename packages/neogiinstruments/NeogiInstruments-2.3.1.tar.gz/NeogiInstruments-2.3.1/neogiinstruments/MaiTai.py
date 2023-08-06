# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:29:27 2020

@author: Mai Tai
"""

import pyvisa
from time import sleep

name = "MaiTai"
hwid = ["10C4:EA60"]
serial_number = ["0001"]

class instrument:

    def __init__(self,port):
        rm = pyvisa.ResourceManager()
        current_port = port.name
        self.MaiTai = rm.open_resource(f'ASRL/dev/{current_port}::INSTR')
        self.MaiTai.baud_rate = 115200

    def Shutter(self,val=0):
        '''Returns print string'''
        if val == 1:
            self.MaiTai.write("SHUT 1")
            #print("Shutter Opened")
        else:
            self.MaiTai.write("SHUT 0")
            #print("Shutter Closed")

    def Get_Wavelength(self):
        """Helper function for instrumental to avoid clutter and make code
        more readable
        >>>returns int"""

        w = int(self.MaiTai.query("WAV?").split('n')[0])
        return w

    def Set_Wavelength(self,position):
        """Helper function for instrumental to avoid clutter and make code
        more readable
        Note that this function allways shutters the laser
        >>>returns null"""
        if  690<=position<=1040:
            self.Shutter(0)
            self.MaiTai.write(f"WAV {position}")
            sleep(10)
        else:
            print('Invalid Wavelength')


    def On(self):
        self.MaiTai.write('ON')

    def Off(self):
        self.Shutter(0)
        self.MaiTai.write("OFF")


