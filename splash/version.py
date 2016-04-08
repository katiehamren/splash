from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "splash: a module for accessing and formatting SPLASH data"
# Long description will go up on the pypi page
long_description = """

splash
========
splash is a module for creating databases of data from the SPLASH survey

To get started you will need to contact Prof. Puragra GuhaThakurta at UC Santa Cruz
for access to the SPLASH data.

To get started with this code, head to the
repository README_.

.. _README: https://github.com/uwescience/shablona/blob/master/README.md

License
=======
``splash`` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2016--, Katherine Hamren, UC Santa Cruz
"""

NAME = "splash"
MAINTAINER = "Katherine Hamren"
MAINTAINER_EMAIL = "katherine.hamren@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://github.com/katie.hamren/splash"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Katherine Hamren"
AUTHOR_EMAIL = "katherine.hamren@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['splash',
            'splash.tests']
PACKAGE_DATA = {'splash': [pjoin('data', '*')]}
REQUIRES = ["astropy","numpy"]
