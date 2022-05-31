import numpy as np
import pytest, shutil, os, obspy
from riversound.spectrum import * 

def approx(x, y, p = 0.01):
    return np.abs((x - y)/x) < p

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
## integral of the spectrum = mean of squared time-domain signal.
## This also checks that the function runs without error when given good inputs.
def test_spectrum_parseval():
    ## create an obspy trace filled with random data for testing
    tr = obspy.Trace(np.random.normal(0, 1, 1000000))
    tr.stats.sampling_rate = 100.0

    ## filter the trace above 1 Hz
    tr.filter('highpass', freq = 1.0)
    
    ## calculate spectrum using an infinite kurtosis threshold (never exclude
    ## a window as suspected noise) and a rectangular window to keep it simple.
    nfft = 4096
    overlap = 0.75
    spectrum_info = spectrum(tr, kurtosis_threshold=1e16, nfft = nfft, overlap = overlap, window = 'boxcar')

    ## calculate power in both the time and frequency domain, and ensure that they are equal
    psd = spectrum_info['mean']
    df = np.diff(spectrum_info['freqs'])[0]
    freq_domain_power = np.sum(psd[1:]) * df # integral of spectrum
    time_domain_power = tr.std()**2 # mean of squares
    #print(freq_domain_power/ time_domain_power-1)
    assert np.abs(freq_domain_power/time_domain_power - 1) < 1e-3 # typically under 1e-4

    ## ensure that the spectrogram dimensions and freqs are approximately correct
    assert len(spectrum_info['freqs']) == spectrum_info['specgram'].shape[0]
    assert approx(len(spectrum_info['freqs']), nfft/2)
    assert approx(spectrum_info['freqs'][1], 1/(nfft*tr.stats.delta))
    assert approx(spectrum_info['freqs'][-1], 0.5/(tr.stats.delta))
    assert approx(spectrum_info['specgram'].shape[1], len(tr.data)/nfft/(1-overlap))
## check that the pgram function obeys Parseval's relation for power:
## integral of the spectrum = mean of squared time-domain signal
## pgram ("periodogram") is the simple single Fourier transform. spectrum is the advanced one for
## averaged spectral estimates involving removal of noisy time periods (e.g., via kurtosis)
def test_pgram_parseval():
    tr = obspy.Trace(np.random.normal(0, 1, 1000000))
    tr.stats.sampling_rate = 100.0
    tr.filter('highpass', freq = 1.0)
    ## calculate spectrum using an infinite kurtosis threshold (never exclude
    ## a window as suspected noise) and a rectangular window to keep it simple
    spectrum_info = pgram(tr, 0.01)

    # calculate power in the time and frequency domains to make sure they're equal.
    psd = spectrum_info['spectrum']
    df = np.diff(spectrum_info['freqs'])[0]
    freq_domain_power = np.sum(psd[1:]) * df # integral of spectrum
    time_domain_power = tr.std()**2 # mean of squares
    print(freq_domain_power/ time_domain_power-1)
    assert np.abs(freq_domain_power/time_domain_power - 1) < 1e-3 # typically under 1e-4


## check that find_peak_freq gives the right result when given simple input
def test_find_peak_freq():
    sg = np.array([[1,1,3], # time 0
                   [2,3,0], # time 1
                   [3,2,0]])# time 2
    assert find_peak_freq(sg, freqmin = 0) == [2,1,0]
    assert find_peak_freq(sg, freqmin = 1) == [2,1,1]
    assert find_peak_freq(sg, freqmin = 0, freqmax = 1) == [0,1,0]
