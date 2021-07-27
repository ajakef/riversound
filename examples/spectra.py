import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew
import riversound

#%% Plot spectrum of river data
## replace this file name with a file on your computer
st = obspy.read('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-04-10_AnnMorrison/mseed/2021-04-01T00_00_00..150..HDF.mseed')
st.filter('highpass', freq = 5.0)

## These optional lines trim the data to a user-designated time interval. If
## left commented, all the data from the mseed is processed.
#t1 = obspy.UTCDateTime('2021-04-01T08:00:00')
#duration_hours = 1
#st.trim(t1, t1 + duration_hours * 3600)

## Calculate the spectrum using a moderately severe kurtosis threshold
spectrum_dict = riversound.spectrum(st[0], kurtosis_threshold = 0.25)
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])
plt.xlabel('Time (sec) after %s' % st[0].stats.starttime.strftime(format = '%Y-%m-%d %H:%M'))
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')

#%% kurtosis_threshold demo
## Kurtosis is a good but not perfect way to identify windy time intervals and
## exclude them from the spectrum calculation. A typical kurtosis_threshold
## would be around 0.25 to 0.5; 2000 is intended to be an impossible bar to
## meet, so no data are excluded based on kurtosis.
plt.close('all')
spectrum_dict = riversound.spectrum(st[0], kurtosis_threshold = 2000)
plt.figure(); plt.semilogy(spectrum_dict['specgram'][100:,:].sum(0), '.')
spectrum_dict = riversound.spectrum(st[0], kurtosis_threshold = 0.25)
plt.figure(); plt.semilogy(spectrum_dict['specgram'][100:,:].sum(0), '.')

#%% runmed_radius_t demo
## Median filters are a good way to remove outliers, but they risk biasing data
## when the mean of non-outliers is different from the median. Experiment with
## this to make sure it does what you want.
plt.close('all')
spectrum_dict = riversound.spectrum(st[0])
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(spectrum_dict['specgram'][200:400,:].sum(0), '.')
plt.subplot(2,1,2)
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])


spectrum_dict = riversound.spectrum(st[0], runmed_radius_t = 1, runmed_radius_f = 1)
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(spectrum_dict['specgram'][200:400,:].sum(0), '.')
plt.subplot(2,1,2)
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])

