## Example of how to estimate a power law for a spectrum. This is inherently a tricky thing to do and it requires some human judgement (particularly picking the bounds) to get good results consistently.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import riversound

## read in a data file (either .wav, or a ref spectrum)
site = 'MRBD' # Maple River Beaver Dam (Michigan)
if site.lower() == 'mrbd':
    freqs, spectrum = read_ref_spec('data/reference_spectra/MRBD_2021-09-13.txt')
elif site.lower() == 'wwp_p2_1':
    freqs, spectrum = read_ref_spec('data/reference_spectra/WWP_P2_1_2021-06-14.txt')
elif site.lower() == 'wwp':
    freqs, spectrum = read_ref_spec('data/reference_spectra/WWP_2021-05-24.txt')
elif site.lower() in ['annmorrison', 'settlers']:
    freqs, spectrum = read_ref_spec('data/reference_spectra/AnnMorrison_2021-04-27_2021-05-01.txt')
elif site.lower() in ['eckert', 'ridenbaugh']:
    freqs, spectrum = read_ref_spec('data/reference_spectra/Eckert_2021-05-24.txt')
elif site.lower() == 'con1e':
    tr = riversound.read_audiomoth('data/audiomoth/20210414_060000.WAV')
    s = riversound.spectrum(tr, nfft = 2**16)
    freqs, spectrum = (s['freqs'], s['mean'])

## calculate the power law by binning the spectrum into 3rd-octaves and calculating the slope between 2 points
d = band_bin(freqs, spectrum)
plt.loglog(d['centers'], d['psd'])
calc_degree_2pt(d['centers'], d['psd'], 40)
