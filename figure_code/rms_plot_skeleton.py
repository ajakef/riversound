import numpy as np
import matplotlib.pyplot as plt
import obspy, glob, datetime
from scipy.stats import kurtosis
    
## define a function to find the start time of a mseed file given its file name.
## we could just read the files directly and find the start times from the contents, but that would be a lot slower.
## keep in mind that the file name may include the path
def find_mseed_start_time(filename):
    
    ## code goes here...use the "split" method for the filename string
    first_split = filename.split('..')
    better_split = first_split[0].split('/')
    date_split = better_split[-1]
    return obspy.UTCDateTime(date_split)
#%%
mseed_list = sorted(glob.glob('/home/scott/Desktop/2021-04-30-Whitewater/mseed/*')) # fix the folder path if needed

t1 = obspy.UTCDateTime('2021-04-09T22:00:00')
t2 = obspy.UTCDateTime('2021-04-30T21:00:00')

overlap = 0.5 # play with these
window_length_sec = 60

window_start_time = t1

## Find the first file to read; it'll be the last one whose start time is before t1.
mseed_index = 0
while True:
    if find_mseed_start_time(mseed_list[mseed_index + 1]) > t1:
        st = obspy.read(mseed_list[mseed_index])
        break
    else:
        mseed_index += 1

# loop until the current window starts after the end of the time period we're studying
mid_time_list = []
rms_list = []
kurtosis_list = []

while window_start_time < t2:
    ## Check to see if st has data all the way from window_start_time to (window_start_time +
    ## window_length_sec). If not, read and append the next mseed and increment mseed_index.
    while st[0].stats.endtime < (window_start_time + window_length_sec):
        mseed_index += 1
        print('Reading %s' % mseed_list[mseed_index]) ## keep the user informed
        st += obspy.read(mseed_list[mseed_index])
        ## merge the stream so that it just contains one trace, and fill any short gaps
        st.merge(fill_value = 'interpolate') 

    st.trim(window_start_time, t2) # get rid of unneeded old data
        
    ## use st.slice create a temporary trace with just this time window to do calculations on
    st_win = st.slice(window_start_time,window_start_time+window_length_sec)
    tr_win = st_win[0]
    ## a stream is a list of traces, so you'll need to index this to extract a trace
    ## Use obspy.Stream methods of st_win to detrend and high-pass filter the data "in place".
    tr_win.detrend()
    tr_win.filter("highpass", freq=5)
    ## This means picking a good low corner frequency based on the data--take a look with PQL.
    window_rms = tr_win.std()
    ## Use the std method of tr_win and the "kurtosis" function imported from scipy.stats to update
    ## the output lists.
    window_kurtosis = kurtosis(tr_win.data) # kurtosis needs numeric data
    rms_list.append(window_rms) # good
    kurtosis_list.append(window_kurtosis) # good
    mid_time_list.append((window_start_time + window_length_sec/2).datetime)
    ## FYI, obspy uses its own time class "UTCDateTime" because the default Python class "datetime"
    ## is only microsecond-precise. That happens to be good enough for us. Plot formatting is easier
    ## with the normal datetime class, so the previous line converts it before plotting.

    ## finally, increment window_start_time
    window_start_time += (1-overlap) * window_length_sec
#%%
## Done looping; convert the output lists into a more convenient format (numpy array)
mid_time_list = np.array(mid_time_list)
rms_list = np.array(rms_list)
kurtosis_list = np.array(kurtosis_list)

## plot the results
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(mid_time_list, rms_list, 'k.')

## make a second subplot with only the low-kurtosis windows plotted
low_kurt = kurtosis_list < 0.2# * kurtosis_list.min())
plt.subplot(2,1,2)
plt.plot(mid_time_list[low_kurt], rms_list[low_kurt], 'k.')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.figure(2)
plt.plot(kurtosis_list, rms_list, '.')
plt.xlabel('Kurtosis')
plt.ylabel('Amplitude')
