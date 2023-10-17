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
    p, x = max([(p, x) for x, p in hist.items()])
    return x


def AllModes(hist):
    """Returns value-freq pairs in decreasing order of frequency.

    hist: Hist object

    returns: iterator of value-freq pairs
    """
    return sorted(hist.items(), key=itemgetter(1), reverse=True)


def WeightDifference(live, firsts, others):
    """Explore the difference in weight between first babies and others.

    live: DataFrame of all live births
    firsts: DataFrame of first babies
    others: DataFrame of others
    """
    print("Columns in the 'live' DataFrame:", live.columns)

    mean0 = live.totalwgt_lb1.mean()
    mean1 = firsts.totalwgt_lb1.mean()
    mean2 = others.totalwgt_lb1.mean()

    var1 = firsts.totalwgt_lb1.var()
    var2 = others.totalwgt_lb1.var()

    print('Mean')
    print('First babies', mean1)
    print('Others', mean2)

    print('Variance')
    print('First babies', var1)
    print('Others', var2)

    print('Difference in lbs', mean1 - mean2)
    print('Difference in oz', (mean1 - mean2) * 16)

    print('Difference relative to mean (%age points)', 
          (mean1 - mean2) / mean0 * 100)

    d = stat1.CohenEffectSize(firsts.totalwgt_lb1, others.totalwgt_lb1)
    print('Cohen d', d)


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    live, firsts, others = distributions.MakeFrames()
    hist = stat1.Hist(live.prglngth)

    # explore the weight difference between first babies and others
    WeightDifference(live, firsts, others)

    # test Mode    
    mode = Mode(hist)
    print('Mode of preg length', mode)
    assert(mode == 39)

    # test AllModes
    modes = AllModes(hist)
    assert(modes[0][0] == 39)  # Check the value of the mode

    for value, freq in modes[:5]:
        print(value, freq)

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
