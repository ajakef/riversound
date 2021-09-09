#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:40:42 2021

@author: scott
"""
# website for glenwood bridge gauge in cfs:
# https://waterservices.usgs.gov/nwis/iv/?sites=13206000&parameterCd=00060&startDT=2021-05-24T00:00:00.000-06:00&endDT=2021-06-12T23:59:59.999-06:00&siteStatus=all&format=rdb


## The "Classic" USGS Water Data pages will be discontinued (in favor of a new "Monitoring Location" site) in 2023--just when Scott should be writing up, and when disruptions will be most unwelcome. However, the "waterservices.usgs.gov" link shown above will still work with the fancy new website. So the code below should be safe.

import matplotlib.pyplot as plt
import pandas as pd
import io
import requests
import pytz


def read_discharge(sitenum,start_time,end_time):
    """ 
        Parameters:
        sitenum is the sitenumber from the USGS website
        start_time is the start time from the USGS website in Mountain Time
        end_time is the ending time from the USGS website in Mountain Time
        
        Returns: 
        t,q where t is column vector of datetimes, and q is measured discharge
        in cubic meters per second. 
        
        Example:
            start_time = '2021-05-24T00:00:00.000-06:00'
            end_time= '2021-06-12T23:59:59.999-06:00'
            sitenum ='glenwood'
            
            t,q = read_discharge(sitenum, start_time, end_time)
            """
            
    if sitenum.lower() == 'glenwood':
        sitenum = '13206000'
    elif sitenum.lower() == 'darby':
        sitenum = '12344000'
    url = f'https://waterservices.usgs.gov/nwis/iv/?sites={sitenum}&parameterCd=00060&startDT={start_time}&endDT={end_time}&siteStatus=all&format=rdb' # f ensures parsing of braces
    print(url)
    s = requests.get(url).content
    parse_dates = ['20d']
    c= pd.read_csv(io.StringIO(s.decode('utf-8')),skiprows=27,delimiter='\t',parse_dates=['20d'])
    print(c) 
    t = c['20d']
    q = c['14n']
    
    q = q/3.28084**3 # convert from ft to m cubed per second 
    
    t = t.dt.tz_localize('America/Boise')
    t = t.dt.tz_convert('UTC')
    return [t,q]
#%%
#sitenum ='13206000'
#start_time= '2021-05-24T00:00:00.000-06:00'
#end_time= '2021-06-12T23:59:59.999-06:00'
#t,q = read_discharge(sitenum,start_time,end_time)

#plt.figure(1)
#plt.plot(t,q)
#plt.xlabel('Time')
#plt.ylabel('Discharge (m^3/s)')
#plt.title('Gauged Discharge')
