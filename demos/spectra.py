import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew

import sys
sys.path.append('riversound')
from riversound.spectrum import spectrum, image

st = obspy.read('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-04-10_AnnMorrison/mseed/2021-04-01T00_00_00..150..HDF.mseed')
st.filter('highpass', freq = 5.0)
t1 = obspy.UTCDateTime('2021-04-01T08:00:00')
st.trim(t1, t1 + 3*3600)
sg, freqs, times = spectrum(st[0], kurtosis_threshold = 20)
image(np.log10(sg.T), times, np.log10(freqs+freqs[1]))

#%% kurtosis_threshold demo
plt.close('all')
sg, freqs, times = spectrum(st[0], kurtosis_threshold = 2000)
plt.figure(); plt.semilogy(sg[100:,:].sum(0), '.')
sg, freqs, times = spectrum(st[0], kurtosis_threshold = 0.25)
plt.figure(); plt.semilogy(sg[100:,:].sum(0), '.')

#%% runmed_radius_t demo
plt.close('all')
sg, freqs, times = spectrum(st[0])
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(sg[200:400,:].sum(0), '.')
plt.subplot(2,1,2)
image(np.log10(sg.T), times, np.log10(freqs+freqs[1]))


sg, freqs, times = spectrum(st[0], runmed_radius_t = 1, runmed_radius_f = 1)
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(sg[200:400,:].sum(0), '.')
plt.subplot(2,1,2)
image(np.log10(sg.T), times, np.log10(freqs+freqs[1]))

