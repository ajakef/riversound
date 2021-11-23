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


def read_audiomoth(filename, network = '', station = '', location = '', channel = 'GDF', remove_response = True):
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

    if remove_response:
        # following VERY ROUGH sensitivity estimate taken from assumptions below
    ## need to replace this with a real response
        #adc_bitweight = 1.25/2**12
        #gain = 10**(30.6/20)
        #mic_sensitivity = 10**(-38/20)
        #pa_per_count = adc_bitweight / (gain * mic_sensitivity) * 0.03
        #tr.data = tr.data * pa_per_count
        tr.stats.response = response_audiomoth_20211119
        tr.remove_response()

    return tr


## audiomoth response:
# Wonder Gecko ADC (p.886): 12-bit (?), full scale is probably 1.25 or 2.5 V https://www.silabs.com/documents/public/reference-manuals/EFM32WG-RM.pdf
# pre-amp gain in dB (what you set in config): low 27.2 mid 30.6 high 32.0 https://raw.githubusercontent.com/OpenAcousticDevices/Datasheets/main/AudioMoth_Dev_Datasheet.pdf
# above conflicts with this: https://www.openacousticdevices.info/support/configuration-support/how-many-db-audiomoth-records-high-gain-mode
# mic sensitivity: -38 dBV/Pa https://raw.githubusercontent.com/OpenAcousticDevices/Datasheets/main/AudioMoth_Dev_Datasheet.pdf
#tr = read_audiomoth('/home/jake/Work/StreamAcoustics/BoiseRiver/2021_data/2021-05-05_AnnMorrison/AM003/20210505_090000.WAV')


#tr.trim(tr.stats.starttime, tr.stats.starttime + 1)
#tr.spectrogram(log = True, dbscale = True)

## response from 2021-11-19 calibration
## correct claimed audiomoth sensitivity: https://www.openacousticdevices.info/support/device-support/calibration-for-sound-pressure-level-measurement
sens_mic = 10**(-18/20) # -18 dBV/Pa, which includes a built-in gain of 20 dB (https://media.digikey.com/pdf/Data%20Sheets/Knowles%20Acoustics%20PDFs/SPM0408LE5H-TB.pdf)
gain_preamp = 15 # med gain
bitweight_V = 3.3/(2**16-1) # Volts per count
      
poles = [48*6.28, 100*6.28]
zeros = [0,0]

## gain adjustment of 0.7 determined by trial and error in this calibration
response_audiomoth_20211119 = obspy.core.inventory.response.Response()
response_audiomoth_20211119 = response_audiomoth_20211119.from_paz(
    zeros,
    poles,
    stage_gain = 0.7 / (bitweight_V/(sens_mic * gain_preamp)),
    stage_gain_frequency=300.0,
    input_units='M/S',
    output_units='VOLTS',
    normalization_frequency=300.0
    )
