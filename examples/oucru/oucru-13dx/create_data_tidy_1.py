# Libraries
import textwrap
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# Specific libraries
from pathlib import Path

# DataBlend Libraries
from datablend.core import settings
from datablend.utils.logger import load_logger
from datablend.utils.display import str_dtypes
from datablend.utils.display import str_description
from datablend.utils.display import describe

from datablend.core.widgets.tidy import StaticTidyWidget
from datablend.core.widgets.tidy import DefaultTidyWidget

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
path_tidy_raw = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '13dx_data_tidy_raw.csv')

# Path to save tidy data
path_tidy_fmt = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '13dx_data_tidy_fmt.csv')

# -----------------------------------
# Main
# -----------------------------------
# Create empty data
data = pd.DataFrame()

# Read all files
for path in list(Path(path_stack).glob('**/*_stacked_*.csv')):
    data = data.append(pd.read_csv(path))

# Basic formatting
if 'unit' in data:
    data = data.drop(columns=['unit'])
data.date = pd.to_datetime(data.date)
data.date = data.date.dt.date
data = data.sort_values(by=['StudyNo', 'date', 'column'])
# data = data.convert_dtypes() # is it really needed?

# Fixes
data = data.replace({'result': {'False': False, 'True': True}}) # Quick fix str and bool (True False issue)
data = data.drop_duplicates() # Important after modifications

# Convert to tidy format
tidy = data.copy(deep=True)
tidy = tidy.set_index(['StudyNo', 'date', 'column'])

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

# Save raw tidy.
tidy.to_csv(path_tidy_raw, index=False)

# Save raw tidy summary
describe(tidy).to_csv(str(path_tidy_raw.replace(".csv", '_describe.csv')))


# --------------------------
# Format
# --------------------------
# Load tidy data
tidy = pd.read_csv(path_tidy_raw,
    parse_dates=['date'],
    dtype={'anorexia': 'boolean'})

# Load template
template = pd.DataFrame(settings.units)
template['from_name'] = template['name']
template = template.rename(columns={'name': 'to_name'})

# ----------
# Set static
# ----------
# Set all variables that remain constant during the study
tidy = StaticTidyWidget(by='StudyNo').fit_transform(template, tidy)

# ------------
# Set defaults
# ------------
# This variables indicate
#   - levels, if np.nan then 0.
#   - events, if np.nan then False.
#defaults = {c: 0 for c in tidy.columns if 'level' in c} # careful with care level!
defaults = {}
defaults.update({c: False for c in tidy.columns if 'event' in c})

# Add defaults
tidy = DefaultTidyWidget().fit_transform(template, tidy)
tidy = DefaultTidyWidget().transform(tidy, defaults)

# -------------------------------------------
# Set bleeding
# -------------------------------------------
# Bleeding can be defined as:
bleeding = tidy.bleeding_gi | \
           tidy.bleeding_gum | \
           tidy.bleeding_mucosal | \
           tidy.bleeding_nose | \
           tidy.bleeding_skin | \
           tidy.bleeding_urine | \
           tidy.bleeding_vaginal | \
           tidy.bleeding_vensite

# Fill missing bleeding
tidy.bleeding = tidy.bleeding.fillna(bleeding)

# Bleeding Comparison
bldcmp = tidy[['StudyNo', 'date']].copy(deep=True)
bldcmp['computed'] = bleeding
bldcmp['recorded'] = tidy.bleeding

# Find inconsistencies
# What if computed True but recorded False?
# What if computed False but recorded True?
idxs = bldcmp.computed != bldcmp.recorded

# Show inconsistencies
logger.info("\n" + "="*80)
logger.info("The following <bleeding> inconsistencies were found:")
logger.info("\n\n\t{0}\n".format(bldcmp[idxs]
                         .to_string().replace('\n', '\n\t')))
logger.info("="*80)

# -------------------------------------------
# Set bleeding severe
# -------------------------------------------

# -------------------------------------------
# Set complications
# -------------------------------------------
# Complications can be defined as:
tidy['complications'] = \
    tidy.bleeding_severe | \
    tidy.shock | tidy.shock_multiple | \
    tidy.pleural_effusion


# -----------------
# Fix shock
# -----------------
tidy.shock = tidy.shock.fillna(False)

# -----------------
# Fix ages
# -----------------
# Fix age
tidy.age = tidy.age.replace({-1: pd.NA})

# ------------
# Mege skins?
# ------------
# clammy, flush, rash

# restlessness, lethargy?

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

tidy = tidy.convert_dtypes()

# Save
tidy.to_csv(path_tidy_fmt, index=False)

# Save raw tidy summary
describe(tidy).to_csv(str(path_tidy_fmt.replace(".csv", '_describe.csv')))

# --------------------------
# Show information
# --------------------------
# Load
tidy = pd.read_csv(path_tidy_fmt)

# Show
#print(str_dtypes(tidy))

# Show
#print(str_dtypes(settings.prefix_sources(tidy)))