import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew

def spectrum(tr, criterion_function = 'default', runmed_radius_t = 0, runmed_radius_f = 0, nfft = 1024, overlap = 0.5, kurtosis_threshold = 0.5, window = 'hamming'):
    if criterion_function == 'default':
        def criterion_function(x): return kurtosis(x) < kurtosis_threshold
    
    freqs, times, sg = spectrogram(tr.data, fs = tr.stats.sampling_rate, window = window, nperseg = nfft, noverlap = overlap, detrend = 'linear')

    ## If a criterion function is defined, apply it to all the time windows
    ## and change results for failing windows to NaN.
    if criterion_function is not None:
        for i, t in enumerate(times):
            j1 = np.round(t * tr.stats.sampling_rate - nfft/2)
            if not criterion_function(tr.data[int(j1):int(j1 + nfft)]):
                sg[:,i] = np.NaN

    ## Apply median filter if applicable. If more than half the values in a
    ## median filter window are nan, the output for that window will be too.
    if (runmed_radius_t > 0) or (runmed_radius_f > 0):
        kernel_size = (1 + 2*runmed_radius_f, 1 + 2*runmed_radius_t)
        w = ~np.isnan(sg[0,:])
        sg[:,w] = median_filter(sg[:,w], kernel_size)
        
    return {'specgram':sg, 'freqs':freqs, 'times':times, 'mean':np.nanmean(sg,1), 'median':np.nanmedian(sg,1)}
    
def image(Z, x = None, y = None, aspect = 'equal', zmin = None, zmax = None, ax = plt, crosshairs=False):
    # Z rows are x, columns are y
    if x is None:
        x = np.arange(Z.shape[0])
    if y is None:
        y = np.arange(Z.shape[1])

    im = ax.pcolormesh(x, y, Z.T, vmin = zmin, vmax = zmax)#, cmap='YlOrRd')
    if crosshairs:
        ax.hlines(0, x[0], x[-1], 'k', linewidth=0.5)
        ax.vlines(0, y[0], y[-1], 'k', linewidth=0.5)
    return im
    

