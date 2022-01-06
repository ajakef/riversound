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

def test_play_tr():
    # play an infrasound file
    tr = obspy.read('../data/mseed/2021-04-14T06_00_00..128..HDF.mseed')[0]
    tr.trim(tr.stats.starttime, tr.stats.starttime + 600)
    riversound.play_tr(tr.copy())
    riversound.play_tr(tr.copy(), low_cutoff_freq = 10)
    riversound.play_tr(tr.copy(), speedup = 256)
    riversound.play_tr(tr.copy(), speedup = 256, low_cutoff_freq = 10)
    # play an audible file
    tr = riversound.read_audiomoth('../data/audiomoth/20210414_060000.WAV', station = 'AM', location = '00')
    tr.trim(tr.stats.starttime, tr.stats.starttime + 10)
    tr.resample(16000)
    riversound.play_tr(tr.copy())
    riversound.play_tr(tr.copy(), low_cutoff_freq = 400)
    riversound.play_tr(tr.copy(), speedup = 8)
    riversound.play_tr(tr.copy(), speedup = 8, low_cutoff_freq = 400)


def test_play_signal():
    t = np.arange(16000)/8000
    riversound.play_signal(np.sin(2*np.pi*t*440), 8000)
    riversound.play_signal(np.sin(2*np.pi*t*440), 16000)

