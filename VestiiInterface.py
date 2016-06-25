from __future__ import division
import serial
import glob
import platform
import os
import numpy as np


"""A part of the Vestii project during Hack the Senses
Written by: David Turner <dt237@sussex.ac.uk>
Last modified by: David Turner on 25 June, 2016
Copyright (c) 2016 David J Turner.  All right reserved
"""

__author__ = 'David Turner'


class Vestii(object):

    def __init__(self):  # Runs on declaration of new Vestii object
        self.NumElec = 4
        SysID = platform.system()  # Uses platform module to identify Windows/Mac/Other

        if SysID == 'Windows':
            Ports = list(serial.tools.list_ports.comports())  # List of Windows Ports
            for i in range(0, len(Ports)):
                if any("Arduino" in s for s in Ports[i]):
                    ArduinoPort = (str(Ports[i]))[2:6]  # Searches the ports for Vestii

        elif SysID == 'Darwin':
            PortString = str(glob.glob("/dev/tty.usbmodem*")) # OS X port list
            ArduinoPort = PortString[2: (len(PortString)) - 2]

        else:
            ArduinoPort = "/dev/" + os.popen("dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()

        try:  # Tries to connect to the Arduino, if not possible then error is displayed
            self.Interface = serial.Serial(ArduinoPort, 9600)
            self.Connected = True  # Interface and Connected defined as class attributes
        except OSError:
            print('There seems to be an issue connecting')
            print('Either the Arduino is not connected, or Arduino serial monitor is open and accessing the port' + '\n')
            self.Connected = False

        self.History = {}

    def UpdateVestii(self, EListPol, EListCur):
        EDict = {}

        for i in range(0, self.NumElec):
            EDict["ElectrodePol{0}".format(i)] = EListPol[i]
            EDict["ElectrodeCur{0}".format(i)] = EListCur[i]

        self.State = EDict

        if self.State != self.History:
            if self.Connected is True:  # Only send update if data has changed
                self.Interface.write(str(self.NumElec))
                for y in range(0, self.NumElec):
                    self.Interface.write(str(self.State["ElectrodeCur{0}".format(y)]) + '#' + str(self.State["ElectrodePol{0}".format(y)]) + '$')
                self.Interface.write('\n')

            if self.Connected is False:
                print('The fuck you doing')

        self.History = self.State

print('------------------Vestii V1------------------')
print('Control Vestii project from a computer')

EListPol = [0, 1, 0, 1]
EListCur = [0.3, 0.2, 0.3, 0.1]

Device = Vestii()
Device.UpdateVestii(EListPol, EListCur)








"""

def setState(self, AngleState):  # To be called when the stored state of the display needs to be changed
    ChangedTo = np.zeros((self.shape[0], self.shape[1]))  # AngleState MUST be passed in as a sLen by sLen matrix
    for y in xrange(self.shape[0]):  # Moves through the 2D array representing the TGD
        for x in xrange(self.shape[1]):
            ChangedTo[y, x] = (-1 if self.state[y, x] == AngleState[y, x] else AngleState[y, x])
            # ChangedTo matrix stores the new values of changed taxels, no change is represented by -1
    self.state = AngleState  # Then updates current state
    return ChangedTo


def updateDisplay(self, ChangeMatrix):  # Pushes update to display
    for y in xrange(self.shape[0]):  # Cycles through every taxel on display
        for x in xrange(self.shape[1]):
            if self.Connected is True and ChangeMatrix[y, x] > 0:  # Will only move taxels that have changed
                self.Interface.write(str(ChangeMatrix[y, x]) + '#' + str((self.shape * y) + x + 1) + '\n')
                # Utilises serial connection to Arduino
    if self.Connected is False:
        print(ChangeMatrix)
        print(self.state)


def resetDisplay(self):  # Sets all taxels to zero state
    Reset = np.zeros((self.shape[0], self.shape[1]), dtype=int)
    Reset.fill(MinServoAng)
    ChangedTo = TGD.setState(self, Reset)
    TGD.updateDisplay(self, ChangedTo)
"""