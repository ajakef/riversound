import riversound, glob, obspy, matplotlib, datetime, os, gemlog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

output_data_path = os.path.realpath(os.path.join(riversound.__path__[0], '../data/reference_spectra'))

############################
output_file = 'trail_creek_low_2021-10-10.txt' ### Trail Creek low flow (October)
infrasound_file = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-10-10/mseed/2021-10-10T00_00_00..191..HDF.mseed'
audible_file = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-10-10/AM005/20211010_090000.WAV'
t1 = obspy.UTCDateTime('2021-10-10T09:00:00')
t2 = obspy.UTCDateTime('2021-10-10T11:00:00')

trailcreek_low = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
trailcreek_low.to_csv(os.path.join(output_data_path, output_file), index = False)

###########################
output_file = 'trail_creek_high_2021-05-16.txt' ### Trail Creek high flow (May)
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-05-17/mseed/2021-05-16T00_00_00..101..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/TrailCreek/2021-05-17/AM006/20210516_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-16T09:00:00')
t2 = obspy.UTCDateTime('2021-05-16T11:00:00')

trailcreek_high = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
trailcreek_high.to_csv(os.path.join(output_data_path, output_file), index = False)

###########################
output_file = 'tahquamenon_2021-08-02.txt' ### Upper Tahquamenon Falls, 2021-08-02
infrasound_file = '/data/jakeanderson/2021_Boise_River/short_term/2021-08-02_UpperTahquamenonFalls_Michigan/mseed/2021-08-02T20_10_09..191..HDF.mseed'
audible_file =  '/data/jakeanderson/2021_Boise_River/short_term/2021-08-02_UpperTahquamenonFalls_Michigan/audio/20210802_201009.WAV'
t1 = obspy.UTCDateTime('2021-08-02T20:10:28')
t2 = obspy.UTCDateTime('2021-08-02T20:11:49')

tahquamenon = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
tahquamenon.to_csv(os.path.join(output_data_path, output_file), index = False)

##############################
output_file = 'WWP_P2_1_2021-06-14.txt' ### Phase 2 of WWP, first wave (double black diamond)
infrasound_file = '/data/jakeanderson/2021_Boise_River/short_term/2021-06-14_wwp_wave2/mseed/*160*'
audible_file =  '/data/jakeanderson/2021_Boise_River/short_term/2021-06-14_wwp_wave2/Audiomoth/000/19700101_030441.WAV'
t1 = obspy.UTCDateTime('2021-01-02T20:10:28')
t2 = obspy.UTCDateTime('2021-12-02T20:11:49')

wwp_p2_1 = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
wwp_p2_1.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'AnnMorrison_2021-04-27_2021-05-01.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/AnnMorrison/mseed/2021-04-27T00_00_00..150..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/AnnMorrison/AM003/20210501_090000.WAV'
t1 = obspy.UTCDateTime('2021-01-02T20:10:28')
t2 = obspy.UTCDateTime('2021-12-02T20:11:49')

annmorrison = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
annmorrison.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'Eckert_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/Eckert/mseed/2021-05-24T00_00_00..119..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/Eckert/AM004_all/20210524_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

eckert = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
eckert.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'DiversionDam_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/DivDam/mseed_093_all/2021-05-24T00_00_00..093..HDF.mseed'
audible_file = '/data/jakeanderson/2021_Boise_River/long_term/DivDam/AM005_all/20210524_090000.WAV'
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

diversiondam = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
diversiondam.to_csv(os.path.join(output_data_path, output_file), index = False)

#############################
output_file = 'WWP_2021-05-24.txt' ### 
infrasound_file = '/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/mseed/2021-05-24T00_00_00..148..HDF.mseed'
audible_file =  glob.glob('/data/jakeanderson/2021_Boise_River/long_term/WhitewaterPark/Audiomoth*/20210524_090000.WAV')[0]
t1 = obspy.UTCDateTime('2021-05-24T09:00:00')
t2 = obspy.UTCDateTime('2021-05-24T10:00:00')

wwp = riversound.site_reference_spectrum(infrasound_file, audible_file, t1, t2)
wwp.to_csv(os.path.join(output_data_path, output_file), index = False)

plt.loglog(trailcreek_high['freqs'], trailcreek_high['spectrum'])
plt.loglog(trailcreek_low['freqs'], trailcreek_low['spectrum'])
plot_noise_specs()

