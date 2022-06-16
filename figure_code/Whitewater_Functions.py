# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:22:53 2022

@author: ttatu
"""
# Import Data Needed

## Calculate spectrogram over a several-day period using data from only certain times of day (in order to reduce computational expense and avoid noisy periods)

import riversound, glob, obspy, gemlog
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib qt # probably not needed

def interp_times(t_out, t, q):
    t_out = np.array([x.timestamp() for x in t_out])
    t = np.array([x.timestamp() for x in t])
    return np.interp(t_out, t, q)

#%%

# Infrasound/Gem Function

def infrasound(files):
    ## if needed, enter the times of day to trim data. These are used by later lines
    ## that can be commented or uncommented.
    start_hour = 3 + 6 # 6 is time zone difference vs UTC
    end_hour = 4 + 6
    
    nfft = 2**10 # change to 2**10 for Gem and 2**14 for Audiomoth
    
    ## initialize the output variables, so they can be filled in during the loop
    start_times = np.zeros(len(files), dtype = object)
    plot_times = np.zeros(len(files), dtype = object)
    power = np.zeros(len(files))
    meanspec = np.zeros([len(files), nfft // 2 + 1]) 
    medspec = np.zeros([len(files), nfft // 2 + 1])
    
    ## loop through all the data files
    for i, file in enumerate(files):
        print('%i of %i' % (i, len(files)))
        tr = obspy.read(file)[0] # UNCOMMENT these lines if using Gem
        try:
            tr.detrend()
            tr.filter('highpass', freq = 10)
            tr = gemlog.deconvolve_gem_response(tr)
        
            #tr = riversound.read_audiomoth(file) # COMMENT this if using Gem
        
            ## uncomment these lines if trimming a long file to a shorter length
            t1 = tr.stats.starttime.replace(hour = start_hour, minute = 0, second = 0)
            tr.trim(t1, t1 + 3600*(end_hour - start_hour))
            
            start_times[i] = tr.stats.starttime.datetime
            plot_times[i] = tr.stats.starttime.datetime.replace(hour=0)
            spec_info = riversound.spectrum(tr, nfft = nfft)
            freqs = spec_info['freqs']
            medspec[i,:] = spec_info['median']
            meanspec[i,:] =  spec_info['mean']
            power[i] = np.sum(spec_info['mean']) * np.diff(freqs)[0] # integral spec * df
        except:
            pass
    
    return plot_times, power, freqs, meanspec

#%%

# Audiable/AudioMoth Function

def audiodata(files):
    ## if needed, enter the times of day to trim data. These are used by later lines
    ## that can be commented or uncommented.
    start_hour = 3 + 6 # 6 is time zone difference vs UTC
    end_hour = 4 + 6
    
    nfft = 2**14 # change to 2**10 for Gem and 2**14 for Audiomoth
    
    ## initialize the output variables, so they can be filled in during the loop
    start_times = np.zeros(len(files), dtype = object)
    plot_times = np.zeros(len(files), dtype = object)
    power = np.zeros(len(files))
    meanspec = np.zeros([len(files), nfft // 2 + 1]) 
    medspec = np.zeros([len(files), nfft // 2 + 1])
    
    ## loop through all the data files
    for i, file in enumerate(files):
        print('%i of %i' % (i, len(files)))
        #tr = obspy.read(file)[0] # UNCOMMENT these lines if using Gem
        try:
            #tr.detrend()
            #tr.filter('highpass', freq = 1)
            #tr = gemlog.deconvolve_gem_response(tr)
        
            tr = riversound.read_audiomoth(file) # COMMENT this if using Gem
        
            ## uncomment these lines if trimming a long file to a shorter length
            t1 = tr.stats.starttime.replace(hour = start_hour, minute = 0, second = 0)
            tr.trim(t1, t1 + 3600*(end_hour - start_hour))
            
            start_times[i] = tr.stats.starttime.datetime
            plot_times[i] = tr.stats.starttime.datetime.replace(hour=0)
            spec_info = riversound.spectrum(tr, nfft = nfft)
            freqs = spec_info['freqs']
            medspec[i,:] = spec_info['median']
            meanspec[i,:] =  spec_info['mean']
            power[i] = np.sum(spec_info['mean']) * np.diff(freqs)[0] # integral spec * df
        except:
            pass
    
    return plot_times, power, freqs, meanspec

#%%

# Graph/Spectrogram Function

def spectrogram(plot_times,power,freqs,meanspec,title,discharge1,discharge2):
    ## plot the spectrogram and power
    plt.figure()
    plt.suptitle(title, fontsize=30)
    
    plt.subplot(3,1,1) # Discharge data
    t,q = riversound.read_discharge('glenwood',discharge1,discharge2)
    weekday2021S(plot_times,interp_times(plot_times, t, q)) # Change based on schedule
    plt.legend(['Wave/Hole','Green Wave'],prop={'size': 15}) # Change based on schedule
    plt.plot(plot_times,interp_times(plot_times, t, q))
    plt.xlim(plot_times[0], plot_times[-1])
    plt.ylabel('Discharge (m$^3$/s)',fontsize=23)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=21)
    
    plt.subplot(3,1,2) # Power data
    weekday2021S(plot_times,power*10**4) # Change based on schedule
    plt.plot(plot_times, power*10**4) 
    plt.ylabel('Power (Pa$^{2}*10^{-4}$)',fontsize=23)
    plt.xlim(plot_times[0], plot_times[-1])
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=21)
    
    plt.subplot(3,1,3) # Frequency data
    w = freqs < 10000
    riversound.image(np.log10(meanspec[:,w] + 0.1 * np.quantile(meanspec, 0.95)), plot_times, freqs[w], crosshairs = False, log_y = False)
    #riversound.image(np.log10(meanspec + 0.001 * np.quantile(meanspec, 0.95)), plot_times, freqs, crosshairs = False, log_y = False)
    #plt.ylim([10,max(freqs)])
    plt.ylabel('Frequency (Hz)',fontsize=23)
    plt.xlim(plot_times[0], plot_times[-1])
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=21)
    
    return t,q

#%%

# Weekday Functions

def weekday2016Spring(plot_times,y_value):
    x = [x.isoweekday() for x in plot_times]
    col =[]
    shp =[]
    
    for i in range(0, len(x)):
        if x[i] == 2:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        elif x[i] == 4:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        elif x[i] == 6:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        else:
            col.append('magenta') 
            shp.append('o')
            print(plot_times[i],'is Green Wave')
    
    # Adjust for any alternating Sundays (manually)    
    col[12] = 'blue'
    shp[12] = '^'
    print(plot_times[12],'is Wave/Hole')
    
    print('-- End of Data Section --')
            
    for i in range(len(plot_times)):
        plt.scatter(plot_times[i],y_value[i], c = col[i], marker = shp[i], s = 120, linewidth = 0)
        #plt.legend(['Green Wave','_nolegend_','Wave/Hole'],prop={'size': 15})
    return

def weekday2021S(plot_times,y_value):
    x = [x.isoweekday() for x in plot_times]
    col =[]
    shp =[]
    
    for i in range(0, len(x)):
        if x[i] == 1:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        elif x[i] == 4:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        elif x[i] == 6:
            col.append('blue')
            shp.append('^')
            print(plot_times[i],'is Wave/Hole')
        else:
            col.append('magenta') 
            shp.append('o')
            print(plot_times[i],'is Green Wave')
            
    print('-- End of Data Section --')
            
    for i in range(len(plot_times)):
        plt.scatter(plot_times[i],y_value[i], c = col[i], marker = shp[i], s = 120, linewidth = 0)
        #plt.legend(['Wave/Hole','Green Wave'],prop={'size': 15})
    return

def weekday2022W(plot_times):
    x = [x.isoweekday() for x in plot_times]
    
    # need to copy/paste/test
    return

#%%

# Select Files Used for Graphing

#path_pattern = '/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/mseed/2021-05-[123]*149*' # change to the files you want to read
path_pattern = 'C:/Users/ttatu/Desktop/Whitewater Park Data/Infrasound Compliation/Infrasound Comp/May 17th to June 7th/*.mseed' # change to the files you want to read
fn = sorted(glob.glob(path_pattern))
    
#%%
    
## UNCOMMENT IF USING GEM DATA
[plot_times, power, freqs, meanspec] = infrasound(fn)

## UNCOMMENT IF USING AUDIO DATA
#[plot_times, power, freqs, meanspec] = audiodata(fn)

#%%

## GRAPHS DATA
# NOTE: Make sure you change the name of the function 
# within with proper weekday schedule
[t,q] = spectrogram(plot_times, power, freqs, meanspec, 'Infrasound Data from May/June 2021',"2021-05-17","2021-06-07")

#%%

## plot discharge vs sound power
plt.figure()
plt.loglog(interp_times(plot_times, t, q), power, 'b.') # can sub banded power to display different
plt.xlabel('Discharge (m$^3$/s)')
plt.ylabel('Power (Pa$^2$)')

## plot discharge vs infrasound and audible peak frequencies
plt.figure()
plt.loglog(interp_times(plot_times, t, q), riversound.find_peak_freq(meanspec, freqs, 13), 'b.')
plt.xlabel('Discharge (m$^3$/s)')
plt.ylabel('Peak Frequency (Hz)')