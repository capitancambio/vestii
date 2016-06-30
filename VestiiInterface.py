from __future__ import division
import serial
import glob
import platform
import os


"""A part of the Vestii project during Hack the Senses
Written by: David Turner <dt237@sussex.ac.uk>
Last modified by: David Turner on 25 June, 2016
Copyright (c) 2016 David J Turner.  All right reserved
"""

__author__ = 'David Turner'


class Vestii(object):

    def __init__(self, NumElec=2):  # Runs on declaration of new Vestii object
        self.NumElec = NumElec 
        SysID = platform.system()  # Uses platform module to identify Windows/Mac/Other

        if SysID == 'Windows':
            Ports = list(serial.tools.list_ports.comports())  # List of Windows Ports
            for i in range(0, len(Ports)):
                if any("Arduino" in s for s in Ports[i]):
                    ArduinoPort = (str(Ports[i]))[2:6]  # Searches the ports for Vestii

        elif SysID == 'Darwin':
            PortString = str(glob.glob("/dev/tty.usbmodem*")) # OS X port list
            #ArduinoPort = PortString[2: (len(PortString)) - 2]
            ArduinoPort = "/dev/cu.usbmodem1411"

        else:
            ArduinoPort = "/dev/" + os.popen("dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()

        try:  # Tries to connect to the Arduino, if not possible then error is displayed
            self.Interface = serial.Serial(ArduinoPort, 9600)
            self.Connected = True  # Interface and Connected defined as class attributes
        except OSError as x:
            print(x)
            print('There seems to be an issue connecting')
            print('Either the Arduino is not connected, or Arduino serial monitor is open and accessing the port' + '\n')
            self.Connected = False
            exit()
        self.History = {}

    def UpdateVestii(self, EListPol, EListCur):
        """ 
        :EListPol: is a list with the polarities 
        :EListCur: is a list of currents  
        """
        EDict = {}
        for i in range(0, self.NumElec):
            EDict["ElectrodePol{0}".format(i)] = EListPol[i]  # ElectrodePol is a polarity value
            EDict["ElectrodeCur{0}".format(i)] = EListCur[i]  # ElectrodeCur is a current value

        self.State = EDict

        if self.State != self.History:
            if self.Connected is True:  # Only send update if data has changed
                # ToSend = str(self.NumElec)
                # for y in range(0, self.NumElec):
                    # ToSend = ToSend + (str(self.State["ElectrodeCur{0}".format(y)]) + '#' + str(self.State["ElectrodePol{0}".format(y)]) + '$')
                # ToSend = ToSend + '\n'  # Control string to send to Arduino
                # self.Interface.write(ToSend)  # Writes over serial to Arduino
                to_send = "%d%d%3d%3d\n" % (EListPol[0],EListPol[1], EListCur[0],EListCur[1])
                self.Interface.write(to_send)
                #print "SENT!!!", to_send
                # print "Read", self.Interface.read(1)
            if self.Connected is False:
                print('The fuck you doing')
                # ToSend = str(self.NumElec)
                # for y in range(0, self.NumElec):
                    # ToSend = ToSend + (str(self.State["ElectrodeCur{0}".format(y)]) + '#' + str(
                        # self.State["ElectrodePol{0}".format(y)]) + '$')
                # ToSend = ToSend + '\n'  # Control string to send to Arduino
                # print(ToSend)  # Prints string

        self.History = self.State

    def ZeroVestii(self):
        ZeroPol = []
        ZeroCur = []
        for i in range(0, self.NumElec):
            ZeroPol.append(0)
            ZeroCur.append(0)

        self.UpdateVestii(ZeroPol, ZeroCur)
