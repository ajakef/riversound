import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew
import riversound

#%% Read a river .mseed file recorded by a Gem
## replace this file name with a file on your computer
#tr = obspy.read('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-04-10_AnnMorrison/mseed/2021-04-01T00_00_00..150..HDF.mseed')[0]
#tr.filter('highpass', freq = 5.0) # filter out low-frequency noise below 5 Hz

## optional: comment out the last line and replace it with this to read an
## audiomoth .wav file instead
tr = riversound.read_audiomoth('/home/jake/Dropbox/riversound/data/20210414_060000.WAV')


## These optional lines trim the data to a user-designated time interval. If
## left commented, all the data from the mseed is processed.
#t1 = obspy.UTCDateTime('2021-04-01T08:00:00')
#duration_hours = 1
#st.trim(t1, t1 + duration_hours * 3600)

#%% Plot spectrum of river data

## Calculate the spectrum using a moderately severe kurtosis threshold
spectrum_dict = riversound.spectrum(tr, kurtosis_threshold = 0.25)

## plot spectrogram; white bars are time intervals rejected by kurtosis criterion
plt.figure()
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])
plt.xlabel('Time (sec) after %s' % tr.stats.starttime.strftime(format = '%Y-%m-%d %H:%M'))
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')

## plot average spectrum
plt.figure()
plt.loglog(spectrum_dict['freqs'], spectrum_dict['mean'])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power ($counts^2$)')
plt.title('Mean Spectrum')
           
#%% kurtosis_threshold demo
## Kurtosis is a good but not perfect way to identify windy time intervals and
## exclude them from the spectrum calculation. A typical kurtosis_threshold
## would be around 0.25 to 0.5; 2000 is intended to be an impossible bar to
## meet, so no data are excluded based on kurtosis.
plt.close('all')
spectrum_dict = riversound.spectrum(tr, kurtosis_threshold = 2000)
plt.figure(); plt.semilogy(spectrum_dict['specgram'][100:,:].sum(0), '.')
spectrum_dict = riversound.spectrum(tr, kurtosis_threshold = 0.25)
plt.figure(); plt.semilogy(spectrum_dict['specgram'][100:,:].sum(0), '.')

#%% runmed_radius_t demo
## Median filters are a good way to remove outliers, but they risk biasing data
## when the mean of non-outliers is different from the median. Experiment with
## this to make sure it does what you want.
plt.close('all')
spectrum_dict = riversound.spectrum(tr)
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(spectrum_dict['specgram'][200:400,:].sum(0), '.')
plt.subplot(2,1,2)
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])


spectrum_dict = riversound.spectrum(tr, runmed_radius_t = 1, runmed_radius_f = 1)
plt.figure();
plt.subplot(2,1,1)
plt.semilogy(spectrum_dict['specgram'][200:400,:].sum(0), '.')
plt.subplot(2,1,2)
riversound.image(np.log10(spectrum_dict['specgram'].T), spectrum_dict['times'], spectrum_dict['freqs'])

