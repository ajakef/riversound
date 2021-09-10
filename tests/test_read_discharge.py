import numpy as np
import pytest, shutil, os, obspy, riversound, datetime

## set up the temporary folder for running the tests
def setup_module():
    try:
        shutil.rmtree('tmp') # exception if the directory doesn't exist
    except:
        pass
    os.makedirs('tmp')
    os.chdir('tmp')

## remove the temporary folder where the tests are run
def teardown_module():
    os.chdir('..')
    shutil.rmtree('tmp') 

## Run a series of tests on the USGS discharge reader. If any line results in an error, or if an
## assertion turns out to be false, the test will fail.
def test_read_USGS():
    ## Download data from the Glenwood gauge; should run without error. 
    t, q = riversound.read_discharge('glenwood', '2021-05-01', '2021-05-31')

    ## Do a bunch of tests to make sure the output is valid. None should raise exceptions.
    # time and discharge outputs must be the right types
    assert type(t[0]) == datetime.datetime 
    assert (type(q[0]) == float) or (type(q[0]) == np.float64)
    # time and discharge outputs must be the same length
    assert len(t) == len(q)

    # the number of time samples should be approximately what we expect for 31 days
    assert len(t) >= (30*24*4) # 15-minute intervals
    assert len(t) <= (1 + 31*24*4) # 15-minute intervals

    # when NaNs are excluded from discharge, the mean should not be NaN (i.e., it must have good data)
    assert not np.isnan(np.nanmean(q))

## Run a series of tests on the Dry Creek Experimental Watershed discharge reader. If any line 
## results in an error, or if an assertion turns out to be false, the test will fail.
def test_read_DCEW():
    ## Download data from Lower Gauge; should run without error. 
    t, q = riversound.read_DCEW('../data/discharge/LG_StreamHrlySummary_2021.csv')

    ## Do a bunch of tests to make sure the output is valid. None should raise exceptions.
    # output data should be the correct types
    assert type(t[0]) == datetime.datetime
    assert (type(q[0]) == float) or (type(q[0]) == np.float64)
    # Make sure that output time and discharge arrays are the same length.
    assert len(t) == len(q)
    # Because we don't give time limits, we don't know in advance how long the output should be,
    # but it shouldn't be short.
    assert len(t) >= 100
    # when NaNs are excluded from discharge, the mean should not be NaN (i.e., it must have good data)    
    np.nanmean(q)

