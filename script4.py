# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:16:20 2016

@author: markprosser
"""

#%reset        #clear variables

import numpy as np
import matplotlib.pyplot as plt
import os
import time
import datetime
import math



SC = 1364
LATRES = 1
LONGRES = 2

#Local time or London time?
opt1 = 1
#1 = put in LONtime, LONG = LOCtime
#2 = put in LOCtime, LONG = LONtime
#3 = put in LOCtime, LONtime = LONG

LATMAT = np.empty((180./LATRES,360./LONGRES))
LATMAT[:] = np.NAN
LONGMAT = np.empty((180./LATRES,360./LONGRES))
LONGMAT[:] = np.NAN
SIMAT = np.empty((180./LATRES,360./LONGRES)) #Solar Insolation
SIMAT[:] = np.NAN
PERCMAT = np.empty((180./LATRES,360./LONGRES)) #Solar Insolation Percentage
PERCMAT[:] = np.NAN


for i in range(0,len(LATMAT[0])): 
    LATMAT[:,i]=np.arange(90-LATRES/2,-90+LATRES/2-1,-LATRES)
    LATMAT
    
for i in range(0,len(LONGMAT)): 
    LONGMAT[i,:]=np.arange(-180+LONGRES/2,180-LONGRES/2+1,LONGRES)
    LONGMAT
    
for j in range(0,len(SIMAT[0])):    
    for i in range(0,len(SIMAT)): 
    
        LAT = LATMAT[i,j]
            
        if opt1==1:
            mydateLON = datetime.datetime(1994, 6, 21, 18, 0, 0)   
            LONG = LONGMAT[i,j]
            TIMEadj = LONG/180*12*3600
            mydateLOC=mydateLON + datetime.timedelta(0,TIMEadj) #datetimeobj
            mydateLOC = mydateLOC.timetuple() #structdateobj
            #mydateLOC = datetime.datetime(*mydateLOC[:6])
    
        ts=((mydateLOC[3]*3600) + mydateLOC[4]*60 + mydateLOC[5]) - (12*3600);
        LAT = math.radians(LAT)
        LONG = math.radians(LONG)

        DJ = mydateLOC[7]
        #DL FAM p318 eq 9.7
        if mydateLOC[0] >= 2001:
            DL = (mydateLOC[0] - 2001)/4
        else:
            DL = ((mydateLOC[0] - 2000)/4) - 1 

        NJD = 364.5 + ((mydateLOC[0]-2001)*365) + DJ + DL

        GM = 357.528 + 0.9856003*NJD; #DEG
        LM = 280.460 + 0.9856474*NJD; #DEG
        LAMec = LM + 1.915*math.sin(math.radians(GM)) + 0.020*math.sin(math.radians(2*GM)) #in degrees?
        EPSob = 23.439 - 0.0000004*NJD #DEG
        DELTA = math.degrees(math.asin(math.sin(math.radians(EPSob))*math.sin(math.radians(LAMec)))) #Solar Declination Angle (DEG)
        Ha = math.degrees((2*math.pi*ts)/86400) #DEG
        THETAs = math.degrees(math.acos(math.sin(LAT)*math.sin(math.radians(DELTA)) + math.cos(LAT)*math.cos(math.radians(DELTA))*math.cos(math.radians(Ha)))) #Solar Zenith Angle (DEG)


        if math.cos(math.radians(THETAs)) < 0:
            INSOL = 0
        else:
            INSOL = SC*math.cos(math.radians(THETAs))

        SIMAT[i,j]=INSOL
        PERCMAT[i,j]=INSOL/SC*100

plt.pcolor(np.flipud(SIMAT), cmap='cuntfuck')
SIMAT.shape
plt.show()
