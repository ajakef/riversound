import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew

def spectrum(tr, criterion_function = 'default', runmed_radius_t = 0,
             runmed_radius_f = 0, nfft = 1024, overlap = 0.5,
             kurtosis_threshold = 0.5, window = 'hamming'):
    """Calculate spectrogram and Welch spectrum of an obspy trace, where either
    kurtosis thresholds or median filters can be used to exclude noisy times.

    Parameters
    ----------
    tr : obspy.Trace
        Data trimmed to period for which spectrum is calculated
    criterion_function : function, 'default', or None
        Function that returns True or False and determines whether a time window
        is too noisy to process (False) or acceptable (True). If 'default', test
        whether the time window's kurtosis is less than kurtosis_threshold. If 
        None, do not exclude any time windows.
    runmed_radius_t : int
        Radius of median filter in time dimension. If zero, do not apply a median
        filter over time.
    runmed_radius_f : int
        Radius of median filter in frequency dimension. If zero, do not apply a 
        median filter over frequency.
    nfft: int
        Length of fft to calculate. The minimum nonzero frequency in the output
        spectrum will be 1/(nfft * dt).
    overlap : float
        Proportion of overlap between adjacent time windows; must be >=0 and <1.
    kurtosis_threshold : float
        If using criterion_function = 'default', time windows with kurtosis 
        greater than this value are considered noisy and excluded.
    window : str
        Window function to use when calculating individual spectral estimates. 
        See help(scipy.signal.windows.getwindow) for options. Common choices
        include 'hamming', 'hann', 'blackmanharris', and 'boxcar' (rectangular).
    
    Returns
    -------
    Dictionary with following items:
    specgram: spectrogram of time period
    times: times of output spectrogram
    freqs: frequencies of output spectrum and spectrogram
    mean: mean spectrum (Welch's method)
    median: median spectrum
    stdev: standard deviation of mean spectrum

    Example
    -------
    import obspy, riversound
    import matplotlib.pyplot as plt
    st = obspy.read()
    spec_dict = riversound.spectrum(st[0])
    plt.loglog(spec_dict['freqs'], spec_dict['mean'])

    """
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
        
    return {'specgram':sg, 'freqs':freqs, 'times':times, 'mean':np.nanmean(sg,1), 'median':np.nanmedian(sg,1), 'stdev': np.nanstd(sg, 1)}
    
def image(Z, x = None, y = None, aspect = 'equal', zmin = None, zmax = None, ax = plt, crosshairs=False):
    # Z rows are x, columns are y
    if x is None:
        x = np.arange(Z.shape[0])
    if y is None:
        y = np.arange(Z.shape[1])

    im = ax.pcolormesh(x, y, Z.T, vmin = zmin, vmax = zmax, shading = 'nearest')#, cmap='YlOrRd')
    if crosshairs:
        ax.hlines(0, x[0], x[-1], 'k', linewidth=0.5)
        ax.vlines(0, y[0], y[-1], 'k', linewidth=0.5)
    return im
    

