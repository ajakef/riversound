#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    raise RuntimeError('setuptools is required')


import os
from distutils.util import convert_path
import sys

# The minimum python version which can be used to run ObsPy
MIN_PYTHON_VERSION = (3, 6)

# Fail fast if the user is on an unsupported version of python.
if sys.version_info < MIN_PYTHON_VERSION:
    msg = ("gemlog requires python version >= {}".format(MIN_PYTHON_VERSION) +
           " you are using python version {}".format(sys.version_info))
    print(msg, file=sys.stderr)
    sys.exit(1)


DESCRIPTION = ''
LONG_DESCRIPTION = """
"""

DISTNAME = 'riversound'
LICENSE = 'GPL-3.0'
AUTHOR = 'Jake Anderson'
MAINTAINER_EMAIL = 'ajakef@gmail.com'
URL = 'https://github.com/ajakef/riversound'


# TO-DO: replace this with versioneer
#version_dict = {}
#version_path = convert_path('gemlog/version.py')
#with open(version_path) as version_file:
#    exec(version_file.read(), version_dict)
#VERSION = version_dict['__version__']
VERSION = '0.1.1'

INSTALL_REQUIRES = [
#    'simpleaudio', # hard to install on windows? non-essential
    'acoustics',
    'obspy',
    'numpy==1.22.0', # 1.22.0 breaks obspy 1.2.2. When new obspy is released, make both >=
    'pandas>=1.0.0',
    'scipy>=1.0.0',
    'matplotlib>=3.2.0',
    'lxml',
    'setuptools',
    'sqlalchemy',
    'decorator',
    'requests'
]

TESTS_REQUIRE = ['pytest']

EXTRAS_REQUIRE = {
    # 'optional': [...],
    'doc': ['sphinx==3.2.1', 'sphinx-rtd-theme==0.5.0'],
    'test': TESTS_REQUIRE
}
EXTRAS_REQUIRE['all'] = sorted(set(sum(EXTRAS_REQUIRE.values(), [])))

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Physics'
]

ENTRY_POINTS = {
    'console_scripts': [
        'convert_wav = riversound.convert_wav:main',
        'play_data = riversound.play_data:main',
#        'gemconvert = gemlog.gem2ms:main',
#        'gem_cat = gemlog.gem_cat:main'
    ]
}

setuptools_kwargs = {
    'zip_safe': False,
    'scripts': [],
    'include_package_data': True,
}

PACKAGES = ['riversound']

ext_modules = []

setup(name=DISTNAME,
      version=VERSION,
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      tests_require=TESTS_REQUIRE,
      ext_modules=ext_modules,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      maintainer_email=MAINTAINER_EMAIL,
      license=LICENSE,
      url=URL,
      classifiers=CLASSIFIERS,
      entry_points=ENTRY_POINTS,
      **setuptools_kwargs)
