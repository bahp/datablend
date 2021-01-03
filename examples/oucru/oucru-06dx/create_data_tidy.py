# Libraries
import pathlib
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend Libraries
from datablend.utils.logger import load_logger
from datablend.utils.display import str_dtypes
from datablend.core import settings

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path to saved stacked data
path_stack = '{0}/resources/outputs/datasets/'.format(curr_path)

# Path to save tidy data
path_tidy = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '06dx_data_tidy.csv')


# -----------------------------------
# Main
# -----------------------------------
# Create empty data
data = pd.DataFrame()

# Read all files
for path in list(Path(path_stack).glob('**/*_stacked_*.csv')):
    data = data.append(pd.read_csv(path))

# Basic formatting
data = data.drop(columns=['unit'])
data.date = pd.to_datetime(data.date)
data.date = data.date.dt.date
data = data.convert_dtypes()
data = data.drop_duplicates()
data = data.sort_values(by=['study_no', 'date', 'column'])

# Convert to tidy format
tidy = data.copy(deep=True)
tidy = tidy.set_index(['study_no', 'date', 'column'])

# Look for index duplicates
duplicates = tidy.index.duplicated(keep=False)

# Logging information
logger.info("=" * 80)
logger.info("The data size: %s", str(data.shape))
logger.info('The following duplicates were found:\n\n\t%s\n', \
    tidy[duplicates].to_string().replace('\n', '\n\t\t'))
logger.info("=" * 80)

# Keep only last row
tidy = tidy[~tidy.index.duplicated(keep='last')]  # keep only last row
tidy = tidy.unstack(level=2)  # Unstack
tidy.columns = tidy.columns.droplevel(level=0)  # Drop...
tidy = tidy.reset_index()

# --------------------------
# Format
# --------------------------

# Set static
# ----------
# Features that do not change over time the course of the admission.
static = ['gender', 'age', 'diabetes', 'height', 'pregnant',
          'weight', 'anemia', 'asthma', 'coronary_heart_disease',
          'hypertension', 'peptic_ulcer', 'chronic_hepatitis',
          'renal_disease']

for c in static:
    if c in tidy:
        tidy[c] = tidy.groupby(by='study_no')[c].ffill()
        tidy[c] = tidy.groupby(by='study_no')[c].bfill()

# Set Levels
# ----------
# Features in which level is indicated with a number. Thus if no
# level indicated (np.nan) then the level is 0.
levels = [c for c in tidy.columns if 'level' in c]

# When setting an integer 0 it was sometimes
# raising an error not possible to assign int
# to string array...
tidy[levels] = tidy[levels].fillna('0')

# Date of onset
# -------------
# For some parameters, it is indicated the date of onset.
#
# The dataset is a combination of history, examination and
# resources_evolution spreadsheets. Thus the following assumptions
# are made.
#
# - We use bfill for those results in which the first value
#   is False. This means that if the value obtained on
#   examination was false there was no previous symptoms
#   of such either.
#
#
onset = ['chills', 'anorexia', 'nausea', 'vomiting', 'diarrhoea',
         'sore_throat', 'cough', 'bleeding_skin', 'feeling_faint']

for c in onset:
    if c in tidy:
        tidy[c] = tidy[c].ffill()

# Date admission / discharge
# --------------------------

# Haematocrit
# ------------
# Fill with max or min


# Save
tidy.to_csv(path_tidy, index=False)

# Load
tidy = pd.read_csv(path_tidy)

# Show
logger.info(str_dtypes(tidy))

# Show
#print(str_dtypes(settings.prefix_sources(tidy)))