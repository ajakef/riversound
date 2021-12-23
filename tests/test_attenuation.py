import numpy as np
import pytest, shutil, os, obspy
from riversound.attenuation import * # this will have to change once we properly package the repo

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

def E_to_dB(x): return 10 * np.log10(x)

def approx_equal(x, y, p = 0.01):
    return np.abs((x - y)/x) < p

## Compare attenuation_power_spectrum results against valid data from ISO9613-1 table 1, posted
## online at http://resource.npl.co.uk/acoustics/techguides/absorption/validata.html
def check_attenuation_power_spectrum_results():
    assert approx_equal(E_to_dB(attenuation_power_spectrum(50.12, 1, -20, 101325, 10)), -0.000589)
    assert approx_equal(E_to_dB(attenuation_power_spectrum(251.19, 1, 15, 101325, 70)), -0.00113)
    assert approx_equal(E_to_dB(attenuation_power_spectrum(1000.0, 1, 45, 101325, 20)), -0.0101)
    assert approx_equal(E_to_dB(attenuation_power_spectrum(10000.0, 1, 20, 101325, 15)), -0.267)

