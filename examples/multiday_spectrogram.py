## Calculate spectrogram over a several-day period using data from only certain times of day (in order to reduce computational expense and avoid noisy periods)

import riversound, glob, obspy
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib qt # probably not needed

#path_pattern = '/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/mseed/2021-05-[123]*149*' # change to the files you want to read
#path_pattern = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-05-17/AM006/*_090000.WAV' # change to the files you want to read
path_pattern = '/home/jake/2022-08-31_Goodwin/audiomoth/202206[01]?_16*WAV'
fn = sorted(glob.glob(path_pattern))

if len(fn) == 0:
    raise Exception('No matching files found! Double-check path_pattern')

## if needed, enter the times of day to trim data. These are used by later lines
## that can be commented or uncommented.
start_hour = 2 + 6 # 6 is time zone difference vs UTC
end_hour = 5 + 6

nfft = 2**14 # change to 2**10 for Gem

## initialize the output variables, so they can be filled in during the loop
start_times = np.zeros(len(fn), dtype = object)
plot_times = np.zeros(len(fn), dtype = object)
power = np.zeros(len(fn))
meanspec = np.zeros([len(fn), nfft // 2 + 1]) 
medspec = np.zeros([len(fn), nfft // 2 + 1])

## loop through all the data files
for i, file in enumerate(fn):
    print('%i of %i' % (i, len(fn)))
    # tr = obspy.read(file)[0] # uncomment these lines if using Gem
    # tr.filter('highpass', freq = 1)
    
    tr = riversound.read_audiomoth(file) # comment this if using Gem

    ## uncomment these lines if trimming a long file to a shorter length
    #t1 = tr.stats.starttime.replace(hour = start_hour, minute = 0, second = 0)
    #tr.trim(t1, t1 + 3600*(end_hour - start_hour))
    
    start_times[i] = tr.stats.starttime.datetime
    plot_times[i] = tr.stats.starttime.datetime.replace(hour=0)
    spec_info = riversound.spectrum(tr, nfft = nfft)
    freqs = spec_info['freqs']
    medspec[i,:] = spec_info['median']
    meanspec[i,:] =  spec_info['mean']
    power[i] = np.sum(spec_info['mean']) * np.diff(freqs)[0] # integral spec * df

w = freqs > 50
freqs = freqs[w]
medspec = medspec[:,w]
meanspec = meanspec[:,w]

## plot the spectrogram and power
plt.figure()
plt.subplot(2,1,1)
riversound.image(np.log10(meanspec + 0.001 * np.quantile(meanspec, 0.95)), plot_times, freqs, crosshairs = False, log_y = True)
plt.ylim([100, 10000])
plt.ylabel('Frequency (Hz)')
plt.subplot(2,1,2)
plt.plot(plot_times, power)
plt.ylabel('Power (counts$^2$)')

## plot the daily spectra
plt.figure()
for i in range(meanspec.shape[0]):
    plt.loglog(freqs, meanspec[i,:])

plt.legend([t.strftime('%Y-%m-%d') for t in plot_times])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (counts$^2$/Hz)')
