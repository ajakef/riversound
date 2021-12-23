import riversound, glob, obspy, matplotlib, datetime, os, gemlog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

write_data = True

output_data_path = os.path.realpath(os.path.join(riversound.__path__[0], '../data/reference_spectra'))

############################
output_file = 'trail_creek_low_2021-10-10.txt' ### Trail Creek low flow (October)
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/mseed/2021-10-10T00_00_00..191..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/AM005/20211010_090000.WAV'
t1 = obspy.UTCDateTime('2021-10-10T09:00:00')
t2 = obspy.UTCDateTime('2021-10-10T11:00:00')

trailcreek_low = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2, window = 'mcnamara')
if write_data:
    trailcreek_low.to_csv(os.path.join(output_data_path, output_file), index = False)

###########################
output_file = 'trail_creek_high_2021-05-16.txt' ### Trail Creek high flow (May)
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-05-17/mseed/2021-05-16T09_00_00..101..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-05-17/AM006/20210516_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-16T09:00:00')
t2 = obspy.UTCDateTime('2021-05-16T11:00:00')

trailcreek_high = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    trailcreek_high.to_csv(os.path.join(output_data_path, output_file), index = False)

###########################
output_file = 'tahquamenon_2021-08-02.txt' ### Upper Tahquamenon Falls, 2021-08-02
infrasound_file = '/data/jakeanderson/2021_Boise_River/short_term/2021-08-02_UpperTahquamenonFalls_Michigan/mseed/2021-08-02T20_10_09..191..HDF.mseed'
audible_file =  '/data/jakeanderson/2021_Boise_River/short_term/2021-08-02_UpperTahquamenonFalls_Michigan/audio/20210802_201009.WAV'
t1 = obspy.UTCDateTime('2021-08-02T20:10:28')
t2 = obspy.UTCDateTime('2021-08-02T20:11:49')

tahquamenon = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    tahquamenon.to_csv(os.path.join(output_data_path, output_file), index = False)

##############################
output_file = 'WWP_P2_1_2021-06-14.txt' ### Phase 2 of WWP, first wave (double black diamond)
infrasound_file = '/data/jakeanderson/2021_Boise_River/short_term/2021-06-14_wwp_wave2/mseed/*160*'
audible_file =  '/data/jakeanderson/2021_Boise_River/short_term/2021-06-14_wwp_wave2/Audiomoth/000/19700101_030441.WAV' # wonky date from lost real time clock
t1 = obspy.UTCDateTime('1900-01-02T20:10:28') # accommodate wonky date
t2 = obspy.UTCDateTime('2021-12-02T20:11:49')

wwp_p2_1 = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    wwp_p2_1.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'AnnMorrison_2021-04-27_2021-05-01.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/AnnMorrison/mseed/2021-04-27T00_00_00..150..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/AnnMorrison/AM003/20210501_090000.WAV'
t1 = obspy.UTCDateTime('2021-01-02T20:10:28')
t2 = obspy.UTCDateTime('2021-12-02T20:11:49')

annmorrison = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    annmorrison.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'Eckert_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/Eckert/mseed/2021-05-24T00_00_00..119..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/Eckert/AM004_all/20210524_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

eckert = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    eckert.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'DiversionDam_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/DivDam/mseed_093_all/2021-05-24T00_00_00..093..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/DivDam/AM005_all/20210524_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

diversiondam = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    diversiondam.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'WWP_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/mseed/2021-05-24T00_00_00..148..HDF.mseed'
audible_file =  glob.glob('/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/Audiomoth*/20210524_090000.WAV')[0]
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

wwp = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    wwp.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'Con1E_2021-04-18.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/CON1E_DCEW/mseed_all/2021-04-18T00_00_00..128..HDF.mseed'
audible_file =  '/data/jakeanderson/2021_Boise_River/long_term/CON1E_DCEW/audio_all/20210418_090000.WAV'
t1 = obspy.UTCDateTime('2021-04-18T09:00:00')
t2 = obspy.UTCDateTime('2021-04-18T10:00:00')

con1e = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    con1e.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'MRBD_2021-09-13.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/MRBD_Michigan/mseed_all/2021-09-12T00_00_00..191..HDF.mseed'
audible_file =  '/data/jakeanderson/2021_Boise_River/long_term/MRBD_Michigan/audio_all/20210912_030000.WAV'
t1 = obspy.UTCDateTime('2021-09-12T02:48:00')
t2 = obspy.UTCDateTime('2021-09-12T03:07:00')

MRBD = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
if write_data:
    MRBD.to_csv(os.path.join(output_data_path, output_file), index = False)

