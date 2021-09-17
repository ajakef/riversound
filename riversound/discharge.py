import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io, requests, pytz
import obspy
import datetime 



def read_DCEW(filename = '/home/jake/Work/StreamAcoustics/DCEW/LG_StreamHrlySummary_2021.csv', skiprows = 18, na_values = '#NUM!', encoding = 'utf-7'):
    """
    Read a data file from a Dry Creek Experimental Watershed stream gauge

    Parameters:
    -----------
    filename : str
    Name of .csv data file to read. Must be .csv, not .xls, .xlsx, .ods, etc.

    skiprows : int
    Number of rows to skip before data begins; optional, in case of inconsistent formatting.

    na_values : str
    Symbol for missing numeric data in data file; optional, in case of inconsistent formatting.

    encoding : int
    Encoding used in file (often utf-7 or utf-8); optional, in case of inconsistent formatting.

    Returns:
    --------
    tuple (t, q):
    t: numpy.array of sample times (type datetime, time UTC)
    q: numpy.array of discharge estimates (cubic meters per second)
    """
    
    ## use indices instead of column names in case column names are encoded wrong (likely)
    df = pd.read_csv(filename, encoding_errors = 'ignore', skiprows = skiprows, sep = ',', encoding = encoding, na_values = na_values)
    t = pd.to_datetime(df.iloc[:,0], format='%m/%d/%Y %H:%M')
    t = t.dt.tz_localize('-06:00')
    t = t.dt.tz_convert('UTC')
    t = np.array([i.to_pydatetime() for i in t])
    return t, df.iloc[:,1] * 0.001
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:40:42 2021

@author: scott
"""
# website for glenwood bridge gauge in cfs:
# https://waterservices.usgs.gov/nwis/iv/?sites=13206000&parameterCd=00060&startDT=2021-05-24T00:00:00.000-06:00&endDT=2021-06-12T23:59:59.999-06:00&siteStatus=all&format=rdb


## The "Classic" USGS Water Data pages will be discontinued (in favor of a new "Monitoring Location" site) in 2023--just when Scott should be writing up, and when disruptions will be most unwelcome. However, the "waterservices.usgs.gov" link shown above will still work with the fancy new website. So the code below should be safe.

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
            end_time = '2021-06-12T23:59:59.999-06:00'
            sitenum ='glenwood'
            
            t,q = riversound.read_discharge(sitenum, start_time, end_time)
            """
    start_time = _reformat_time(start_time)
    end_time = _reformat_time(end_time)
    if sitenum.lower() == 'glenwood':
        sitenum = '13206000'
    elif sitenum.lower() == 'darby':
        sitenum = '12344000'
    url = f'https://waterservices.usgs.gov/nwis/iv/?sites={sitenum}&parameterCd=00060&startDT={start_time}&endDT={end_time}&siteStatus=all&format=rdb' # f ensures parsing of braces
    print(url)
    s = requests.get(url).content
    parse_dates = ['20d']
    #c= pd.read_csv(io.StringIO(s.decode('utf-8')),skiprows=27,delimiter='\t',parse_dates=['20d'])
    c= pd.read_csv(io.StringIO(s.decode('utf-8')),skiprows=0,delimiter='\t', comment = '#').iloc[1:,:] # using comments instead of skipped rows to make it less sensitive to web page format
    t = pd.to_datetime(c.iloc[:,2])
    q = c.iloc[:,4].astype(float)
    
    q = q/3.28084**3 # convert from ft to m cubed per second
    q = np.array(q)
    
    t = t.dt.tz_localize('America/Boise')
    t = t.dt.tz_convert('UTC')
    t = np.array([i.to_pydatetime() for i in t])
    return [t,q]




def _reformat_time(t):
    if (type(t) is obspy.UTCDateTime) or (type(t) is datetime.datetime):
        return t.isoformat()
    elif type(t) is str:
        return obspy.UTCDateTime(t).isoformat()
    else:
        raise TypeError('Input time must be str, UTCDateTime, or datetime.datetime')
    
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
