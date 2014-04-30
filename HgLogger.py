# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:20:10 2014

@author: universe
"""

import CouchCom
import OrcaCom

class Hglog:
    def __init__(self):
        self.couch=CouchCom.CouchCom()
        self.orca=OrcaCom.orca()

    def wavelengthmeter(self, wl):
        adoc = {
        "type" : "log",
        "value" : {"wavelengthmeter, nm" : str(wl)}
        }
        self.couch.post(adoc)
    
    def triggered(self):
        adoc = {
        "type" : "log",
        "value" : {"triggered": 1}
        }
        self.couch.post(adoc)
    
    def runstarted(self, runNumber):
        adoc = {
        "type" : "log",
        "value" : {"run started with No": runNumber}
        }
        self.couch.post(adoc)
        
    def readoutStatus(self, status):
        adoc = {
        "type" : "log",
        "value" : {"readout beam status": status}
        }
        self.couch.post(adoc)
        
    def pumpStatus(self, status):
        adoc = {
        "type" : "log",
        "value" : {"puming beam status": status}
        }
        self.couch.post(adoc)
        