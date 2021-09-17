import riversound, glob, obspy, matplotlib, datetime
import numpy as np
import matplotlib.pyplot as plt
## run this code if you're using ipython and it doesn't show plot windows
# %matplotlib qt 

## FFT works best when data length is a power of 2, so use this function to help determine window size.
def next_power_2(x):
    return int(2**np.ceil(np.log2(x)))

def interp_times(t_out, t, q):
    t_out = np.array([x.timestamp() for x in t_out])
    t = np.array([x.timestamp() for x in t])
    return np.interp(t_out, t, q)

def reformat(l): # turn list l into a numpy array
    lengths = np.array([len(i) for i in l])
    normal_length = lengths[lengths > 0][0]
    if any((lengths != 0) & (lengths != normal_length)):
        raise ValueError('nonzero lengths of elements of l must all be the same')
    for i in np.where(lengths == 0)[0]:
        l[i] = np.zeros(normal_length)
    return np.array(l)

    
    
    
## define paths containing infrasound and audible data
#path = '/data/jakeanderson/2021_Boise_River/long_term/DivDam/2021-05-25_DiversionDam/'
path = '/data/jakeanderson/2021_Boise_River/long_term/Eckert/'
path_infrasound = path + 'mseed_119_all'
path_audible = path + 'AM004_all'

day1 = obspy.UTCDateTime('2021-03-01')
day2 = obspy.UTCDateTime('2021-06-30')
n_days = int(np.round((day2 - day1)/86400)) # length of study period in days

## Enter the times of day (UTC) to read data from.
start_hour = 3 + 6 # 6 is time zone difference vs UTC
end_hour = 4 + 6


## Initialize the output variables, so they can be filled in during the loop.
plot_times = np.zeros(n_days, dtype = object)

## For 2-D data like these, it's a little easier to initialize as an empty list and then convert to
## np.array. Reason is because audiomoth data can have multiple sample rates, and because of that
## we don't know the number of points in the spectrum until after we start reading files.
times_infrasound = []
meanspec_list_infrasound = [] 
medspec_list_infrasound = []
power_infrasound = []
times_audible = []
meanspec_list_audible = []
medspec_list_audible = []
power_audible = []

## Loop through all the days, read the data, calculate spectra, and save to outputs
for i in range(n_days):
    current_day = day1 + i*86400
    t1 = current_day.replace(hour = start_hour)
    t2 = current_day.replace(hour = end_hour)
    tr_infrasound, tr_audible = riversound.read_infrasound_audible(t1, t2, path_infrasound, path_audible)
    nfft_infrasound = next_power_2(10 / tr_infrasound.stats.delta) # >10-sec windows for freq resolution finer than 0.1 Hz
    nfft_audible = next_power_2(0.1 / tr_audible.stats.delta) # >0.1-sec windows for freq res finer than 10 Hz

    print([i, current_day, tr_infrasound, tr_audible])
    
    plot_times[i] = current_day.datetime
    #    times_infrasound.append((tr_infrasound.stats.starttime + 0.5*(tr_infrasound.stats.endtime - tr_infrasound.stats.starttime)).datetime)
    times_infrasound.append(t1.datetime)
    times_audible.append(t1.datetime)

    ## infrasound
    try: # check whether the data can be processed (i.e., make sure it isn't missing)
        tr_infrasound.filter('highpass', freq = 1, zerophase = True)
        spec_info = riversound.spectrum(tr_infrasound, nfft = nfft_infrasound)
    except: # do nothing if there's an error in the above code block
        medspec_list_infrasound.append([])
        meanspec_list_infrasound.append([])
        power_infrasound.append(np.nan)
    else: # append the results to the output lists if there's no error
        freqs_infrasound_all = spec_info['freqs']
        medspec_list_infrasound.append(spec_info['median'])
        meanspec_list_infrasound.append(spec_info['mean'])
        power_infrasound.append(np.sum(spec_info['mean']) * np.diff(spec_info['freqs'])[0]) # integral spec * df

    ## audible
    try:
        spec_info = riversound.spectrum(tr_audible, nfft = nfft_audible)
        assert len(spec_info['mean']) > 0 # raises an exception if an empty result is returned
    except:
        medspec_list_audible.append([])
        meanspec_list_audible.append([])
        power_audible.append(np.nan)
    else:
        freqs_audible_all = spec_info['freqs']
        medspec_list_audible.append(spec_info['median'])
        meanspec_list_audible.append(spec_info['mean'])
        power_audible.append(np.sum(spec_info['mean']) * np.diff(spec_info['freqs'])[0])

## reformat result lists from the loop into numpy arrays that are easy to plot
w = (freqs_infrasound_all < 40) & (freqs_infrasound_all > 1)
freqs_infrasound = freqs_infrasound_all[w]    
meanspec_infrasound = reformat(meanspec_list_infrasound)[:,w]
medspec_infrasound = reformat(medspec_list_infrasound)[:,w]
#power_infrasound = reformat(power_infrasound)

w = (freqs_audible_all < 20000) & (freqs_audible_all > 40)
freqs_audible = freqs_audible_all[w]    
meanspec_audible = reformat(meanspec_list_audible)[:,w]    
medspec_audible = reformat(medspec_list_audible)[:,w]
#power_audible = reformat(power_audible)

xlim = [np.min(times_infrasound + times_audible), np.max(times_infrasound+times_audible)]
## plot the discharge, power, and spectrogram
plt.figure() 
plt.subplot(3,1,1) # discharge
t, q = riversound.read_discharge('glenwood', xlim[0] - datetime.timedelta(days=1), xlim[1] + datetime.timedelta(days=1))
plt.semilogy(t,q)
plt.semilogy(times_infrasound + times_audible, interp_times(times_infrasound+times_audible, t, q), 'k.')

plt.xlim(xlim[0], xlim[1])
plt.ylabel('discharge (m$^3$/s)')

plt.subplot(3,1,2) # power
plt.semilogy(times_infrasound, power_infrasound)
plt.semilogy(times_audible, power_audible)
plt.xlim(xlim[0], xlim[1])
plt.ylabel('Power (Pa$^2$)')
plt.legend(['Infrasound', 'Audible'])

plt.subplot(3,1,3) # spectrogram
riversound.image(np.log10(meanspec_audible), times_audible, freqs_audible, crosshairs = False, log_y = True)
riversound.image(np.log10(meanspec_infrasound), times_infrasound, freqs_infrasound, crosshairs = False, log_y = True)
plt.xlim(xlim[0], xlim[1])
plt.yticks(np.arange(5), 10**np.arange(5))
plt.ylabel('Frequency (Hz)')

## plot the daily spectra
plt.figure()
num_colors = len(plt.rcParams['axes.prop_cycle'].by_key()['color'])
for i in range(n_days):
    col = plt.rcParams['axes.prop_cycle'].by_key()['color'][i%num_colors]
    plt.loglog(freqs_infrasound, meanspec_infrasound[i,:], color = col)
    plt.loglog(freqs_audible, meanspec_audible[i,:], color = col, label = plot_times[i].strftime('%Y-%m-%d'))
plt.legend() # uses labels from plt.loglog
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (counts$^2$/Hz)')

