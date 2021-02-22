# Libraries
import pathlib
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend Libraries
from datablend.core import settings
from datablend.core.validation.reports import stack_validate


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
# Create empty data
stack = pd.DataFrame()

# Read all files
for path in list(Path(path_stack).glob('**/*_stacked_*.csv')):
    stack = stack.append(pd.read_csv(path, parse_dates=['date']))


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
