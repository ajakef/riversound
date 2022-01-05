import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import riversound

from scipy.optimize import curve_fit
from scipy.integrate import trapezoid, cumulative_trapezoid

def calc_degree_2pt(x, y, xmin = 0.5, xmax = np.inf):
    """
    Estimate the degree of a power-law relationship by drawing a line between min/max values. Within
    the given xmin-to-xmax region, two points are selected near (not at) the min and max y-values.

    Parameters:
    -----------
    --x, y: coordinates to fit a power-law relationship
    --xmin, xmax: lower and upper limits to fit

    Returns:
    --------
    --degree of power-law relationship
    --graphical output (plot of data and fit line)
    """
    w = np.where((x >= xmin) & (x < xmax))[0]
    x = x[w]
    y = y[w]
    i1 = np.where(y > (0.1*y.max()))[0][-1]
    i2 = np.where(y < (2*y.min()))[0][0]
    d = np.log(y[i1]/y[i2]) / np.log(x[i1]/x[i2])
    a = y[i1]/x[i1]**d
    plt.loglog(x, y)
    xx = np.array([x[i1], x[i2]])
    plt.loglog(xx, a * xx**d)
    return d
  

def read_ref_spec(filename):
    """
    Read a reference spectrum
    
    Parameters:
    -----------
    filename: path and name of reference spectrum file
    
    Returns:
    --------
    tuple of frequencies (Hz) and power spectral densities (Pa^2/Hz) of spectrum

    Example (run from riversound root directory):
    freqs, spectrum = read_ref_spec('data/reference_spectra/MRBD_2021-09-13.txt')
    """
    s = pd.read_csv(filename)
    return (np.array(s.freqs), np.array(s.spectrum))

def band_bin(freqs, spectrum, bands_per_octave = 3):
    """
    Integrate a power spectrum over logarithmic frequency bins

    Parameters:
    -----------
    freqs, spectrum: frequencies and PSDs of spectrum (numpy arrays; Hz and Pa^2/Hz)
    bands_per_octave: how many freq bins per octave (doubling of frequency); 1/3 octave is common

    Result: 
    -------
    dict with following items:
    --bounds: limits of frequency bands (length is 1 more than other items)
    --centers: center of each frequency band (geometric mean of upper and lower limit)
    --power: integrated power over each frequency band (Pa^2)
    --psd: mean power spectral density over each band (Pa^2/Hz)
    --psd53: mean power spectral density over each band, multiplied by freq**(5/3)
    """
    band_bounds = 2**(np.arange(15*bands_per_octave)/bands_per_octave)
    band_centers = np.exp(0.5 * (np.log(band_bounds[1:]) + np.log(band_bounds[:-1])))
    band_widths = np.diff(band_bounds)

    w = np.where((band_centers > 0.5) & (band_centers < 1e4))[0]
    w_bounds = np.concatenate([w, [1+w[-1]]]) # band_bounds will need one additional element
    band_powers = np.array([_integrate(freqs, spectrum, band_bounds[i], band_bounds[i+1]) for i in w])
    band_psd = band_powers/band_widths[w]
    return {'bounds':band_bounds[w_bounds], 'centers':band_centers[w], 'power':band_powers, 'psd':band_psd, 'psd53':band_psd * band_centers[w]**(5/3)}

def _integrate(x, y, x1 = -np.inf, x2 = np.inf): 
    w = (x >= x1) & (x < x2)
    return trapezoid(y[w], x[w])
