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

def test_read_audiomoth():
    ## check that the function reads a wav file to an obspy trace without error
    #print(os.getcwd())
    tr = riversound.read_audiomoth('../data/audiomoth/20210414_060000.WAV', station = 'AM', location = '00')

    ## check that the output trace has the correct start time
    assert tr.stats.starttime == obspy.UTCDateTime('20210414_0600')
    ## check that it can be written to an output file without error
    riversound.write_wav(tr, path = '../tmp/')
