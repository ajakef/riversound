import pandas as pd
import numpy as np

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
