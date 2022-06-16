# for linux, need to install simpleaudio's dependency with sudo apt-get install -y python3-dev libasound2-dev
import sys # should always be available, doesn't need to be in "try"
try:
    import numpy as np
    import os, glob, getopt, logging, traceback, platform
    import riversound, obspy
except Exception as e:
    print('Either dependencies are missing, or the environment is not active')
    print('Error message:')
    print(e)
    sys.exit(2)

try:
    import simpleaudio
except Exception as e:
    print('Dependency package "simpleaudio" cannot be imported')
    print('Error message:')
    print(e)
    sys.exit(2)

allowed_sample_rates = [8000, 11025, 16000, 22050, 24000, 32000, 44100, 48000, 88200, 96000, 192000]

def print_call():
    print('play_data -i <input_file> -s <speedup> -l <low_cutoff_freq> -t <trace_number>')
    print('-i --input_file: required')
    print('-s --speedup: factor to speed up data in recording (default 100)')
    print('-l --low_cutoff_freq: default 1 (Hz)')
    print('-t --trace_number: if input file has multiple traces, which to convert (default 0)')
    print('-h --help: print this message')
    print('')
    print('Note: low_cutoff_freq * speedup should be greater than 20 to prevent inaudible')
    print('frequencies from dominating the output')


def main(argv = None):
    if argv is None:
        argv = sys.argv[1:]
    input_file = None
    trace_number = 0
    test = False
    speedup = None
    low_cutoff_freq = 1
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:l:",[])
    except getopt.GetoptError:
        print_call()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_call()
            sys.exit()
        elif opt in ("-i", "--input_file"):
            input_file = arg
        elif opt in ("-s", "--speedup"):
            speedup = float(arg)
        elif opt in ("-l", "--low_cutoff_freq"):
            low_cutoff_freq = float(arg)
        elif opt in ("-t", "--trace_number"):
            trace_number = arg

    if input_file is None:
        raise Exception('input_file must be provided (-i, --input_file)')
        print("")
        print_call()
        sys.exit()

    ## read the input file (could be either seismic or wav)
    try:
        tr = obspy.read(input_file)[trace_number] # works for mseed, sac, etc
    except:
        try:
            tr = riversound.read_audiomoth(input_file)
        except:
            print("Could not open input data file " + input_file + ".")
            sys.exit()
            
    # in-place operations to make the data playable
    tr.detrend()
    tr.filter('highpass', freq = low_cutoff_freq)
    tr.normalize() 
    
    play_tr(tr, speedup)


def play_tr(tr, speedup = None, low_cutoff_freq = 1):
    """
    Play an obspy Trace as audio
    
    Parameters:
    -----------
    tr: data to play as audio (obspy.Trace; if obspy.Stream is given, plays the first Trace)
    speedup: factor by which data is sped up in playback compared to original sample rate.
    low_cutoff_freq: frequency to filter above
    
    Returns: None

    Notes:
    -----
    play_tr uses the sample rate in tr to guess whether it's infrasound or audible. If infrasound,
    the default is to speed up by 128 (7 octaves). If audible, default is to not speed up at all.

    low_cutoff_freq * speedup should be greater than 20 to prevent inaudible frequencies from 
    dominating the output


    See also: play_signal (to play a numpy.array instead of an obspy.Trace)
    """
    if type(tr) is obspy.Stream:
        tr = tr[0]
    elif type(tr) is np.array:
        raise TypeError('tr must be an obspy.Trace, not a numpy.array. Consider play_signal()')
    elif type(tr) is not obspy.Trace:
        raise TypeError('tr must be an obspy.Trace')

    if speedup is None:
        if tr.stats.sampling_rate >= 8000: ## assumed audio data
            speedup = 1
        else:
            speedup = 128 ## infrasound

    ## detrend and high-pass filter ensures the output signal is actually audible
    tr.detrend()
    tr.filter('highpass', freq = low_cutoff_freq)

    ## speed up the data
    tr.stats.sampling_rate = tr.stats.sampling_rate * speedup

    ## only certain sample rates are allowed; resample to the lowest sample rate above current value
    ## this won't change any pitches
    w = np.where(np.array(allowed_sample_rates) >= (tr.stats.sampling_rate*0.99))[0][0]
    tr.resample(allowed_sample_rates[w])

    play_signal(tr.data, tr.stats.sampling_rate)

def play_signal(signal, sample_rate = 8000):
    """
    Play a signal as audio
    
    Parameters:
    -----------
    signal: data to play as audio (array-like)
    sample_rate: rate (Hz) at which data should be played; see note for allowable values

    Returns: None

    Note: only certain sample rates are supported. In Hz: [8000, 11025, 16000, 22050, 24000, 32000, 
    44100, 48000, 88200, 96000, 192000]

    See also: play_tr to play an obspy.Trace
    """

    try:
        signal = np.array(signal)
    except:
        raise TypeError("'signal' must be numpy array or convertible to numpy array (e.g., a list)")

    sample_rate = int(sample_rate)
    if sample_rate not in allowed_sample_rates:
        raise Exception('sample_rate must be [8,11.025,16,22.05,24,32,44.1,48,88.2,96,192] kHz')
    
    ## convert y to 16-bit ints spanning the full range
    signal = (signal / np.max(np.abs(signal) + 1e-12) * (2**15 - 1)).astype(np.int16)

    # Start playback
    play_obj = simpleaudio.play_buffer(signal, 1, 2, int(sample_rate))

    # Wait for playback to finish before exiting
    play_obj.wait_done()





if __name__ == "__main__":
   main(sys.argv[1:])
