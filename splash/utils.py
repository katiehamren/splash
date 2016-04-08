import re

def _parse_filename(filename):
    '''
    Split spec1d filenames into useful information
    :param filename: filename to parse
    :return:
    '''

    fparts = re.split('\.',filename)
    if fparts[-1] == 'gz':
        jnk, mask, slit, objname, jnk = fparts[:-1]
    elif fparts[-1] == 'fits':
        jnk, mask, slit, objname = fparts[:-1]
    else:
        raise ValueError('Invalid filename')

    return mask, slit, objname