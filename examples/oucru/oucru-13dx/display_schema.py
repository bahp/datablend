# Libraries
import numpy as np
import pandas as pd

# Specific
from pathlib import Path

# Libraries from datablend
from datablend.core import settings

# Libraries from pandas_schema
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation
from pandas_schema.validation import TrailingWhitespaceValidation
from pandas_schema.validation import CanCallValidation
from pandas_schema.validation import CanConvertValidation
from pandas_schema.validation import MatchesPatternValidation
from pandas_schema.validation import IsDistinctValidation
from pandas_schema.validation import IsDtypeValidation
from pandas_schema.validation import InRangeValidation
from pandas_schema.validation import InListValidation


# FeatureRegistry()

# -----------------------------------
# Methods
# -----------------------------------
def schema_from_json(json):

    # Initialise schema
    s = []

    # Loop json records
    for record in json:
        # Get name
        name = record['name']
        # Construct validators
        if 'range' in record:
            if 'absolute' in record['range']:
                low, high, unit = record['range']['absolute']
                s.append(Column(name, [InRangeValidation(low, high) | InListValidation(NULL)]))
        if 'categories' in record:
            categories = record['categories']
            s.append(Column(name, [InListValidation(categories) | InListValidation(NULL)]))



    # Return
    return Schema(s)


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
# Constants
NULL = [pd.NA, None, 'nan', np.nan]

# Load tidy data
tidy = pd.read_csv(path_tidy, parse_dates=['date'])

# Create schema from json information
schema = schema_from_json(settings.units)

"""
# Create schema
schema = Schema([
    #Column('Given Name', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
    #Column('Family Name', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
    #Column('Customer ID', [MatchesPatternValidation(r'\d{4}[A-Z]{4}')])
    Column('age', [InRangeValidation(0, 100) | InListValidation(NULL)]),
    #Column('gender', [InListValidation(['Male', 'Female']) | InListValidation(NULL)]),
    #Column('body_temperature', [InRangeValidation(30, 45) | InListValidation(NULL)])
])
"""

# Common columns
columns_schema = set([c.name for c in schema.columns])
columns_tidy = set(tidy.columns)

# Find errors
errors = schema.validate(tidy,
    columns=columns_schema.intersection(columns_tidy))

#df = pd.DataFrame(errors)

#print(df)

# Show errors
for error in errors:
    print(error)