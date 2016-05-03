#!/usb/bin/python
import os
from ConfigParser import ConfigParser

class Config:

    def __init__(self):
        self.__prs = ConfigParser()
        self.__cfg = 'config.cfg'
        self.__params = self.__loadCfg('config.cfg') if self.__cfgExists() else self.__getDefault()
       
    def __cfgExists(self):
        return os.path.exists(self.__cfg)
    
    def __getDefault(self):
        
        fileName = "config.cfg"

        generalDict = {'pt'    : -1,
                       'sleep' : 0,
                       'port'  : '/dev/ttyUSB1'
                       }

        with open(fileName,'w') as cfgFile:
            self.__prs.add_section('General')
            for key in generalDict:
                self.__prs.set('General', key, generalDict[key])
            
            self.__prs.write(cfgFile)

        return generalDict
    
    def __loadCfg(self,cfg):
        
        generalDict = {}

        self.__prs.read(cfg)
        for section in self.__prs.sections():
            for (key, val) in self.__prs.items(section):
                generalDict[key] = val

        return generalDict
                
    def getParameters(self):
        return self.__params
    
        
        
