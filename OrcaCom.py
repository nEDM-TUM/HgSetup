# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 13:30:58 2014

@author: universe
"""

import cloudant
import time
import pprint
 
class orca:
    def __init__(self):
        # Authentication
        self.acct = cloudant.Account(uri="http://raid.nedm1:5984")
        self.res = self.acct.login("HgLaserPc", "clu$terXz")
        assert self.res.status_code == 200
        # Grab the correct database
        self.db = self.acct["nedm%2Fhg_laser"]
        self.des = self.db.design("nedm_default")
     
    def post(self, adoc):
            # Push to the database
        r = self.des.post("_update/insert_with_timestamp", params=adoc)
        return r

    def query(self,adoc):
        r = self.des.post("_update/insert_with_timestamp", params=adoc)
        
        resp = r.json()
        if "ok" not in resp: 
            raise Exception("Urrgh, insertion problem")
       
        doc_return = self.db[resp["id"]]    
        while 1:
            new_resp = doc_return.get().json()
            if "response" in new_resp: break
            time.sleep(0.5)
           
        if "ok" not in new_resp["response"]:
            raise Exception("Urrgh, problem with response")
        
        return new_resp
        
    
    def trigger(self):
        # Define the document
        adoc = {
        "type" : "command",
        "execute" : "trigger"
        }
        self.post(adoc)
    def isrunning(self):
        adoc = {
        "type" : "command",
        "execute" : "isrunning"
        }
        new_resp=self.query(adoc)
        print new_resp["response"]["return"] 
        if new_resp["response"]["return"]:
            return True
        return False
    def startRun(self):
        """
        start a Run, if not Running. Stop Run and start
        a new one if running. 
        Return the run number of the new run
        """
        if self.isrunning():
            self.stopRun()
        adoc={
        "type" : "command",
        "execute" : "runstart"
        }
        self.post(adoc)
        return self.getRunNumber()
    def stopRun(self):
        adoc={
        "type" : "command",
        "execute" : "runstop"
        }
        self.post(adoc)
        
    def getRunNumber(self):
        adoc={
        "type":"command",
        "execute":"runnumber"
        }
        new_resp=self.query(adoc)
        return new_resp["response"]["return"]
#        pprint.pprint(new_resp)     
        print new_resp["response"]["return"]