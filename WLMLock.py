# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 15:26:24 2014

@author: universe
"""

import digilock
import WLM
import time
import pid 
import threading
from time import strftime
killme=False
locked=False
update_setpoint=False
update_I=False
update_P=False
globsetp=1014.9215
globi=0.1
globp=0.5
class pidthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.locker=locker()
    def run(self):
        self.locker.lock()
        
class wlmlocker():
    def __init__(self):
        pass
    def lock(self):
        self.lockerthread=pidthread()
        self.lockerthread.start()
    def changesetpoint(self,setpoint):
        global update_setpoint
        global globstep
        globstep=setpoint
        update_setpoint=True
    def changeI(self, I):
        global update_I
        global globi
        globi=I
        update_I=True
    def changeP(self, P):
        global update_P
        global globp
        globp=P
        update_P=True
    def unlock(self):
        global killme
        killme=True
        
        
        

class locker():
    def __init__(self):
        self.digilock_ip='localhost'
        self.wlm=WLM.WavelengthMeter()
        self.digi=digilock.digilock(self.digilock_ip,60001)
    def lock(self,wl_setpoint=1014.9215,P=0.5,I=0.1,D=0,Derivator=0,Integrator=0,Integrator_max=40,Integrator_min=-40,Max_Stepsize=0.005):
        global update_setpoint
        global update_I
        global update_P
        global locked
        global killme
        locked=True
        print "lock started"
        #get piezo offset at beginning
        self.voltagestart=self.digi.getoffset()
        #define starting correction value to enable limitation of the stepsize
        corr_old=self.voltagestart
        print self.voltagestart
        print "pre pid"
        #set Ki to initial offset
        pi=pid.PID(P,I,D,Derivator,Integrator,Integrator_max-0.1*Integrator_max,Integrator_min+0.1*Integrator_min)
        pi.setPoint(wl_setpoint)
        pi.setIntegrator(self.voltagestart)
        print killme
        counter=0
        #the actual pid controller loop:
        #counter is used to not break until several measurementsin a row  exceed max values
        while not killme:
#            print "in the loop"
            try:
                counter=(counter-1 if counter > 0 else 0) 
                if update_setpoint:
                    self.voltagestart=self.digi.getoffset()
                    print self.voltagestart
                    pi.setPoint(globsetp)
                    pi.setIntegrator(self.voltagestart)
                    update_setpoint=False
                    print "setpoint changed"
                if update_I:
                    pi.setKi(globi)
                    update_I=False
                if update_P:
                    pi.setKp(globp)
                    update_P=False
                #get current wavelength
                wl=self.wlm.getWL()
                time.sleep(1)
                #update pid
                print wl
                corr=pi.update(wl)
                #print corr
                #check for limits
                if corr>Integrator_max or corr< Integrator_min:
                    if counter<3:
                        counter+2
                        corr=(Integrator_max if corr>Integrator_max else Integrator_min)
                    else:
                        print "reached a Voltage limit at: "+strftime("%Y-%m-%d %H:%M:%S")
                        print "please readjust wavelength mechanically"
                        killme=True
                        break
                #set piezo offset voltage
              #  raw_input("now or never")
                self.digi.setoffset(corr)
                #limit the stepsize to avoid laser jumps
                if corr-corr_old>Max_Stepsize:
                    corr=corr+Max_Stepsize
                elif corr_old-corr>Max_Stepsize:
                    corr=corr-Max_Stepsize
                corr_old=corr
            except KeyboardInterrupt:
                locked=False
                break
        locked=False