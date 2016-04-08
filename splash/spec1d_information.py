import numpy as np
import os
import pandas as pd
import re

from astropy.coordinates import Angle
from astropy.io import fits
from multiprocessing import Pool

from py_specrebin import rebinspec

spec1d_tags = ['LBIN','SPEC','IVAR','SPECNORMED','IVARNORMED','POS_A',
               'PAR_A','RA','DEC','RA_DEG','DEC_DEG','MASK_RA','MASK_DEC']

def one_star(input):
    '''
    Read the spec1d file, shift each chip to the rest frame, and stitch together
    :param input: tuple containing (dataframe, spec1d_file, z, lbin)
    :return: tuple containing spec1d file and Series containing all information
    '''

    spec1d_file, z, zqual, lbin = input
    nlbin = len(lbin)

    flux = np.zeros(nlbin)
    ivar = np.zeros(nlbin)

    while sum(flux) == 0:

        hdu = fits.open(spec1d_file)

        # Check number of extensions
        if np.size(hdu) < 5:
            log.write('%s has the wrong number of extensions \n' %(spec1d_file))
            break

        # Are the extensions structure arrays
        sB = hdu[1].data
        sR = hdu[2].data

        if (sB == None) or (sR == None):
            log.write('%s is missing a structure \n' %(spec1d_file))
            break

        if min(sR.LAMBDA[0]) < max(sB.LAMBDA[0] < 25):
            sR = hdu[3].data

        rSpec = sR.SPEC[0]
        bSpec = sB.SPEC[0]

        # Does the spectrum actually have values
        if ((bSpec[(bSpec != bSpec) | (bSpec == 0.0)]).sum() > 3000) or \
                ((rSpec[(rSpec != rSpec) | (rSpec == 0.0)]).sum() > 3000):
            log.write('%s does not have enough real numbers in its arrays \n' %(spec1d_file))
            break

        # Shift to rest frame
        lrshift = sR.LAMBDA[0]/(1.+z)
        lbshift = sB.LAMBDA[0]/(1.+z)

        # Rebin red side
        specbinR, ivarbinR = rebinspec(lrshift, rSpec, lbin, ivar=sR.IVAR[0])

        # Rebin blue side
        specbinB, ivarbinB = rebinspec(lbshift, bSpec, lbin, ivar=sB.IVAR[0])

        # stitch the sides together
        for j in range(nlbin):
            if specbinR[j] == specbinR[j]:
                flux[j] = specbinR[j]
                ivar[j] = ivarbinR[j]
            else:
                flux[j] = specbinB[j]
                ivar[j] = ivarbinB[j]

        # Some header information for ease of reading the subsequent lines
        header = hdu[1].header
        ra = header['RA_OBJ']
        dec = header['DEC_OBJ']

        tonorm = np.median(flux[(lbin > 7500) & (lbin < 7600)])
        data = [lbin, flux, ivar, flux/tonorm, ivar*(tonorm**2), header['SLITPA'], header['PARANG'],
                ra, dec,Angle('%s hours'%(ra)).degrees, Angle('%s degrees' %(dec)).degrees,
                header['RA'], header['DEC']]

        return spec1d_file, pd.Series(dict(zip(spec1d_tags, data)))


def spec1d(spec1d_files, zspec_array, lbin, tags, logfile):
    '''
    multiprocessing wrapper for the one_star function
    :param spec1d_files:
    :param z_array: array of tuples containing (z, zqual)
    :param lbin: wavelength array to bin things onto
    :param tags: tags to output (does not need to just be spec1d tags)
    :param logfile:
    :return: dataframe containing spec1d info
    '''

    # initialize df
    df = pd.DataFrame(columns=[st for st in spec1d_tags if st in tags], index=spec1d_files)

    # open log file
    global log
    log = open(logfile,'a')

    # run one_star in parallel
    inputs = [(sf, z, zqual, lbin) for sf, z, zqual in zip(spec1d_files, zspec_array)]
    pool = Pool(processes=8)
    output = pool.map(one_star, inputs)

    # update df
    for i, s in output:
        df.loc[i] = s

    log.close()

    return df