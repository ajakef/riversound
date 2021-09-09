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


def test_read_USGS():
    ## Download data from the Glenwood gauge; should run without error. 
    t, q = riversound.read_discharge('glenwood', '2021-05-01', '2021-05-31')

    ## Do a bunch of tests to make sure the output is valid. None should raise exceptions.
    assert type(t[0]) == datetime.datetime
    assert (type(q[0]) == float) or (type(q[0]) == np.float64)
    assert len(t) == len(q)
    assert len(t) >= (30*24*4) # 15-minute intervals
    assert len(t) <= (1 + 31*24*4) # 15-minute intervals
    assert not np.isnan(np.nanmean(q))

def test_read_DCEW():
    ## Download data from the Glenwood gauge; should run without error. 
    t, q = riversound.read_DCEW('../data/discharge/LG_StreamHrlySummary_2021.csv')

    ## Do a bunch of tests to make sure the output is valid. None should raise exceptions.
    assert type(t[0]) == datetime.datetime
    assert (type(q[0]) == float) or (type(q[0]) == np.float64)
    assert len(t) == len(q)
    assert len(t) >= 100 # 
    np.nanmean(q)

