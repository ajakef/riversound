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

def print_call():
    print('convert_wav -i <input_file> -s <speedup> -o <output_file> -l <low_cutoff_freq>')
    print('-i --input_file: required')
    print('-s --speedup: factor to speed up data in recording (default 100)')
    print('-o --output_file: default input_file.wav. If dir, writes to output_file/input_file.wav')
    print('-t --trace_number: if input file has multiple traces, which to convert (default 0)')
    print('-l --low_cutoff_freq: default 1 (Hz)')
    print('-h --help: print this message')
    print('')
    print('Note: low_cutoff_freq * speedup should be greater than 20 to prevent inaudible')
    print('frequencies from dominating the output')


def main(argv = None):
    if argv is None:
        argv = sys.argv[1:]
    input_file = None
    output_file = None
    trace_number = 0
    test = False
    speedup = 100
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
        elif opt in ("-o", "--output_file"):
            output_file = arg
        elif opt in ("-t", "--trace_number"):
            trace_number = arg

    if input_file is None:
        raise Exception('input_file must be provided (-i, --input_file)')
        print("")
        print_call()
        sys.exit()
#    try:
#        fn = os.listdir(input_file)
#    except:
#        print("Could not open input data file " + input_file + ".")
#        sys.exit()

    if output_file is None:
        output_file = input_file + '.wav'
    elif os.path.isdir(output_file):
        output_file = os.path.join(output_file, os.path.split(input_file)[-1] + '.wav')
            
    ## actually run the conversion now
    tr = obspy.read(input_file)[trace_number]

    # in-place operations to make the data playable
    tr.detrend()
    tr.filter('highpass', freq = low_cutoff_freq)
    tr.normalize() 
    
    tr.stats.sampling_rate = int(tr.stats.sampling_rate * speedup)
    riversound.write_wav(tr, output_file)
    print('')
    print('Wrote wav file %s, filtered above %.2f Hz, sped up by factor of %.1f' % (output_file, low_cutoff_freq, speedup))
    print('')
    
if __name__ == "__main__":
   main(sys.argv[1:])
