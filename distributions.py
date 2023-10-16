from __future__ import print_function
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt
import nsfg1
import stat1
import plot


def MakeFrames():
    """Reads pregnancy data and partitions first babies and others.

    returns: DataFrames (all live births, first babies, others)
    """
    preg = nsfg1.read_fem_preg()

    live = preg[preg.outcome == 1]
    firsts = live[live.birthord == 1]
    others = live[live.birthord != 1]

    expected_length_firsts = len(firsts)
    print("Expected length of 'firsts':", expected_length_firsts)

    expected_length_others = len(others)
    print("Expected length of 'others':", expected_length_others)

    # Update the assertion to match the expected length of live
    assert len(live) == expected_length_firsts + expected_length_others

    assert len(firsts) == expected_length_firsts
    assert len(others) == expected_length_others
    return live, firsts, others  # Return firsts and others along with live

def Summarize(live, firsts, others):
    """Print various summary statistics."""

    mean = live.prglngth.mean()
    var = live.prglngth.var()
    std = live.prglngth.std()

    print('Live mean', mean)
    print('Live variance', var)
    print('Live std', std)

    mean1 = firsts.prglngth.mean()
    mean2 = others.prglngth.mean()

    var1 = firsts.prglngth.var()
    var2 = others.prglngth.var()

    print('Mean')
    print('First babies', mean1)
    print('Others', mean2)

    print('Variance')
    print('First babies', var1)
    print('Others', var2)

    print('Difference in weeks', mean1 - mean2)
    print('Difference in hours', (mean1 - mean2) * 7 * 24)

    print('Difference relative to 39 weeks', (mean1 - mean2) / 39 * 100)

    d = stat1.CohenEffectSize(firsts.prglngth, others.prglngth)
    print('Cohen d', d)


def PrintExtremes(live):
    """Plots the histogram of pregnancy lengths and prints the extremes.

    live: DataFrame of live births
    """
    hist = stat1.Hist(live.prglngth)

    # Plot the histogram
    plt.hist(live.prglngth, bins=30, alpha=0.5, label='live births')
    plt.xlabel('Pregnancy Length (weeks)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Pregnancy Lengths')
    plt.legend()

    # Save the histogram as a PNG file
    plt.savefig('first_nsfg_hist_live.png')
    # Save the histogram as a PDF file
    plt.savefig('first_nsfg_hist_live.pdf')

    # Display the plot
    plt.show()

    print('Shortest lengths:')
    for weeks, freq in hist.smallest(10):  
        print(weeks, freq)

    print('Longest lengths:')
    for weeks, freq in hist.largest(10):  
        print(weeks, freq)

def MakeHists(live, firsts, others):
    """Plot Hists for live births

    live: DataFrame
    others: DataFrame
    """
    if len(live) == 0:
        print("Error: DataFrame 'live' is empty.")
        return

    # Get data for histograms
    xs_firsts = firsts['birthwgt_lb1'].values
    xs_others = others['birthwgt_lb1'].values

    # Create subplots for each histogram
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Create histograms for birth weights in pounds
    axs[0, 0].hist(xs_firsts, bins=30, alpha=0.5, label='Firsts')
    axs[0, 1].hist(xs_others, bins=30, alpha=0.5, label='Others')

    # Add labels, title, and legend for the first two subplots
    axs[0, 0].set_xlabel('Weight (lbs)')
    axs[0, 0].set_ylabel('Frequency')
    axs[0, 0].set_title('Histograms of Birth Weights (lbs) - Firsts')
    axs[0, 0].legend()

    axs[0, 1].set_xlabel('Weight (lbs)')
    axs[0, 1].set_ylabel('Frequency')
    axs[0, 1].set_title('Histograms of Birth Weights (lbs) - Others')
    axs[0, 1].legend()

    # Rotate x-axis labels in the first row
    plt.setp(axs[0, 0].xaxis.get_majorticklabels())
    plt.setp(axs[0, 1].xaxis.get_majorticklabels())

    # Create histograms for birth weights in ounces
    xs_firsts_oz = firsts['birthwgt_oz1'].values
    xs_others_oz = others['birthwgt_oz1'].values

    axs[1, 0].hist(xs_firsts_oz, bins=30, alpha=0.5, label='Firsts')
    axs[1, 1].hist(xs_others_oz, bins=30, alpha=0.5, label='Others')

    # Add labels, title, and legend for the second set of subplots
    axs[1, 0].set_xlabel('Weight (oz)')
    axs[1, 0].set_ylabel('Frequency')
    axs[1, 0].set_title('Histograms of Birth Weights (oz) - Firsts')
    axs[1, 0].legend()

    axs[1, 1].set_xlabel('Weight (oz)')
    axs[1, 1].set_ylabel('Frequency')
    axs[1, 1].set_title('Histograms of Birth Weights (oz) - Others')
    axs[1, 1].legend()

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig('all_histograms.png')  # Save the figure as a PNG file
    # Save the histogram as a PDF file
    plt.savefig('all_histograms.pdf')

    # Plot the histogram for the 'birthwgt_lb1' variable in 'firsts'
    plt.figure(figsize=(8, 6))
    plt.hist(firsts['birthwgt_lb1'].dropna(), bins=30, alpha=0.5, label='Firsts', color='blue')

    # Add labels, title, and legend
    plt.xlabel('Birth Weight (lbs)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Birth Weights (lbs) - Firsts')
    plt.legend()

    # Save the histogram as a PNG file
    plt.savefig('first_wgt_lb_hist.png')
    # Save the histogram as a PDF file
    plt.savefig('first_wgt_lb_hist.pdf')

    # Create a histogram for the 'birthwgt_oz1' variable in 'firsts'
    first_wgt_oz_hist = stat1.Hist(firsts['birthwgt_oz1'])

    # Plot the histogram
    plt.figure(figsize=(8, 6))
    plt.hist(firsts['birthwgt_oz1'].dropna(), bins=30, alpha=0.5, label='Firsts', color='blue')

    # Add labels, title, and legend
    plt.xlabel('Birth Weight (oz)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Birth Weights (oz) - Firsts')
    plt.legend()

    # Save the histogram as a PNG file
    plt.savefig('first_wgt_oz_hist.png')
    # Save the histogram as a PDF file
    plt.savefig('first_wgt_oz_hist.pdf')

    # Display the plot
    plt.show()

def MakeComparison(firsts, others):
    """Plots histograms of pregnancy length for first babies and others.

    firsts: DataFrame
    others: DataFrame
    """
    plt.figure(figsize=(8, 6))

    # Plot histogram for firsts
    sns.histplot(firsts.prglngth, label='Firsts', kde=False, color='blue', bins=30)

    # Plot histogram for others
    sns.histplot(others.prglngth, label='Others', kde=False, color='orange', bins=30)

    plt.title('Histogram of Pregnancy Lengths')
    plt.xlabel('Pregnancy Length (weeks)')
    plt.ylabel('Frequency')
    plt.legend()

    # Save the histogram as a PNG file
    plt.savefig('first_nsfg_hist.png')
    # Save the histogram as a PDF file
    plt.savefig('first_nsfg_hist.pdf')

    # Display the plot
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


