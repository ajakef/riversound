import numpy as np
import pytest, shutil, os, obspy
from riversound.spectrum import * # this will have to change once we properly package the repo

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


## check that the spectrum function obeys Parseval's relation for power:
## integral of the spectrum = mean of squared time-domain signal
def test_spectrum_parseval():
    tr = obspy.Trace(np.random.normal(0, 1, 1000000))
    tr.stats.sampling_rate = 100.0
    tr.filter('highpass', freq = 1.0)
    ## calculate spectrum using an infinite kurtosis threshold (never exclude
    ## a window as suspected noise) and a rectangular window to keep it simple
    spectrum_info = spectrum(tr, kurtosis_threshold=1e16, nfft = 4096, window = 'boxcar')
    psd = spectrum_info['mean']
    df = np.diff(spectrum_info['freqs'])[0]
    freq_domain_power = np.sum(psd[1:]) * df # integral of spectrum
    time_domain_power = tr.std()**2 # mean of squares
    print(freq_domain_power/ time_domain_power-1)
    assert np.abs(freq_domain_power/time_domain_power - 1) < 1e-3 # typically under 1e-4

    
## check that the pgram function obeys Parseval's relation for power:
## integral of the spectrum = mean of squared time-domain signal
def test_spectrum_parseval():
    tr = obspy.Trace(np.random.normal(0, 1, 1000000))
    tr.stats.sampling_rate = 100.0
    tr.filter('highpass', freq = 1.0)
    ## calculate spectrum using an infinite kurtosis threshold (never exclude
    ## a window as suspected noise) and a rectangular window to keep it simple
    spectrum_info = pgram(tr, 0.01)
    psd = spectrum_info['spectrum']
    df = np.diff(spectrum_info['freqs'])[0]
    freq_domain_power = np.sum(psd[1:]) * df # integral of spectrum
    time_domain_power = tr.std()**2 # mean of squares
    print(freq_domain_power/ time_domain_power-1)
    assert np.abs(freq_domain_power/time_domain_power - 1) < 1e-3 # typically under 1e-4
