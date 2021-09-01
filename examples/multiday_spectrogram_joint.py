import riversound, glob, obspy
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib qt # probably not needed

## FFT works best when data length is a power of 2, so use this function to help determine window size.
def next_power_2(x):
    return int(2**np.ceil(np.log2(x)))

## define paths containing infrasound and audible data
path = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-05-17/'
path_infrasound = path + 'mseed'
path_audible = path + 'AM006'

day1 = obspy.UTCDateTime('2021-05-10')
day2 = obspy.UTCDateTime('2021-05-17')
n_days = int(np.round((day2 - day1)/86400)) # length of study period in days

## Enter the times of day (UTC) to read data from.
start_hour = 3 + 6 # 6 is time zone difference vs UTC
end_hour = 4 + 6


## Initialize the output variables, so they can be filled in during the loop.
plot_times = np.zeros(n_days, dtype = object)
power_infrasound = np.zeros(n_days)
power_audible = np.zeros(n_days)

## For 2-D data like these, it's a little easier to initialize as an empty list and then convert to
## np.array. Reason is because audiomoth data can have multiple sample rates, and because of that
## we don't know the number of points in the spectrum until after we start reading files.
meanspec_infrasound = [] 
medspec_infrasound = []
meanspec_audible = []
medspec_audible = []

## Loop through all the days, read the data, calculate spectra, and save to outputs
for i in range(n_days):
    current_day = day1 + i*86400
    t1 = current_day.replace(hour = start_hour)
    t2 = current_day.replace(hour = end_hour)
    tr_infrasound, tr_audible = read_infrasound_audible(t1, t2, path_infrasound, path_audible)
    nfft_infrasound = next_power_2(10 / tr_infrasound.stats.delta) # >10-sec windows for freq resolution finer than 0.1 Hz
    nfft_audible = next_power_2(0.1 / tr_audible.stats.delta) # >0.1-sec windows for freq res finer than 10 Hz

    print([i, current_day, tr_infrasound, tr_audible])
    
    plot_times[i] = current_day

    ## infrasound
    tr_infrasound.filter('highpass', freq = 1, zerophase = True)
    spec_info = riversound.spectrum(tr_infrasound, nfft = nfft_infrasound)
    freqs_infrasound = spec_info['freqs']
    medspec_infrasound.append(spec_info['median'])
    meanspec_infrasound.append(spec_info['mean'])
    power_infrasound[i] = np.sum(spec_info['mean']) * np.diff(freqs_infrasound)[0] # integral spec * df

    ## audible
    spec_info = riversound.spectrum(tr_audible, nfft = nfft_audible)
    freqs_audible = spec_info['freqs']
    medspec_audible.append(spec_info['median'])
    meanspec_audible.append(spec_info['mean'])
    power_audible[i] = np.sum(spec_info['mean']) * np.diff(freqs_audible)[0] # integral spec * df

w = (freqs_infrasound < 40) & (freqs_infrasound > 1)
freqs_infrasound = freqs_infrasound[w]    
meanspec_infrasound = np.array(meanspec_infrasound)[:,w]    
medspec_infrasound = np.array(medspec_infrasound)[:,w]

w = (freqs_audible < 20000) & (freqs_audible > 40)
freqs_audible = freqs_audible[w]    
meanspec_audible = np.array(meanspec_audible)[:,w]    
medspec_audible = np.array(medspec_audible)[:,w]

## plot the spectrogram and power
plt.figure()
plt.subplot(2,1,1)
riversound.image(np.log10(meanspec_audible), plot_times, freqs_audible, crosshairs = False, log_y = True)
riversound.image(np.log10(meanspec_infrasound), plot_times, freqs_infrasound, crosshairs = False, log_y = True)
plt.yticks(np.arange(5), 10**np.arange(5))
plt.ylabel('Frequency (Hz)')
plt.subplot(2,1,2)
plt.semilogy(plot_times, power_infrasound)
plt.semilogy(plot_times, power_audible)
plt.ylabel('Power (Pa$^2$)')
plt.legend(['Infrasound', 'Audible'])

## plot the daily spectra
plt.figure()
for i in range(n_days):
    col = plt.rcParams['axes.prop_cycle'].by_key()['color'][i]
    plt.loglog(freqs_infrasound, meanspec_infrasound[i,:], color = col)
    plt.loglog(freqs_audible, meanspec_audible[i,:], color = col, label = plot_times[i].strftime('%Y-%m-%d'))
plt.legend() # uses labels from plt.loglog
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (counts$^2$/Hz)')
