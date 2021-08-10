from scipy.io import wavfile
import numpy as np
import obspy

def write_wav(tr, filename = None, time_format = '%Y-%m-%dT%H_%M_%S', path = '.'):
    if filename is None:
        datetime_str = tr.stats.starttime.strftime(time_format)
        s = tr.stats
        station_str = '%s.%s.%s.%s' % (s.network, s.station, s.location, s.channel)
        filename = datetime_str + '.' + station_str + '.wav'
    ## need to ensure that the data is either integers, or float from -1 to 1
    if tr.data.dtype == 'float':
        ref = np.abs(tr.data).max()
        if ref > 0:  ## prevent divide-by-zero
            tr.data /= ref
    ## sample rate must be an int
    if int(tr.stats.sampling_rate) != tr.stats.sampling_rate:
        raise TypeError('sample rate must be an integer')
    wavfile.write(path + '/' + filename, int(tr.stats.sampling_rate), tr.data)


def read_audiomoth(filename, network = '', station = '', location = '', channel = 'GDF'):
    # channel code: G means sample rate 1000-5000 Hz, corner period < 10 sec. This is the closest SEED code allowed; it does not support fs > 5000 Hz.
    datetime_str = filename.split('/')[-1].split('\\')[-1].split('.')[0]
    #(date_str, time_str) = datetime_str.split('_')
    #starttime = obspy.UTCDateTime(date_str[0:4] + '-' + date_str[4:6] + '-' + date_str[6:8] + \
    #                              'T' + time_str[0:2] + ':' + time_str[2:4] + ':' + time_str[4:6])
    starttime = obspy.UTCDateTime(datetime_str)
    samplerate, data = wavfile.read(filename)
    tr = obspy.Trace(data)
    tr.stats.sampling_rate = samplerate
    tr.stats.starttime = starttime
    tr.stats.network = network
    tr.stats.station = station
    tr.stats.location = location
    return tr

    
#tr = read_audiomoth('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-05-05_AnnMorrison/AM003/20210505_090000.WAV')
#tr.trim(tr.stats.starttime, tr.stats.starttime + 1)
#tr.spectrogram(log = True, dbscale = True)
