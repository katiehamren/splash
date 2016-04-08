import os
import re
import pdb
import warnings
import numpy as np
import pandas as pd

from astropy.io import fits

from utils import _parse_filename


warnings.filterwarnings('ignore')
zspec_tags = ['Z', 'ZQUAL','ZSNR','ABAND','MJD','AIRM']


def zquality(zspec_path, spec1d_files, tags, serendip_file=None):
    '''
    Return the values associated with "tags" for the stars in spec1d_files
    :param zspec_path: path to zspec files
    :param spec1d_files: list/array of spec1d_files
    :param tags: list/array of tags to return.
    :param serendip_file: file (with path) containing serendip information
    :return: A dataframe that contains those tags from the "tags" input that can be accomplished with a
    '''

    if (zspec_path is None) or not os.path.isdir(zspec_path):
        raise AttributeError("zspec path does not exist")

    if (type(spec1d_files) != list) & (type(spec1d_files) != np.ndarray):
        raise AttributeError('spec1d_files must be a list or array')
    elif type(spec1d_files) == list:
        spec1d_files = np.array(spec1d_files)

    if serendip_file is None:
        print 'skipping serendips'
    elif serendip_file == 'Default':

        if os.path.isfile('%s/SLIT.goodFormat' %(zspec_path)):
            serendip_file = '%s/SLIT.goodFormat' %(zspec_path)
            print 'using default serendip file'
        else:
            raise IOError('no default serendip file')
    else:
        if not os.path.isfile(serendip_file):
            raise IOError('input serendip file does not exist')

    # Get the masks associated with these spec1d files, so as to go mask by mask
    all_masks = np.array([_parse_filename(sf)[0] for sf in spec1d_files])

    # Go mask by mask and get a dataframe of all zspec-related tags
    df_list = []
    for m in all_masks:

        zfile = '%s/zspec.%s.fits' %(zspec_path, m)
        sfiles = spec1d_files[all_masks == m]

        df = read_zspec_fits(zfile, sfiles, serendip_file)
        df_list.append(df)

    # Concatenate dataframes into a master
    full_df = pd.concat(df_list)

    # Include all tags that are either included in the desired list OR are necessary later
    # Things that will matter later include
    # - Z, ZQUAL (for shift & stitch)
    # - MJD, ABAND (for kinematics)

    return full_df[[c for c in full_df.columns if (c in tags) | (c in ['Z','ZQUAL','MJD','ABAND'])]]


def read_zspec_fits(zfile, spec1d_files, serendip_file):
    '''
    Given an input zspec file and a list of spec1d_files, return a dataframe containing all possible tags
    :param zfile: zspec file
    :param spec1d_files: list of spec1d_files associated with the input zfile
    :return:
    '''

    mask = re.split('\.', zfile)[1]

    if os.path.isfile(zfile):
        hduZ = fits.open(zfile)
        zspec = hduZ[1].data
    else:
        raise ValueError('invalid zfile, does not exist')

    df = pd.DataFrame(columns=zspec_tags, index=spec1d_files)


    # walk through each spec1d_file one at a time
    for sf in spec1d_files:

        # find the relevant entry in the zspec file by using the spec1d_file tag (where available)
        if 'SPEC1D_FILE' in hduZ[1].columns.names:
            charInds = np.core.defchararray.find(zspec.SPEC1D_FILE,sf)
            ind = np.argwhere(charInds != -1)

        else:
            zspec_spec1d_file = np.array(['spec1d.%s.%s.%s.fits.gz' %(mask, s.zfill(3), o)
                                          for s, o in zip(zspec.SLITNAME, zspec.OBJNAME)])

            charInds = np.core.defchararray.find(zspec_spec1d_file,sf)
            ind = np.argwhere(charInds != -1)

        try:
            i = ind[0][0]
            z = zspec.Z[i]
            zqual = zspec.ZQUALITY[i]
            snr = zspec.SN[i]
            if 'ABAND' in hduZ[1].columns.names:
                aband = zspec.ABAND[i]
            else:
                aband = np.nan
            if 'MJD' in hduZ[1].columns.names:
                mjd = zspec.MJD[i]
            else:
                mjd = np.nan
            if 'AIRMASS' in hduZ[1].columns.names:
                airm = zspec.AIRMASS[i]
            else:
                airm = np.nan
        except IndexError:
            # Test if this is a serendip
            if serendip_file is None:
                airm = mjd = aband = snr = zqual = z = np.nan
            else:
                z = read_serendip_zqual(sf, serendip_file)
                zqual = 3
                airm = mjd = aband = snr = np.nan


        # This part determines if there are -1s in the zspec file. If there *are*, then zquality = 1 is a
        # manual velocity determination. If there *aren't*, then zquality = 1 is crap
        if zqual == 1:
            zq = zspec.ZQUALITY
            if -1 not in zq:
                zqual = 0

        # Write this star into the df
        df.loc[sf] = pd.Series({'Z':z, 'ZQUAL':zqual,'ZSNR':snr,'ABAND':aband,'MJD':mjd,'AIRM':airm})

    return df

def read_serendip_zqual(spec1d_file, serendip_file):
    '''
    Get z value from serendip file
    :param spec1d_file:
    :param serendip_file:
    :return: z
    '''

    try:
        zfile, z = np.loadtxt(serendip_file, usecols = (0,1), dtype = 'S30,f', unpack = True)
    except:
        raise ValueError('could not read serendip file')

    if spec1d_file in zfile:
        return z[file == zfile]
    else:
        return np.nan

