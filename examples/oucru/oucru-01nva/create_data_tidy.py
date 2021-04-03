# Libraries
import textwrap
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# DataBlend Libraries
from datablend.core.blend.blender import Blender
from datablend.core.repair.correctors import oucru_correction
from datablend.core.repair.schema import SchemaCorrectionTidy

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path to config file
yaml_datablend = '{0}/{1}'.format(curr_path, './datablend.yaml')
yaml_corrector = '{0}/{1}'.format(curr_path, '../corrector.yaml')


# ----------------------------------
# Create tidy format
# ----------------------------------
# Create blender
blender = Blender(
    filepath=yaml_datablend,
    curr_path=curr_path)

# Create tidy data
tidy, duplicated = blender._tidy_from_config()

# Save tidy data
tidy.to_csv(blender.bc.filepath_tidy(), index=False)

# ----------------------------------
# Create tidy format corrected
# ----------------------------------
# .. note: Should we ready directly the csv to ensure that
#          behaviour will be the same? The read_csv does
#          some dtype transformations.

# Read data
original = pd.read_csv(blender.bc.filepath_tidy(),
    parse_dates=['date'],
    dtype={'body_temperature': 'Float64'})

# Create tidy
tidy = original.copy(deep=True)

# Create corrector
corrector = \
    SchemaCorrectionTidy(filepath=yaml_corrector)

# Apply corrections
tidy, corrections = \
    corrector.transform(tidy, report_corrections=True)

# Apply OUCRU corrections
tidy = oucru_correction(tidy)

# Define filename
filename = '{0}/{1}.csv'.format(
    blender.bc.filepath_datasets(),
    blender.bc.filename(mode='tidy', add='corrected'))


# Save tidy corrected
tidy.to_csv(filename, index=False)

# --------------------------------------------------------
# Reports
# --------------------------------------------------------

"""
# -----------------------
# Yaml config (DataFrame)
# -----------------------
# Get configuration report
summary = bc.features_summary(tidy)

# Define filename
filename = '{0}/{1}.csv'.format(
    bc.filepath_reports(),
    bc.filename(mode='tidy', add='corrections_summary'))

# Save
summary.to_csv(filename, index=False)

# -----------------------
# Corrections
# -----------------------
# Import library
from datablend.utils.pandas import save_df_dict

# Save all worksheets separated in same xlsx file.
save_df_dict(corrections, filepath=bc.filepath_reports(),
    filename=bc.filename(mode='tidy', add='corrections'),
    extension='xlsx', index=False)

# -----------------
# Comparison (txt)
# -----------------
# Create report
report = report_tidy_corrections(orig, tidy)

# Define filename
filename = '{0}/{1}.txt'.format(
    bc.filepath_reports(),
    bc.filename(mode='tidy', add='comparison'))

# Save it
with open(filename, "w") as text_file:
    print(report, file=text_file)

# ----------------------
# Describe (summary)
# ----------------------
# Create description
description = describe(tidy)

# Define filename
filename = '{0}/{1}.csv'.format(
    bc.filepath_reports(),
    bc.filename(mode='tidy', add='description'))

# Save
description.to_csv(filename)


# --------------------------------
# Pandas-profile (HTML)
# ---------------------------------
# Libraries
from pandas_profiling import ProfileReport

# Generate report
profile = ProfileReport(tidy, title='OUCRU - 13dx_corrected')

# Create report
filename = '{0}/{1}.html'.format(
    bc.filepath_reports(),
    bc.filename(mode='tidy', add='profile'))

# Save as HTML
profile.to_file(filename)
"""