"""


see:  https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/index.html
"""

# Libraries
import numpy as np
import pandas as pd

# Specific libraries
from pathlib import Path

# Pandas profiling
from pandas_profiling import ProfileReport

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = Path(__file__).parent.absolute()

# Filename
filename = '13dx_data_tidy_raw'

# Path to save tidy data
path_tidy = '{0}/resources/outputs/datasets/{1}.csv'.format(
    curr_path, filename)


# -----------------------------------
# Main
# -----------------------------------
# Load tidy data
tidy = pd.read_csv(path_tidy,
    parse_dates=['date'])

# Generate report
profile = ProfileReport(tidy, title='OUCRU - 13Dx')

# Save as HTML
profile.to_file("{0}.html".format(filename))