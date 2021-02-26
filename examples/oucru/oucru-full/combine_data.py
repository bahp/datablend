# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path


# -----------------------------------
# Methods
# -----------------------------------
def combine_files(path_data, regexp='**/*.csv', **kwargs):
    """This method combines files in folder.

    Parameters
    ----------
    path_data: str
        The folder with the data files.

    Returns
    -------
        pd.DataFrame
    """
    # Information
    print("\nCombining files in '{0}'".format(path_data))

    # Initialise
    data = {}

    # Loop filling data
    for path in sorted(list(path_data.glob(regexp))):
        # Show information
        print("  Loading... %s" % path.stem)

        # Read and add source
        aux = pd.read_csv(path, **kwargs)
        aux['dsource'] = path.name.split("_")[0]
        aux['study_no'] = \
            aux['dsource'].astype(str) + '-' + \
            aux['study_no'].astype(str)

        # Add to dictionary
        data[path.name] = aux

    # Return
    return data


# -----------------------------------
# Configuration
# -----------------------------------

# -----------------------------------
# Constants
# -----------------------------------

# -------------------------------------------------------
# Main
# -------------------------------------------------------
# Path with data
path_stack = Path('./resources/datasets/stacked/')
path_tidy = Path('./resources/datasets/tidy/')
path_save = Path('./resources/datasets/combined/')

# Create folders if they dont exist
path_stack.mkdir(parents=True, exist_ok=True)
path_tidy.mkdir(parents=True, exist_ok=True)
path_save.mkdir(parents=True, exist_ok=True)

# ----------------------------------
# Copy files from ther oucru folders
# ----------------------------------
# .. TODO: Find the regular expression to exclude the
#          folder 'oucru-full' so that we do not need
#          to check in the for loop.
# Libraries
import shutil

# Define pattern
pattern = "!(test)/**/*_data_tidy_corrected.csv"


# Copy tidy files
for f in Path('../').glob('**/*data_tidy_corrected.csv'):
    if 'oucru-full' in str(f):
        continue
    shutil.copy(f, path_tidy)
    print("Copied file %s" % f)


# Copy stacked files
for f in Path('../').glob('**/*data_stacked_corrected.csv'):
    if 'oucru-full' in str(f):
        continue
    shutil.copy(f, path_stack)
    print("Copied file %s" % f)

# ----------------------------------
# Combine stacked
# ----------------------------------
# Initialise stacked
data_stacked = combine_files(
        path_data=path_stack,
        regexp='**/*stacked*.csv',
        parse_dates=['date'],
        low_memory=False)

# Combine
data_comb = pd.concat(data_stacked.values())

# Save stacked
data_comb.to_csv(
    '{0}/combined_stacked.csv'.format(path_save))


# ----------------------------------
# Read tidy
# ----------------------------------
# Initialise stacked
data_tidy = combine_files(
        path_data=path_tidy,
        parse_dates=['date'],
        regexp='**/*tidy*.csv',
        low_memory=False)

# ----------------------------------
# Combine tidy
# ----------------------------------
# Combine
data_comb = pd.concat(data_tidy.values())

# Save stacked
data_comb.to_csv(
    '{0}/combined_tidy.csv'.format(path_save))