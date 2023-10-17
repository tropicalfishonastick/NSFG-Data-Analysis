from __future__ import print_function

import sys
from operator import itemgetter

import distributions
import stat1


def Mode(hist):
    """Returns the value with the highest frequency.

    hist: Hist object

    returns: value from Hist
    """
    # Find the item with the maximum frequency in the histogram
    max_item = max(hist.items(), key=itemgetter(1))
    return max_item[0]


def AllModes(hist):
    """Returns value-freq pairs in decreasing order of frequency.

    hist: Hist object

    returns: iterator of value-freq pairs
    """
    # Sort items in decreasing order of frequency
    return sorted(hist.items(), key=itemgetter(1), reverse=True)


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    live, firsts, others = distributions.MakeFrames()
    hist = stat1.Hist(live.prglngth)

    # test Mode
    mode = Mode(hist)
    print('Mode of preg length', mode)
    assert mode == 39, mode

    # test AllModes
    modes = AllModes(hist)
    assert modes[0][1] == 2370, modes[0][1]

    for value, freq in modes[:5]:
        print(value, freq)

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
