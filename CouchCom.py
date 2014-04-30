# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:17:19 2014

@author: universe
"""

import cloudant
import time
 
class CouchCom:
    """
    Communication with the CouchDB
    """
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
        