from __future__ import print_function
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt
import nsfg1
import stat1

def MakeFrames():
    """Reads pregnancy data and partitions first babies and others.

    returns: DataFrames (all live births, first babies, others)
    """
    preg = nsfg1.read_fem_preg()

    live = preg[preg.outcome == 1]
    firsts = live[live.birthord == 1]
    others = live[live.birthord != 1]

    print("Length of live:", len(live))
    print("Length of firsts:", len(firsts))
    print("Length of others:", len(others))

    assert len(live) == 6489
    assert len(firsts) == 3067
    assert len(others) == 3422
    return live, firsts, others

def Summarize(live, firsts, others):
    """Print various summary statistics."""
    # Your existing code here

def PrintExtremes(live):
    """Plots the histogram of pregnancy lengths and prints the extremes.

    live: DataFrame of live births
    """
    hist = stat1.Hist(live.prglngth)

    # Plot histogram
    plt.hist(live.prglngth, bins=np.arange(-0.5, 54.5, 1), label='live births', alpha=0.7)

    # Save the plot as PNG and PDF files
    plt.savefig('first_nsfg_hist_live.png')
    plt.savefig('first_nsfg_hist_live.pdf')

    # Display the plot
    plt.show()

    print('Shortest lengths:')
    for weeks, freq in hist.smallest(10):  # Corrected to smallest
        print(weeks, freq)

    print('Longest lengths:')
    for weeks, freq in hist.largest(10):
        print(weeks, freq)

def MakeHists(live, firsts, others):
    """Plot Hists for live births

    live: DataFrame
    firsts: DataFrame
    others: DataFrame
    """
    # Your existing code here

def MakeComparison(firsts, others):
    """Plots histograms of pregnancy length for first babies and others.

    firsts: DataFrame
    others: DataFrame
    """
    # Plot histograms side-by-side
    plt.hist(firsts['prglngth'].dropna(), bins=np.arange(26.5, 47.5, 1), label='first', alpha=0.7)
    plt.hist(others['prglngth'].dropna(), bins=np.arange(26.5, 47.5, 1), label='other', alpha=0.7)

    plt.xlabel('Weeks')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Comparison of Pregnancy Lengths for First Babies and Others')
    plt.savefig('prglngth_comparison.png')
    plt.savefig('prglngth_comparison.pdf')
    plt.show()

def main(script):
    live, firsts, others = MakeFrames()

    MakeHists(live, firsts, others)
    PrintExtremes(live)
    MakeComparison(firsts, others)
    Summarize(live, firsts, others)

if __name__ == '__main__':
    import sys
    main(sys.argv)



