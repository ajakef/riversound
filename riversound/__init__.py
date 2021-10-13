from riversound.wav import read_audiomoth, write_wav
from riversound.spectrum import spectrum, image, apply_function_windows, pgram, find_peak_freq
from riversound.joint_instrumentation import read_infrasound_audible
from riversound.discharge import read_discharge, read_DCEW
from riversound.ref_spectra import site_reference_spectrum, plot_noise_specs
#from gemlog.gemlog import Convert, ReadGem, convert, read_gem, get_gem_specs
#from gemlog.gem_network import summarize_gps, read_gps, SummarizeAllGPS, make_gem_inventory, rename_files, merge_files_day
#from gemlog.gemlog_aux import make_db, calc_channel_stats
#from gemlog.gem_cat import gem_cat
#from gemlog.version import __version__

#try:
#    from gemlog import parsers
#except ImportError:
#    print('Cannot find "parsers"; continuing')
#    pass
