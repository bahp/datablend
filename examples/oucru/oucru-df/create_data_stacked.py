# Libraries
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# Specific libraries
from datablend.core.blend.blender import Blender
from datablend.core.widgets.format import FullTemplateWidget
from datablend.core.repair.schema import SchemaCorrectionStack

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path to config file
yaml_datablend = '{0}/{1}'.format(curr_path, './datablend.yaml')
yaml_corrector = '{0}/{1}'.format(curr_path, '../corrector.yaml')

# -------------------------------
# Main
# -------------------------------
# Create blender
blender = Blender(filepath=yaml_datablend,
                  curr_path=curr_path,
                  widgets=[FullTemplateWidget()])

# Fit the blender
blender = blender._fit_from_config()

# Stack data
stacked = blender._stack_from_config()

# The outputs are stored in disk.
#   resources/outputs/datasets
#   resources/outputs/reports
#   resources/outputs/templates


# --------------------------------
# Clean stacked
# --------------------------------
# Concatenate
stacked = pd.concat(stacked.values(), ignore_index=True)

# Keep original copy
original = stacked.copy(deep=True)

# Create schema corrector
schema_corrector = \
    SchemaCorrectionStack(filepath=yaml_corrector)

# Show schema transformations summary

# Correct schema
stacked, report = \
    schema_corrector.transform(stacked)

# ---------------------------------------------
# Manual unit correction, move to SchemaStacked
# ---------------------------------------------
# DataBlend library
from datablend.core.repair.correctors import unit_correction

# It is just for PLT
idxs =  (stacked.column=='plt') & (stacked.unit=='megacount/L')

# Manual corrections (to move to corrector stack schema if possible!)
stacked.loc[idxs, 'result'] = unit_correction(stacked[idxs].result,
    unit_from='megacount/L', unit_to='gigacount/L')
stacked.loc[idxs, 'unit'] = 'gigacount/L'
# ----------------------------------------------

# Include old results/dates before correction
stacked['result_old'] = \
    original.result.astype(str) \
        .compare(stacked.result.astype(str)).self

stacked['date_old'] = \
    original.date.astype(str) \
        .compare(stacked.date.astype(str)).self

# Filter between 2010 and 2014.
#stack = stack[stack.date.dt.year.between(2010, 2014)]

# Drop those with nan values?

# Save
stacked.to_csv('{0}/{1}.csv'.format(
    blender.bc.filepath_datasets(),
    blender.bc.filename(mode='stacked', add='corrected'),
))