######################################################
w = np.where(tahquamenon['freqs'] < 40)[0]
tahquamenon['spectrum'][w] = filtfilt(np.ones(20)/20, 1, tahquamenon['spectrum'][w])
plt.loglog(trailcreek_high['freqs'], trailcreek_high['spectrum'], label = 'TC_high')
plt.loglog(trailcreek_low['freqs'], trailcreek_low['spectrum'], label = 'TC_low')
plt.loglog(tahquamenon['freqs'], tahquamenon['spectrum'], label = 'TQ')
#plt.loglog(wwp_p2_1['freqs'], wwp_p2_1['spectrum'], label = 'WWP_P2_1')
plt.loglog(annmorrison['freqs'], annmorrison['spectrum'], label = 'AM')
plt.loglog(eckert['freqs'], eckert['spectrum'], label = 'Eckert')
plt.loglog(diversiondam['freqs'], diversiondam['spectrum'], label = 'DD')
plt.loglog(wwp['freqs'], wwp['spectrum'], label = 'WWP')
plt.loglog(con1e['freqs'], con1e['spectrum'], label = 'C1E')
plt.loglog(MRBD['freqs'], MRBD['spectrum'], label = 'MRBD')

## plot turbulence power law
ff = np.array([1e-3, 1e5])
plt.loglog(ff, ff**-(5/3), 'k-')
plt.loglog(ff, 1e-6*ff**-(5/3), 'k-')
plt.loglog(ff, 1e-2*ff**-(5/3), 'k-')
plt.legend()
riversound.plot_noise_specs()


plt.loglog(annmorrison['freqs'], annmorrison['q1'])
plt.loglog(annmorrison['freqs'], annmorrison['q3'])



plt.loglog(trailcreek_low['freqs'], trailcreek_low['q1'], label = 'TC_low')
plt.loglog(trailcreek_low['freqs'], trailcreek_low['q3'], label = 'TC_low')


## WWP_P2_1
plt.loglog(wwp_p2_1['freqs'], wwp_p2_1['spectrum'], label = 'WWP_P2_1')
plt.loglog(ff, 10**-1.5*ff**-(5/3), 'k-')
plt.xlim([1, 1e4])
plt.ylim([1e-9, 1e-3])
#https://photos.google.com/share/AF1QipOPfcmaADZo6eFsOd_QuzoWnezfhFDGy5p_m6X-80-oDG6gYj29Nq_l-_8W8N0Zyg/photo/AF1QipM2VCBxi8Pjx4sCRxc_nPjBeO17p0TETo_2IK6y
#https://photos.google.com/share/AF1QipOPfcmaADZo6eFsOd_QuzoWnezfhFDGy5p_m6X-80-oDG6gYj29Nq_l-_8W8N0Zyg/photo/AF1QipPm0dA5uAloZs5abTTR81ReA7UkrM-ZQueXYgtx
#https://photos.google.com/share/AF1QipOPfcmaADZo6eFsOd_QuzoWnezfhFDGy5p_m6X-80-oDG6gYj29Nq_l-_8W8N0Zyg/photo/AF1QipMG06W0droOJica7SVZC9FjQWB8VHbQBLeiu1Sn

## jump up above 40 Hz: DD, TC_high, TC_low
## jump down above 20 Hz: AM, Eckert
## No effect: MRBD

## truncating the infrasound data to just a couple minutes in order to more closely approximate the audible recording period doesn't fix it.
##################################

############################
import riversound, glob, obspy, matplotlib, datetime, os, gemlog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

write_data = False

output_data_path = os.path.realpath(os.path.join(riversound.__path__[0
], '../data/reference_spectra'))

## significant scatter in band-limited power estimates. Spectrum of power estimates appears to be mostly white; weak long-term trends. Correlation between power estimates over different freq bands is negligible at short window lengths (5 sec) and significant at much longer window lengths. Using the McNamara/Buland 2004 window (cosine taper 10% on each side) makes almost no difference except at f << 1.

output_file = 'trail_creek_low_2021-10-10.txt' ### Trail Creek low flow (October)
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/mseed/2021-10-10T00_00_00..191..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/AM005/20211010_090000.WAV'
t1 = obspy.UTCDateTime('2021-10-10T09:00:00')
t2 = obspy.UTCDateTime('2021-10-10T11:00:00')

tr_infrasound = obspy.read('/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/mseed/2021-10-10T00_00_00..191..HDF.mseed')[0]

#def f(x): print(kurtosis(x)); return kurtosis(x) < 0.05
#s_inf = riversound.spectrum(tr_infrasound, criterion_function = f)
s_inf = riversound.spectrum(tr_infrasound, kurtosis_threshold = 0.5, nfft = 2**13)
M = s_inf['specgram']
f = s_inf['freqs']
df = np.diff(f)[0]
p22 = M[(f>22) & (f < 25),:].sum(0) * df
p15 = M[(f>15) & (f < 18),:].sum(0) * df
p35 = M[(f>35) & (f < 38),:].sum(0) * df
w = (~np.isnan(p15)) & (p22 > 1.4) & (p22 < 2.1) & (p15 > 1.9) & (p15 < 2.7)
print([np.quantile(p22[w], 0.75)/np.quantile(p22[w], 0.25), np.quantile(p15[w], 0.75)/np.quantile(p15[w], 0.25), np.quantile(p35[w], 0.75)/np.quantile(p35[w], 0.25)])
print(np.corrcoef(p15[w], p22[w]))
print(np.corrcoef(p15[w], p35[w]))




plt.loglog(p15, p35)
np.corrcoef(p15, p22)
plt.loglog(p15[w], p22[w], 'g,')
