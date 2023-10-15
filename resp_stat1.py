from __future__ import print_function, division

import sys
import nsfg1
import stat1

def read_fem_resp(dct_file='2013_2015_FemRespSetup.dct',
                             dat_file='2013_2015_FemRespData.dat.gz',
                             nrows=None):
    dct = stat1.read_stata_dct(dct_file)
    df_resp = dct.read_fixed_width(dat_file, compression='gzip', nrows=nrows)
    clean_fem_resp(df_resp)
    return df_resp


def clean_fem_resp(df_resp):
    # You can add cleaning logic if needed
    pass


def validate_pregnum(resp, preg):
    preg_map = nsfg1.make_preg_map(preg)

    for index, pregnum in resp.pregnum.items():
        caseid = resp.caseid[index]
        indices = preg_map.get(caseid, [])

        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True


def main():
    resp = read_fem_resp()

    assert len(resp) == 5699
    assert resp.pregnum.value_counts()[1] == 888

    # Read and clean pregnancy DataFrame
    preg = nsfg1.read_fem_preg()

    # Validate pregnum
    assert validate_pregnum(resp, preg)

    print('All tests passed.')


if __name__ == '__main__':
    main()

