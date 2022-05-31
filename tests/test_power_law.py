import numpy as np
import pytest, shutil, os, obspy
from riversound.power_law import *

def approx(x, y, p = 0.01):
    return np.abs((x - y)/x) < p

def test_power_law_synthetic():
    x = np.arange(1, 10000)
    noise = np.random.normal(0, 0.1, len(x))
    y = (x/100)**(-5/3 + noise) + (x/100)**(-5 + noise) # segmented power law with noise

    ## bin the data before estimating a power-law fit; it's too noisy otherwise
    d = band_bin(x,y)

    ## use 10% as the "approx" threshold in the examples below. 1% is hard to meet.
    ## check that, when limited to x>150, it correctly finds a slope of about -5/3
    assert approx(-5/3, calc_degree_2pt(d['centers'], d['psd'], xmin = 150), 0.1)
    ## check that, when not limited to a straight segment, it correctly finds a "wrong" slope
    assert not approx(-5/3, calc_degree_2pt(x, y, xmin = 1), 0.1)
    

