# Libraries
import yaml
import pathlib
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend Libraries
from datablend.core import settings
from datablend.core.blend.config import BlenderConfig
from datablend.core.validation.reports import stack_validate
from datablend.core.validation.correctors import schema_correction_stack
from datablend.core.validation.correctors import date_outliers_correction
from datablend.core.repair.schema import SchemaCorrectionStack

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path to config file
yaml_datablend = '{0}/{1}'.format(curr_path, './corrector.yaml')
yaml_corrector = '{0}/{1}'.format(curr_path, '../corrector.yaml')

# Create the blender config
bc = BlenderConfig(yaml_datablend, curr_path)

# Path to saved stacked data
path = bc.filepath_datasets()


# -----------------------------------
# Load data
# -----------------------------------
# Path
filepath = bc.filepath_datasets()
filename = '13dx_data_stacked_flat.csv'

# Load data.
stack = pd.read_csv('%s/%s' % (filepath, filename),
    parse_dates=['date'])

# Keep original copy
original = stack.copy(deep=True)

# Correct date outliers
# .. note: Can be done through yaml??
stack.date = \
    stack.groupby(by=['study_no']) \
         .date.transform(date_outliers_correction,
             max_days_to_median=15,
             outliers_as_nat=True)

# --------------------------
# Apply corrections to data
# --------------------------
# Load DataBlend configuration
# Apply corrections
#stack = schema_correction_stack(stack, bc.features())

# Create schema corrector
schema_corrector = \
    SchemaCorrectionStack(filepath=yaml_corrector)

# Show schema transformations summary

# Correct schema
stack, report = \
    schema_corrector.transform(stack)



# Include results and dates before correction
stack['result_old'] = \
    original.result.astype(str) \
        .compare(stack.result.astype(str)).self

stack['date_old'] = \
    original.date.astype(str) \
        .compare(stack.date.astype(str)).self

# Filter between 2010 and 2014.
stack = stack[stack.date.dt.year.between(2010, 2014)]

# Drop those with nan values?

# Save
stack.to_csv('{0}/{1}.csv'.format(
    bc.filepath_datasets(),
    bc.filename(mode='stacked', add='corrected'),
))
