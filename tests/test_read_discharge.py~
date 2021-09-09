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

#path = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-05-17/'
def test_read_infrasound_audible():
    path = '../data/'
    path_infrasound = path + 'mseed'
    path_audio = path + 'audiomoth'
    t1 = obspy.UTCDateTime('2021-04-14T06_00_00')
    t2 = obspy.UTCDateTime('2021-04-14T07_00_00')
    st = riversound.read_infrasound_audible(t1, t2, path_infrasound, path_audio)
    
    assert len(st) == 2
    assert len(st.select(station='')[0].data) == (30*48000)
    assert len(st.select(station='128')[0].data) == (3600*100)

