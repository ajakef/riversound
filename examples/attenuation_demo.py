import numpy as np
import matplotlib.pyplot as plt
import riversound
from numpy.random import uniform

def dewpoint_to_rel_humidity(dewpoint_C, temp_C):
    return 100 * ((112 - 0.1*temp_C + dewpoint_C) / (112 + 0.9*temp_C))**8

## Monte Carlo for atmospheric attenuation shows that distance and frequency are the main determinants; increases in any of those reduce amplitude. Temperature and humidity have significant effects but they're complicated. Pressure has very little effect.
## If we use 50% energy loss (3 dB) as the criterion, 1-2 kHz are fine up to 50 m, 5 kHz is safe up to 30 m, and 10 kHz is only safe to about 10 m distance.
N = 500

freqs = np.arange(20000)
distance = np.zeros(N)
temperature = np.zeros(N)
pressure = np.zeros(N)
dewpoint = np.zeros(N)
rel_humidity = np.zeros(N)
spectrum = np.zeros([N, len(freqs)])

for i in range(N):
    distance[i] = 5 * 10**uniform(0, 1, 1) # log-uniform from 5-50 m
    temperature[i] = uniform(-10, 40, 1)
    pressure[i] = uniform(91800, # Boise
                       75300, # 8000 ft in Sawtooths
                       1)
    # Average monthly dewpoint ranges from 7 F (winter) to 34 F (summer) below average temperature in Boise.
    # This is a more stable humidity measure than RH (which anti-correlates with temp)
    # https://www.timeanddate.com/weather/usa/boise/climate
    dewpoint_diff = (20+temperature[i])/60 * uniform(5, 35, 1)
    dewpoint[i] = temperature[i] - dewpoint_diff
    rel_humidity[i] = dewpoint_to_rel_humidity(dewpoint[i], temperature[i])
    spectrum[i,:] = riversound.attenuation_power_spectrum(freqs, distance[i], temperature[i], pressure[i], rel_humidity[i])
    plt.loglog(freqs, spectrum[i,:])

plt.loglog(freqs[4000:], (freqs[4000:]/4000)**(-5/3), 'k-') 
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectrum Multiplier')

## Check that the temperature-humidity distribution is realistic
plt.figure()
plt.subplot(1,2,1)
plt.plot(temperature, dewpoint, 'k.')
plt.plot(temperature, temperature)
plt.xlabel('Temperature (C)')
plt.ylabel('Dew Point (C)')
plt.title('Dewpoint vs Temperature')
plt.subplot(1,2,2)
plt.plot(temperature, rel_humidity, 'k.')
plt.xlabel('Temperature (C)')
plt.ylabel('Relative Humidity (%)')
plt.title('Dewpoint vs Relative Humidity')

## study specific frequencies; plot their attenuation coefficient as histograms
s10k = spectrum[:,10000]
s5k = spectrum[:,5000]
s2k = spectrum[:,2000]
s1k = spectrum[:,1000]

plt.figure()
plt.hist(s10k)
plt.hist(s5k)
plt.hist(s2k)
plt.hist(s1k)

## calculate the log-log slopes of the spectra at specific frequencies
slope10k = np.log10(spectrum[:,10000]/spectrum[:,9999]) / np.log10(freqs[10000]/freqs[9999])
slope5k = np.log10(spectrum[:,5000]/spectrum[:,4999]) / np.log10(freqs[5000]/freqs[4999])
slope2k = np.log10(spectrum[:,2000]/spectrum[:,1999]) / np.log10(freqs[2000]/freqs[1999])
slope1k = np.log10(spectrum[:,1000]/spectrum[:,999]) / np.log10(freqs[1000]/freqs[999])


############################################
## plot effects of atmospheric properties on attenuation
def plot_panel(x,y, xlabel, ylabel = 'Power Spec Mult (10 m, dB)'):
    y = 10*np.log10(y)
    plt.plot(x, y, 'c.')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, b + m*x, 'r-')
    plt.text(x.min(), y.min()*1.1, 'y = %0.3f x + %0.3f; r = %0.2f' % (m, b, np.corrcoef(x,y)[0,1]))
    plt.ylim([y.min()*1.1, y.max()])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot_all_panels(s):
    plt.figure()
    plt.subplot(2,2,1)
    plot_panel(dewpoint, s ** (10/distance), 'Dew Point')

    plt.subplot(2,2,2)
    plot_panel(pressure/1000, s ** (10/distance), 'Pressure (kPa)', '')

    plt.subplot(2,2,3)
    plot_panel(temperature, s ** (10/distance), 'Temperature (C)')

    plt.subplot(2,2,4)
    plot_panel(distance, s, 'Distance (m)', 'Total Power Mult (dB)')

    plt.tight_layout()

plot_all_panels(s1k)## 1 kHz
plot_all_panels(s2k)## 2 kHz
plot_all_panels(s5k)## 5 kHz
plot_all_panels(s10k)## 10 kHz
