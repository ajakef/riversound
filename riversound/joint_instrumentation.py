import glob, obspy
import numpy as np
from riversound.wav import read_audiomoth
import matplotlib.pyplot as plt

def read_infrasound_audible(t1, t2, path_infrasound, path_audible):
    """
    For a given start and end time, read both an infrasound miniSEED file and audible .WAV file.

    Parameters:
    -----------
    t1 : obspy.UTCDateTime
    Start time of output data

    t2 : obspy.UTCDateTime
    End time of output data

    path_infrasound : str
    Folder that contains infrasound mseed data

    path_audible : str
    Folder that contains audible .WAV data

    Returns:
    --------
    obspy.Stream, where the first trace is infrasound and the second trace is audible
    
    Example:
    --------
    ## run from main riversound folder (the one that includes 'data')
    import obspy
    from riversound import read_infrasound_audible

    t1 = obspy.UTCDateTime('2021-04-14 06:00:00')
    t2 = obspy.UTCDateTime('2021-04-14 07:00:00')
    path_infrasound = 'data/mseed'
    path_audible = 'data/audiomoth'
    
    ## you can set the output this way to be explicit about which trace is which 
    tr_infrasound, tr_audible = read_infrasound_audible(t1, t2, path_infrasound, path_audible)

    ## or set the outputs this way to package both traces in one stream
    st = read_infrasound_audible(t1, t2, path_infrasound, path_audible)
    """
    breakpoint()
    ## download the instrument response from the IRIS Nominal Response Library
    from obspy.clients.nrl import NRL
    nrl = NRL()
    gem_response = nrl.get_response(sensor_keys = ['Gem', 'Gem Infrasound Sensor v1.0'],
	   		    datalogger_keys = ['Gem', 'Gem Infrasound Logger v1.0',
			    '0 - 128000 counts/V']) # may cause warning--ok to ignore
    
    eps = 1e-6
    t1 = obspy.UTCDateTime(t1)
    t2 = obspy.UTCDateTime(t2) - eps
    fn_infrasound = sorted(glob.glob(path_infrasound + '/*mseed'))
    fn_audible = sorted(glob.glob(path_audible + '/*WAV'))

    if len(fn_infrasound) == 0:
        print('No infrasound files found in path %s' % path_infrasound)
    if len(fn_audible) == 0:
        print('No audible files found in path %s' % path_audible)

    file_start_infrasound = [_find_file_start(filename) for filename in fn_infrasound]
    file_start_audible = [_find_file_start(filename) for filename in fn_audible]
    file_end_guess_infrasound = file_start_infrasound[1:] + [obspy.UTCDateTime('9999-12-31')]
    file_end_guess_audible = file_start_audible[1:] + [obspy.UTCDateTime('9999-12-31')]

    st_infrasound = obspy.Stream()
    for i in range(len(fn_infrasound)):
        if (file_start_infrasound[i] <= t2) and (file_end_guess_infrasound[i] >= t1):
            st_infrasound += obspy.read(fn_infrasound[i])[0]
    st_infrasound.trim(t1, t2, nearest_sample = False)
    st_infrasound.merge()
    for tr in st_infrasound:
        tr.stats.response = gem_response
    st_infrasound.remove_response()


    st_audible = obspy.Stream()
    for i in range(len(fn_audible)):
        if (file_start_audible[i] < t2) and (file_end_guess_audible[i] > t1):
            st_audible += read_audiomoth(fn_audible[i], remove_response = True)
    st_audible.trim(t1, t2, nearest_sample = False)
    ## definitely don't merge the audible traces if you record 30-sec files every hour!
    
    if len(st_infrasound) == 0:
        print('No infrasound files found for these times')
    if len(st_audible) == 0:
        print('No audible files found for these times')
        
    return(st_infrasound + st_audible)

## Helper function to find a data file's start time from its file name.
def _find_file_start(filename):
    return obspy.UTCDateTime(filename.split('/')[-1].split('.')[0])

