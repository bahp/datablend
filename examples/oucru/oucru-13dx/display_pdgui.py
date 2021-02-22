# Libraries
import pandas as pd

# Specific
from pathlib import Path
from pandasgui import show

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = Path(__file__).parent.absolute()

# Path to save tidy data
path_tidy = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '13dx_data_tidy_fmt.csv')

# -----------------------------------
# Main
# -----------------------------------
# Load
tidy = pd.read_csv(path_tidy, parse_dates=['date'])

# Format
tidy = tidy.convert_dtypes()

# Show interactive GUI
show(tidy)