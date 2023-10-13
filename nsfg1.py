import sys
import numpy as np
import stat1

from collections import defaultdict

def read_fem_preg(dct_file='2013_2015_FemPregSetup.dct',
                dat_file='2013_2015_FemPregData.dat.gz'):
    """Reads the NSFG pregnancy data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = stat1.read_stata_dct(dct_file)
    df = dct.read_fixed_width(dat_file, compression='gzip')
    clean_fem_preg(df)
    return df


def clean_fem_preg(df):
    """Recodes variables from the pregnancy frame.

    df: DataFrame
    """

    # Check if 'BIRTHWGT_LB1' column exists in the DataFrame
    if 'birthwgt_lb1' not in df.columns:
        print("Error: 'birthwrgt_lb1' column not found in the DataFrame.")
        return

    # birthwgt_lb contains at least one bogus value (51 lbs)
    # replace with NaN
    df.loc[df.birthwgt_lb1 > 20, 'birthwgt_lb1'] = np.nan
    
    # replace 'not ascertained', 'refused', 'don't know' with NaN
    na_vals = [98, 99]
    df.birthwgt_lb1.replace(na_vals, np.nan, inplace=True)
    df.birthwgt_oz1.replace(na_vals, np.nan, inplace=True)
    df.hpagelb.replace(na_vals, np.nan, inplace=True)

    df.babysex1.replace([8, 9], np.nan, inplace=True)
    df.nbrnaliv.replace([8], np.nan, inplace=True)

    # birthweight is stored in two columns, lbs and oz.
    # convert to a single column in lb
    # NOTE: creating a new column requires dictionary syntax,
    # not attribute assignment (like df.totalwgt_lb)
    df['total_lb1'] = df.birthwgt_lb1 + df.birthwgt_oz1 / 16.0    

    # due to a bug in ReadStataDct, the last variable gets clipped;
    # so for now set it to NaN
    df.cmintvw = np.nan

def make_preg_map(df):
    """Make a map from caseid to list of preg indices.

    df: DataFrame

    returns: dict that maps from caseid to list of indices into `preg`
    """
    d = defaultdict(list)
    for index, caseid in df.caseid.items():
        d[caseid].append(index)
    return d
