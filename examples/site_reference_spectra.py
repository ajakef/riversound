import riversound, glob, obspy, matplotlib, datetime, os, gemlog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

write_data = False

output_data_path = os.path.realpath(os.path.join(riversound.__path__[0], '../data/reference_spectra'))

############################
output_file = 'trail_creek_low_2021-10-10.txt' ### Trail Creek low flow (October)
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/mseed/2021-10-10T00_00_00..191..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-10-10/AM005/20211010_090000.WAV'
t1 = obspy.UTCDateTime('2021-10-10T09:00:00')
t2 = obspy.UTCDateTime('2021-10-10T11:00:00')

trailcreek_low = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
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

plt.loglog(trailcreek_high['freqs'], trailcreek_high['spectrum'], label = 'TC_high')
plt.loglog(trailcreek_low['freqs'], trailcreek_low['spectrum'], label = 'TC_low')
plt.loglog(tahquamenon['freqs'], tahquamenon['spectrum'], label = 'TQ')
plt.loglog(wwp_p2_1['freqs'], wwp_p2_1['spectrum'], label = 'WWP_P2_1')
plt.loglog(annmorrison['freqs'], annmorrison['spectrum'], label = 'AM')
plt.loglog(eckert['freqs'], eckert['spectrum'], label = 'Eckert')
plt.loglog(diversiondam['freqs'], diversiondam['spectrum'], label = 'DD')
plt.loglog(wwp['freqs'], wwp['spectrum'], label = 'WWP')
plt.loglog(con1e['freqs'], con1e['spectrum'], label = 'C1E')
plt.loglog(MRBD['freqs'], MRBD['spectrum'], label = 'MRBD')
plt.legend()
plot_noise_specs()

