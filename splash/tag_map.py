import pickle

'''
Structure containing possible tags for "master" SPLASH files
This code pickles the structure, which is then used elsewhere in the module
'''


tag_map = {
    # Basic spectral information
    'LBIN':'E',
    'SPEC':'E',
    'IVAR':'E',
    'SNR':'D',
    # Different spectral information
    'SPECCALIB':'E',
    'IVARCALIB':'E',
    'SPECNORM':'E',
    'IVARNORM':'E',
    # Basic identification
    'MASK':'7A',
    'SLITNAME':'3A',
    'OBJNAME':'16A',
    'FULLNAME':'38A',
    'GRATE':'D',            # Grating of original observation
    'RA':'11A',
    'DEC':'11A',
    'RA_DEG':'D',           # RA in degrees
    'DEC_DEG':'D',          # DEC in degrees
    'FIELDTYPE':'9A',
    # Mask/observing information
    'POS_A':'D',            # Position angle
    'MASK_RA':'11A',        # Central mask RA
    'MASK_DEC':'11A',       # Central mask DEC
    'MASK_RA_DEG':'D',
    'MASK_DEC_DEG':'D',
    'PAR_A':'D',
    'AIRMASS':'D',
    'PIXAV':'D',            # Extinction at this position from Dalcanton+2015
    'EVSTAGE':'D',          # Evolutionary stage (AGB, RGB, etc.)
    # Kinematic information
    'ABAND':'D',
    'MJD':'D',
    'Z':'D',
    'VHEL':'D',
    'E_VHEL':'D',
    'ZQUAL':'D',
    # Photometry
    'CN':'D',
    'TIO':'D',
    'F275W':'D',
    'F336W':'D',
    'F475W':'D',
    'F814W':'D',
    'F110W':'D',
    'F160W':'D',
    'M':'D',
    'T':'D',
    'DDO51':'D',
    'I':'D',
    'V':'D',
    'R':'D',
    'M36':'D',
    'M45':'D',
    'E_F275W':'D',
    'E_F336W':'D',
    'E_F475W':'D',
    'E_F814W':'D',
    'E_F110W':'D',
    'E_F160W':'D',
    'E_M':'D',
    'E_T':'D',
    'E_DDO51':'D',
    'E_I':'D',
    'E_V':'D',
    'E_R':'D',
    'E_M36':'D',
    'E_M45':'D',
    # IDing misc objects
    'CSTAR':'D',                # carbon star?
    'ESTAR':'D'                 # emission line star?
}

pickle.dump(tag_map, open('tag_map.p','wb'))