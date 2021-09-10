import numpy as np
import pytest, shutil, os, obspy, riversound 

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

## Run tests on read_infrasound_audible using data packaged in the repository
def test_read_infrasound_audible():
    ## set up function inputs
    path = '../data/'
    path_infrasound = path + 'mseed'
    path_audio = path + 'audiomoth'
    t1 = obspy.UTCDateTime('2021-04-14T06_00_00')
    t2 = obspy.UTCDateTime('2021-04-14T07_00_00')

    ## make sure the function runs without error
    st = riversound.read_infrasound_audible(t1, t2, path_infrasound, path_audio)

    # check that the function outputs are correct
    assert len(st) == 2 # the output should have two traces
    
    # the infrasound trace should have the right length (3600 sec * 100 Hz sample rate)
    assert len(st.select(station='128')[0].data) == (3600*100)
    
    # the audible trace should have the right length (30 sec * 48 kHz sample rate)
    assert len(st.select(station='')[0].data) == (30*48000)

