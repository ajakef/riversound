import numpy as np
import matplotlib.pyplot as plt
import obspy
from scipy.signal import spectrogram
from scipy.ndimage import median_filter
from scipy.stats import kurtosis, skew
from scipy.stats import moment

## test to see which moments are useful for detecting windy data. Turns out skewness does nothing but all higher moments detect it; kurtosis does the best and is also simplest.
#%%
## normal distribution moments for even numbers are the products of all preceding odd numbers: 1, 3, 15, 105, etc.
## the moment function is the same as skew and kurtosis if you standardize the variable first and then subtract the expected value (0 or 3)
st = obspy.read('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-04-10_AnnMorrison/mseed/2021-04-01T00_00_00..150..HDF.mseed')
st.filter('highpass', freq = 5.0)
t1 = obspy.UTCDateTime('2021-04-01T08:00:00')
st.trim(t1, t1 + 3*3600)


m2  = np.zeros(1000)
m3 = np.zeros(1000)
m4  = np.zeros(1000)
m5  = np.zeros(1000)
m6 = np.zeros(1000)
m7 = np.zeros(1000)
m8 = np.zeros(1000)
for i in range(1000):
    j1 = i*1000
    x = st[0].data[j1:(j1+1000)]
    m2[i] = (np.var(x))
    x = (x - x.mean()) / np.std(x)
    m3[i] = (skew(x))
    m4[i] = (kurtosis(x))
    m5[i] = (moment(x, 5))
    m6[i] = (moment(x, 6))
    m7[i] = (moment(x, 7))
    m8[i] = (moment(x, 8))
w = (np.array(m4) < (-1 * np.quantile(m4, 0.01)))    
plt.subplot(2,2,1); plt.plot(m3[w], m2[w], ',')
plt.subplot(2,2,2); plt.plot(m4[w], m2[w], ',')
plt.subplot(2,2,3); plt.plot(m5[w], m2[w], ',')
plt.subplot(2,2,4); plt.plot(m6[w], m2[w], ',')

for i, x in enumerate([m3, m4, m5, m6, m7, m8]):
    print('moment %i' % (i+3))
    print(np.corrcoef(m2, x)[0,1]) # pick an off-diagonal from the correlation matrix
    print(np.corrcoef(m2[w], x[w])[0,1])
