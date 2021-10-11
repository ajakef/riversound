import riversound, glob, obspy, matplotlib, datetime, os, gemlog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def site_reference_spectrum(infrasound_file, audible_file, t1, t2, nfft_infrasound = 2**13, nfft_audible = 2**15):
    nfft_audible = 2**15
    nfft_infrasound = 2**13
    tr_audible = riversound.read_audiomoth(audible_file, remove_response = True)
    tr_infrasound = obspy.read(infrasound_file)[0]
    tr_infrasound = gemlog.deconvolve_gem_response(tr_infrasound) # must deconvolve when not using read_infrasound_audible
    tr_infrasound.trim(t1,t2)
    tr_audible.trim(t1,t2)
    infra_spec_info = riversound.spectrum(tr_infrasound, nfft = nfft_infrasound,kurtosis_threshold = 0.25, overlap = 0.9)
    aud_spec_info = riversound.spectrum(tr_audible, nfft = nfft_audible,kurtosis_threshold = 0.25, overlap = 0.9)

    freqs_audible = aud_spec_info['freqs']
    w = (freqs_audible < 20000) & (freqs_audible > 40)
    freqs_audible = freqs_audible[w]    
    medspec_audible = aud_spec_info['median'][w]

    freqs_infrasound = infra_spec_info['freqs']
    w = (freqs_infrasound < 40) & (freqs_infrasound > 0)
    freqs_infrasound = freqs_infrasound[w]    
    medspec_infrasound = infra_spec_info['median'][w]

    freqs = np.concatenate([freqs_infrasound, freqs_audible])
    medspec = np.concatenate([medspec_infrasound, medspec_audible])

    return pd.DataFrame.from_dict({'freqs':freqs, 'spectrum':medspec})


def plot_noise_specs(ax = plt):
    noise_spec_low = gemlog.ims_noise('low')
    noise_spec_med = gemlog.ims_noise('med')
    noise_spec_high = gemlog.ims_noise('high')
    w_ims = noise_spec_low['freqs'] < 8
    noise_spec_gem = gemlog.gem_noise()
    w_gem = noise_spec_gem['freqs'] < 25

    ax.loglog(noise_spec_low['freqs'][w_ims], noise_spec_low['spectrum'][w_ims], 'lightgray')
    ax.loglog(noise_spec_med['freqs'][w_ims], noise_spec_med['spectrum'][w_ims], 'lightgray')
    ax.loglog(noise_spec_high['freqs'][w_ims], noise_spec_high['spectrum'][w_ims], 'lightgray')
    ax.loglog(noise_spec_gem['freqs'][w_gem], noise_spec_gem['spectrum'][w_gem], 'lightgray')

