#!/usr/bin/python

import Config, time
from serial import *

class KITTempBoard:
    
    def __init__(self):
        self.__cfg = Config.Config()
        self.__params = self.__cfg.getParameters()
        self.__port = Serial(self.__params['port'], baudrate=19200)
        self.__prevReadout = "-266.\t-266.\t-266.\t-266."
        self.__port.write("O") # set request mode
        self.__port.write("N") # averaging off (send "M" for on) 

    def setPTConfig(self,hexDec=0):
        # Settings in hex:
        # PT100: 0 | PT1000: 1
        #
        #
        # PT1 | PT2 | PT3 | PT4
        #  1     0     1     0  
        #
        #
        # reversed order: 0 1 0 1 = 5
        #
        self.__port.write("C%s" % hexDec)
        time.sleep(5)

    def getTemperature(self,sensor=-1):
        self.__port.write("R")
        time.sleep(float(self.__params['sleep']))
        readout = self.__port.readline().strip().replace("\x00","")

        if len(readout.split("\t")) < 4:
            if sensor is -1:
                return self.__prevReadout
            else:
                return self.__prevReadout.split("\t")[sensor-1]
        else:
            self.__prevReadout = readout
            if sensor is -1:
                return readout
            else:
                return readout.split("\t")[sensor-1]
        
    def getStatus(self):
        self.__port.write("Z")
        time.sleep(float(self.__params['sleep']))

        return self.__port.read(36).strip()

if __name__ == '__main__':
    
    t = KITTempBoard()
    print t.getStatus()
    while True:
        print t.getTemperature()
    
