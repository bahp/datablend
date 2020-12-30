# Libraries
import textwrap
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path

from datablend.utils.methods import stacked_display

# -----------------------------------
# Configuration
# -----------------------------------
# Configuration
pd.set_option("display.max_rows", None,
              "display.max_columns", None)

# Matplotlib params
mplconfig = {
    'font.size': 8,
    'figure.titlesize': 15,
    'ytick.labelsize': 5,
    'axes.titlesize': 8,
    'axes.titlepad': 3
}

matplotlib.rcParams.update(mplconfig)

# -----------------------------------
# Constants
# -----------------------------------

# --------------------------
# Plot
# --------------------------
def get_layout(nelements, nrows=10):
    ncols = (nelements // nrows)  # Rows
    ncols += bool(nelements % nrows)  # offset
    return nrows, ncols


# Load tidy dataframe
tidy = pd.read_csv('./resources/outputs/32dx-combined-books.csv')

# Get DataFrames for individual patients
groups = tidy.groupby(by='study_no')

# Plot DataFrames for each patient
for i, (sn, aux) in enumerate(tidy.groupby(by='study_no')):

    # Information
    print("%s/%s. Plotting patient: %s" % (i + 1, len(groups), sn))

    # Format dataframe
    aux.set_index('date', inplace=True)

    # Select numbers
    numbers = aux.select_dtypes(['bool', 'number']).astype('float')

    # Plot numbers
    axes = numbers.plot(subplots=True, sharex=True, kind='bar',
                        legend=False, grid=True, figsize=(16, 8),
                        layout=get_layout(len(numbers.columns)),
                        title=numbers.columns.tolist())

    """
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

    for i, v in enumerate(y):
        plt.text(xlocs[i] - 0.25, v + 0.01, str(v))
    """

    # Configure axes
    for ax in axes.flatten():
        # Axes configuration
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.grid(linestyle='--', linewidth=0.25)
        ax.set_ylim(ymin=0)

        # Display histogram values
        for rect in ax.patches:
            height = rect.get_height()
            if height == 0:
                continue
            ax.text(rect.get_x() + rect.get_width() / 2, height + 0.05, int(height),
                    ha='center', va='bottom', fontsize=2)

    # Config plot
    plt.tight_layout()
    plt.subplots_adjust(left=0.04, right=0.98,
                        hspace=0.8, wspace=0.4,
                        top=0.90)
    plt.suptitle('Patient: %s' % sn)

    # Save
    #plt.savefig("./32dx/figures/%s.pdf" % sn, dpi=150)

    if i > 1:
        break

plt.show()