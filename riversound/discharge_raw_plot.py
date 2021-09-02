#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:40:42 2021

@author: scott
"""
# website for glenwood bridge gauge in cfs:
# https://waterservices.usgs.gov/nwis/iv/?sites=13206000&parameterCd=00060&startDT=2021-05-24T00:00:00.000-06:00&endDT=2021-06-12T23:59:59.999-06:00&siteStatus=all&format=rdb

import matplotlib.pyplot as plt
import pandas as pd
import io
import requests
import pytz


def read_discharge(url):
    """ This function depends on the variable url, a string of the USGS link
    containing data of interest. Outputs: t,q are time and discharge respectively.
    Time has been converted to UTC within the function as well. """
    s = requests.get(url).content
    parse_dates = ['20d']
    c= pd.read_csv(io.StringIO(s.decode('utf-8')),skiprows=27,delimiter='\t',sep=',',parse_dates=['20d'])
    print(c) 
    t = c['20d']
    q = c['14n']
    
    t = t.dt.tz_localize('Europe/London')
    t = t.dt.tz_convert('UTC')
    return [t,q]
#%%
url = 'https://waterservices.usgs.gov/nwis/iv/?sites=13206000&parameterCd=00060&startDT=2021-05-24T00:00:00.000-06:00&endDT=2021-06-12T23:59:59.999-06:00&siteStatus=all&format=rdb'
t,q = read_discharge(url)

plt.figure(1)
plt.plot(t,q)
plt.xlabel('Time')
plt.ylabel('Discharge (ft^3/s)')
plt.title('Gauged Discharge')



#In [12]: 'filledinvalue %s something' % '12345'
#Out[12]: 'filledinvalue 12345 something'
#give function station number, then do start and end times