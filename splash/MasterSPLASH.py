import glob
import numpy as np
import os
import pandas as pd
import pdb
import pickle
import re

from spec1d_information import spec1d
from zspec_information import zquality
from utils import _parse_filename

class splash_fits():

    def __init__(self, selection_type,selection_array=None, tags=None, spec1d_path=None, zspec_path=None,
                 lbin_int=0.65, lmin=4000, lmax=10000, logfile='log.txt'):
        '''

        :param selection_type: How you want to select SPLASH data. Options are:
            - all data
            - masks
            - fields
            - fieldtype
        :param selection_array: array containing information necessary to select SPLASH data
        :param tags: tags to include in the resulting file. Default (None) is [LBIN, SPEC, IVAR, RA, DEC]
        :param spec1d_path: path pointing to spec1d repository
        :param zspec_path: path pointing to zspec repository
        :param lbin_int: wavelength dispersion
        :param lmin: minimum wavelength
        :param lmax: maximum wavelength
        :return:
        '''


        # Verify basic inputs
        if selection_type not in ['all data', 'masks','fields','fieldtype']:
            raise AttributeError("Invalid selection type. Options are [all data, masks, fields, fieldtype]")

        if selection_type == 'all data':
            if selection_array is not None:
                raise AttributeError("If 'all data' is selection_type, no selection_array is necessary")

        if selection_type == 'fieldtype':
            if np.any([sa.lower() not in ['dsph','de','halo','substruct','disk','m32'] for sa in selection_array]):
                raise AttributeError('Invalid value in selection array')

        if (spec1d_path is None) or not os.path.isdir(spec1d_path):
            raise AttributeError("spec1d path does not exist")

        tag_map = pickle.load(open('tag_map.p','rb'))

        if (type(tags) != list) and (type(tags) != np.ndarray) and (tags is not None):
            raise AttributeError("tags must be a list, array, or None for default")
        else:
            if tags is None: #Set default tags
                tags = ['LBIN','SPEC','IVAR','RA','DEC']

            if np.any([type(t) != str for t in tags]):
                raise AttributeError("tags must be a list/array of strings")

            if np.any([t not in tag_map.keys() for t in tags]):
                raise AttributeError("one or more tags are not recognized")


        self.selection_type = selection_type
        self.selection_array = selection_array
        self.spec1d_path = spec1d_path
        self.zspec_path = zspec_path
        self.tags = tags

        self.get_stars()

        nlbin = np.fix((lmax-lmin)/lbin_int)
        self.lbin = lmin+lbin_int*np.arange(nlbin)

        self.df = pd.DataFrame(columns=self.tags, index=self.spec1d_files)

        # Go through the tags and get the appropriate information
        pdb.set_trace()
        self.update_df(zquality(self.zspec_path, self.spec1d_files, self.tags))
        pdb.set_trace()
        self.update_df(spec1d(self.spec1d_files, (self.df.Z, self.df.ZQUAL), self.lbin, self.tags))





    def update_df(self, new_df):
        '''
        Fill in the existing df (contained in self.df) with information from a new df
        :param new_df:
        :return: updated self.df
        '''

        for tag in new_df.columns:
            for sf in self.df.index:
                self.df[tag].loc[sf] = new_df[tag].loc[sf]

    @staticmethod
    def _get_fieldtype(mask):
        '''
        Determine fieldtype of a particular mask
        :param mask:
        :return:
        '''

        substruct = ['a3_1','a3_2','a3_3','f2_1','f2_2','f207_1','NE1','NE2','NE3','NE4','NE6',
                     'NW13dV','NW14V_1','NW15V','NW1dV','NW2V_1','NW2V_2','NW2dV','NW3V_1','NW9V_1',
                     'NW9V_2','f123_1','f115_1','f109_1','f116_1','f135_1','m4_1','m4_2','m4_3','m4_4',
                     'm4_5','a13_1','a13_2','a13_3','a13_4','A220_1','A220_2','A220_3']

        if ('mct' in mask) or (mask == 'SE7'):
            return 'disk'
        elif ('d' in mask) and ('nw' not in mask):
            return 'dsph'
        elif ('n147' in mask) or ('n185' in mask) or ('n205' in mask):
            return 'de'
        elif ('m32' in mask):
            return 'm32'
        elif mask in substruct:
            return 'substruct'
        else:
            return 'halo'

    def get_stars(self):

        all_spec1d_files = np.array(glob.glob('%s/*.fits*' %(self.spec1d_path)))
        all_masks = np.array([_parse_filename(f)[0] for f in all_spec1d_files])
        all_fields = np.array([re.split('_',m)[0].lower() for m in all_masks])
        all_fieldtypes = map(self._get_fieldtype, all_masks)

        if self.selection_type == 'all data':
            # When "all data" is the selection type, count up all the spec1d files
            return all_spec1d_files.size, all_spec1d_files

        elif self.selection_type == 'masks':
            # When masks is the selection type, retrieve the files with matching masks
            ind = np.array([i for i, m in enumerate(all_masks) if m in self.selection_array])
            print '%i of %i masks found' %(len(set(all_masks[ind])), len(set(self.selection_array)))

        elif self.selection_type == 'fieldtype':
            # When fieldtype is the selection type, retrieve the files of the same fieldtype
            ind = np.array([i for i, ft in enumerate(all_fieldtypes) if ft in self.selection_array])

        elif self.selection_type == 'fields':
            # When fields is the selection type, return the files of the same fields
            ind = np.array([i for i, m in enumerate(all_fields) if m in self.selection_array])
            print '%i of %i fields found' %(len(set(all_fields[ind])), len(set(self.selection_array)))
        else:
            raise AttributeError('unrecognized selection type, must be "all_data","masks","fields", or "fieldtype"')

        self.nstars = all_spec1d_files[ind].size
        self.spec1d_files = all_spec1d_files[ind]













