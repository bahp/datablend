# Libraris
import numpy as np
import pandas as pd


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


# -----------------------------------
# Constants
# -----------------------------------
# Constants
NULL = [pd.NA, None, 'nan', np.nan]
BOOL = ['False', 'True', 'FALSE', 'TRUE', False, True]


# -----------------------------------
# Methods
# -----------------------------------
def schema_from_json(json):
    """This method creates an schema from json.

    Parameters
    ----------

    Returns
    -------
    """

    # Initialise schema
    s = []

    # Loop json records
    for record in json:

        # Get name
        name = record['name']

        if 'dtype' in record:

            # Numeric
            if (record['dtype'] == np.float64) | \
               (record['dtype'] == np.int64):

                if 'range' in record:
                    if 'absolute' in record['range']:
                        low, high, unit = record['range']['absolute']
                        s.append(Column(name, [InRangeValidation(low, high) |
                                               InListValidation(NULL)]))

            # Boolean
            elif record['dtype'] == np.bool:
                s.append(Column(name, [InListValidation(NULL) |
                                       InListValidation(BOOL)]))

            else:
                if 'categories' in record:
                    categories = record['categories']
                    s.append(Column(name, [InListValidation(NULL) |
                                           InListValidation(categories)]))


    # Return
    return Schema(s)