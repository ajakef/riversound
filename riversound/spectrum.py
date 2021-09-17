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
    if len(tr.data) == 0:
        return {'specgram':np.zeros([nfft,1]), 'freqs':np.arange(nfft), 'times':np.array([0]), 'mean':np.zeros(nfft), 'median':np.zeros(nfft), 'stdev': np.zeros(nfft)}
    
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

def round_sig(f, p): # thanks StackOverflow denizb
    f = np.array(f)
    return np.array([float(('%.' + str(p) + 'e') % ff) for ff in f])

def image(Z, x = None, y = None, aspect = 'equal', zmin = None, zmax = None, ax = plt, crosshairs=False, log_x = False, log_y = False):
    # Z rows are x, columns are y
    if x is None:
        x = np.arange(Z.shape[0])
    if y is None:
        y = np.arange(Z.shape[1])

    if log_x:
        w = x > 0
        plot_x = np.log10(x[w])
        x = x[w]
        Z = Z[:,w]
    else:
        plot_x = x

    if log_y:
        w = y > 0
        plot_y = np.log10(y[w])
        y = y[w]
        Z = Z[:,w]
    else:
        plot_y = y
        
    im = ax.pcolormesh(plot_x, plot_y, Z.T, vmin = zmin, vmax = zmax, shading = 'nearest')#, cmap='YlOrRd')
    if crosshairs:
        ax.hlines(0, x[0], x[-1], 'k', linewidth=0.5)
        ax.vlines(0, y[0], y[-1], 'k', linewidth=0.5)
    if log_x and (ax is plt):
        xt = round_sig(10**plt.xticks()[0],0)
        xt = xt[(np.log10(xt) > plt.xlim()[0]) & (np.log10(xt) < plt.xlim()[1])]
        plt.xticks(np.log10(xt), xt)
    if log_y and (ax is plt):
        yt = round_sig(10**plt.yticks()[0],0)
        yt = yt[(np.log10(yt) > plt.ylim()[0]) & (np.log10(yt) < plt.ylim()[1])]
        plt.yticks(np.log10(yt), yt)
    return im
    


def apply_function_windows(st, f, win_length_sec, overlap = 0.5):
    """
    Run an analysis (or suite of analyses) on overlapping windows for some dataset
    
    Parameters:
    -----------
    st : obspy.Stream
    Stream including data to divide into windows and analyze

    f : function
    Accepts single variable "st" (obspy.Stream), returns dictionary of results

    win_length_sec : float
    Length of analysis windows [seconds]

    overlap : float
    Proportion of a window that overlaps with the previous window [unitless, 0-1]
 
    Returns:
    --------
    dictionary with following items:
    --t_mid (obspy.UTCDateTime): mean time of each window
    --all elements of the output of "f", joined into numpy arrays

    Note:
    -----
    For each time window, the stream is trimmed to fit, but not tapered, detrended, or otherwise 
    processed. If those steps are necessary, be sure they are carried out in f().
"""
    # f must input a stream and return a dict
    eps = 1e-6
    t1 = st[0].stats.starttime
    t2 = st[0].stats.endtime
    data_length_sec = t2 - t1
    num_windows = 1 + int(np.ceil((data_length_sec - win_length_sec) / (win_length_sec * (1 - overlap)) - eps))
    print(num_windows)
    for i in range(num_windows):
        win_start = t1 + i*(data_length_sec - win_length_sec) / (num_windows-1)
        st_tmp = st.slice(win_start-eps, win_start + win_length_sec - eps, nearest_sample = False)
        win_dict = f(st_tmp)
        if i == 0:
            output_dict = {key:[] for key in win_dict.keys()}
            output_dict['t_mid'] = []
        for key in win_dict.keys():
            output_dict[key].append(win_dict[key])
        output_dict['t_mid'].append(win_start + win_length_sec/2)
    output_dict = {key:np.array(output_dict[key]) for key in output_dict.keys()}
    return output_dict

def pgram(x, dt, type = 'power', onesided = True):
    """
    Calculate the periodogram of a signal, obeying Parseval's relation.
    
    Parameters:
    -----------
    x : numpy.array or list 
    Time series to analyze

    dt: float
    time interval between samples (seconds)

    type : string
    type of spectrum to return; can be "power", "amplitude", or "dB"

    onesided : boolean
    if True, eliminate frequencies above Nyquist, and add their power to corresponding lower 
    frequencies

    Returns:
    --------
    Dict, with following elements:
    --freqs: frequencies of output spectrum
    --spectrum: output spectrum
    """
    N = len(x)
    df = 1/(N*dt)
    power = np.abs(np.fft.fft(x))**2/N**2/df ## obeys Parseval's relation: df*sum(power) = mean(x^2)
    freq = df * np.arange(N)
    if onesided:
        power[(freq > 0) & (freq < 0.5/dt)] *= 2 # don't double f = 0 or Nyquist
        power = power[freq <= 0.5/dt]
        freq = freq[freq <= 0.5/dt]
    ## decide what kind of spectrum to return (default "power")
    if type.lower() == 'power':
        spec = power
        spec_units = 'Pa^2/Hz'
    elif type.lower()[:3] == 'amp':
        spec = np.sqrt(power)
        spec_units = 'Pa/sqrt(Hz)'
    elif type.lower() == 'db':
        spec = 10*np.log10(power)
        spec_units = 'dB Pa/sqrt(Hz)'
    else:
        raise Exception('type %s not supported' % type)
    ## parseval check: N = 10;dt = 0.0001;x = np.random.normal(0,1,N);np.sum(pgram(x, dt)['spectrum'] / (N*dt)) / np.mean(x**2)

    return {'freqs':freq, 'spectrum':spec}#, 'type':type, 'spectrum_units':spec_units}
