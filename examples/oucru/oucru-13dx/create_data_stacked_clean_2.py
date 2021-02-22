# Libraries
import yaml
import pathlib
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend Libraries
from datablend.core import settings
from datablend.core.validation.reports import stack_validate
from datablend.core.validation.correctors import schema_correction_stack

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path to saved stacked data
path_stack = '{0}/resources/outputs/datasets'.format(curr_path)

# -----------------------------------
# Load data
# -----------------------------------
# Load data.
stack = pd.read_csv('%s/13dx_data_stacked_flat.csv' % path_stack,
        parse_dates=['date'])


# Keep original copy
original = stack.copy(deep=True)

# -----------------------------------
# Check all units are compatible
# -----------------------------------
# It validates:
#   - has_undefined_units
#   - has_duplicated_units_per_column
#   - schema_validate
# Call function
valid, checks, reports = stack_validate(
    stack=stack, unit_registry=settings.ureg,
    schema_json=settings.units)

# Show reports
for e in reports:
    print(e.report(verbose=1))


# --------------------------------
# Overall patient stay information
# --------------------------------
# Check overall dates.
print("Number of elements outside the 2010-2014 range: %s" \
    % (~stack.date.dt.year.between(2010, 2014)).sum())

# Path
path = './resources/outputs/description/'

"""
# Get summary information of stack
summary, features, dates = \
    report_stack_patients(stack)

# Information
summary.to_csv('%s/stack_summary.csv' % path)
features.to_csv('%s/stack_features.csv' % path)
dates.to_csv('%s/stack_dates.csv' % path)
"""

#hnos = ['6-0994', '16-0759', '2-0100', '2-0102']
#original = original[original.StudyNo.isin(hnos)]
#stack = stack[stack.StudyNo.isin(hnos)]

"""
# Correct date outliers
stack.date = \
    stack.groupby(by=['StudyNo']) \
         .date.transform(date_outliers_correction,
             max_days_to_median=15,
             outliers_as_nat=True)
"""
# --------------------------
# Apply corrections to data
# --------------------------
# Load DataBlend configuration
stream = open("datablend.yaml", 'r')
parsed = yaml.load(stream, Loader=yaml.FullLoader)

print(sorted(stack.column.unique()))

# Apply corrections
stack = schema_correction_stack(stack, parsed['features'])

# Include results and dates before correction
stack['result_old'] = \
    original.result.astype(str) \
        .compare(stack.result.astype(str)).self

stack['date_old'] = \
    original.date.astype(str) \
        .compare(stack.date.astype(str)).self

# Filter between 2010 and 2014.
# stack = stack[stack.date.dt.year.between(2010, 2014)]

# Save
stack.to_csv('%s/13dx_data_stacked_flat_corrected.csv' % path_stack)