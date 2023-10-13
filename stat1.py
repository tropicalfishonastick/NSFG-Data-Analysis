import pandas as pd
import numpy as np
import re
from scipy import ndimage

class FixedWidthVariables(object):
    def __init__(self, variables, index_base=0):
        self.variables = variables
        self.colspecs = variables[["start", "end"]] - index_base
        self.colspecs = self.colspecs.astype(int).values.tolist()
        self.names = variables["name"]

    def read_fixed_width(self, filename, **options):

        df = pd.read_fwf(filename, colspecs=self.colspecs, names=self.names, **options)
        return df

def read_stata_dct(dct_file, **options):
    type_map = dict(byte=int, int=int, long=int, float=float, double=float, numeric=float)
    var_info = []

    with open(dct_file, **options) as f:
        for line in f:
            match = re.search(r"_column\(([^)]*)\)", line)
            if not match:
                continue
            start = int(match.group(1))
            t = line.split()
            vtype, name, fstring = t[1:4]
            name = name.lower()
            if vtype.startswith("str"):
                vtype = str
            else:
                vtype = type_map[vtype]
            long_desc = " ".join(t[4:]).strip('"')
            var_info.append((start, vtype, name, fstring, long_desc))

    columns = ["start", "type", "name", "fstring", "desc"]
    variables = pd.DataFrame(var_info, columns=columns)
    variables["end"] = variables.start.shift(-1)
    variables.loc[len(variables) - 1, "end"] = -1

    dct = FixedWidthVariables(variables, index_base=1)
    return dct

def Resample(xs, n=None):
    """Draw a sample from xs with the same length as xs.

    xs: sequence
    n: sample size (default: len(xs))

    returns: NumPy array
    """
    if n is None:
        n = len(xs)
    return np.random.choice(xs, n, replace=True)

def SampleRows(df, nrows, replace=False):
    """Choose a sample of rows from a DataFrame.

    df: DataFrame
    nrows: number of rows
    replace: whether to sample with replacement

    returns: DataDf
    """
    indices = np.random.choice(df.index, nrows, replace=replace)
    sample = df.loc[indices]
    return sample

def ResampleRows(df):
    """Resamples rows from a DataFrame.

    df: DataFrame

    returns: DataFrame
    """
    return SampleRows(df, len(df), replace=True)

def ResampleRowsWeighted(df, column="finalwgt"):
    """Resamples a DataFrame using probabilities proportional to given column.

    df: DataFrame
    column: string column name to use as weights

    returns: DataFrame
    """
    weights = df[column].copy()
    weights /= sum(weights)
    indices = np.random.choice(df.index, len(df), replace=True, p=weights)
    sample = df.loc[indices]
    return sample

def PercentileRow(array, p):
    """Selects the row from a sorted array that maps to percentile p.

    p: float 0--100

    returns: NumPy array (one row)
    """
    rows, cols = array.shape
    index = int(rows * p / 100)
    return array[index,]

def PercentileRows(ys_seq, percents):
    """Given a collection of lines, selects percentiles along vertical axis.

    For example, if ys_seq contains simulation results like ys as a
    function of time, and percents contains (5, 95), the result would
    be a 90% CI for each vertical slice of the simulation results.

    ys_seq: sequence of lines (y values)
    percents: list of percentiles (0-100) to select

    returns: list of NumPy arrays, one for each percentile
    """
    nrows = len(ys_seq)
    ncols = len(ys_seq[0])
    array = np.zeros((nrows, ncols))

    for i, ys in enumerate(ys_seq):
        array[i,] = ys

    array = np.sort(array, axis=0)

    rows = [PercentileRow(array, p) for p in percents]
    return rows

def Smooth(xs, sigma=2, **options):
    """Smooths a NumPy array with a Gaussian filter.

    xs: sequence
    sigma: standard deviation of the filter
    """
    return ndimage.filters.gaussian_filter1d(xs, sigma, **options)

