from __future__ import print_function, division

import numpy as np
import sys

import nsfg1
import stat1


def read_fem_resp(dct_file='2013_2015_FemRespSetup.dct',
                dat_file='2013_2015_FemRespData.dat.gz',
                nrows=None):
    """Reads the NSFG respondent data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = stat1.read_stata_dct(dct_file)
    df_resp = dct.read_fixed_width(dat_file, compression='gzip', nrows=nrows)
    clean_fem_resp(df_resp)
    return df_resp


def clean_fem_resp(df_resp):
    """Recodes variables from the respondent frame.

    df: DataFrame
    """
    pass


def validate_pregnum(resp):
    """Validate pregnum in the respondent file.

    resp: respondent DataFrame
    """
    # read the pregnancy frame
    preg = nsfg1.read_fem_preg()

    # make the map from caseid to list of pregnancy indices
    preg_map = nsfg1.make_preg_map(preg)
    
    # iterate through the respondent pregnum series
    for index, pregnum in resp.pregnum.items():
        caseid = resp.caseid[index]
        indices = preg_map[caseid]

        # check that pregnum from the respondent file equals
        # the number of records in the pregnancy file
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    resp = read_fem_resp()

    assert(len(resp) == 5699)
    assert(resp.pregnum.value_counts()[1] == 888)
    assert(validate_pregnum(resp))

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
