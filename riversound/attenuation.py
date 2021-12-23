import numpy as np
import matplotlib.pyplot as plt

## Audible attenuation is covered by ISO 9613-1, which is not freely available as far as I can tell. The "acoustics" package looks like the easiest way to implement the ISO 9613-1 solution.
from acoustics.standards.iso_9613_1_1993 import *
from acoustics.atmosphere import Atmosphere
from warnings import warn

def attenuation_power_spectrum(freqs, distance_m, temperature_C=20, pressure_Pa=101325, humidity_percent=20.0):
    """
    Calculate the power spectrum associated with attenuation. Divide an observed power spectrum by 
    the result to remove the effect of attenuation.

    Parameters:
    -----------
    freqs: frequencies for which attenuation should be calculated (Hz)
    distance_m: distance from source to receiver in meters
    temperature_C: local air temperature in degrees C
    pressure_kPa: local air pressure in kPa
    humidity_percent: between 0 and 100

    Returns:
    --------
    numpy array of same length as freqs

    Note:
    -----
    Pressure's effect on attenuation is insignificant at reasonable topographic heights. Temperature
    and humidity have significant non-monotone effects. Attenuation always increases with increased
    distance and frequency.

    This function is just a wrapper for code from the python "acoustics" package, which implements
    the ISO-9613-1 definition of atmospheric attenuation.
    
"""
    ## Make sure inputs look reasonable. It's easy to mess up units.
    if temperature_C < -273.15:
        raise ValueError('Invalid temperature (must be Celsius and above absolute zero)')
    if temperature_C > 200:
        warn('Temperature should be Celsius; did you provide Kelvins instead?')
    if (humidity_percent < 0) or (humidity_percent > 100):
        raise ValueError('Invalid humidity; must be relative humidity in percent (0-100)')
    if pressure_Pa < 0:
        raise ValueError('Pressure cannot be negative')
    if (pressure_Pa > 1.2e5) or (pressure_Pa < 120):
        warn('Pressure should be in Pa, and the provided value looks unlikely')
    ## Do the calculation with the "acoustics" package
    a = Atmosphere(temperature_C + 273.15, pressure_Pa / 1000, humidity_percent)
    return 10**(0.1 * distance_m * -a.attenuation_coefficient(freqs)) # power units, not amplitude, not dB


### test code: compare against valid data from ISO9613-1 table 1, posted online here:
#### http://resource.npl.co.uk/acoustics/techguides/absorption/validata.html
def E_to_dB(x): return 10 * np.log10(x)

def approx_equal(x, y, p = 0.01):
    return np.abs((x - y)/x) < p

assert approx_equal(E_to_dB(attenuation_power_spectrum(50.12, 1, -20, 101325, 10)), -0.000589)
assert approx_equal(E_to_dB(attenuation_power_spectrum(251.19, 1, 15, 101325, 70)), -0.00113)
assert approx_equal(E_to_dB(attenuation_power_spectrum(1000.0, 1, 45, 101325, 20)), -0.0101)
assert approx_equal(E_to_dB(attenuation_power_spectrum(10000.0, 1, 20, 101325, 15)), -0.267)


