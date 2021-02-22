# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend
from datablend.core.settings import ureg
from datablend.utils.pandas import save_df_dict
from datablend.core.repair.schema import SchemaCorrectionTidy
from datablend.core.validation.reports import report_undefined_units
from datablend.core.validation.reports import report_stack_duplicated_units
from datablend.core.validation.reports import report_stack_feature_count
from datablend.core.validation.reports import report_stack_date_count
from datablend.core.validation.reports import report_stack_stay
from datablend.core.validation.reports import report_stack_units_per_dataset
from datablend.core.validation.reports import report_tidy_dtypes_per_dataset
from datablend.core.validation.reports import report_tidy_feature_count_per_dataset

# -----------------------------------
# Configuration
# -----------------------------------

"""
# -----------------------------------
# Constants
# -----------------------------------
# Path with data
path_data = Path('./resources/datasets/combined/combined_stacked.csv')


# ------------------------------
# Load data
# ------------------------------
# Load data
data = pd.read_csv(path_data, parse_dates=['date'])

# -------------------------------------------------
# Report duplicated units
# -------------------------------------------------
# Identify the different units that have been
# use for the features contained in the data.
#

# Check for the whole dataset
report = \
    report_stacked_duplicated_units(data)

# Show for combined
print("Investigating <combined>:\n")
print(str_df(report))

# Check for each subset.
if report.shape[0]:
    for i, df in data.groupby('dsource'):
        # Perform check
        report = report_stacked_duplicated_units(df)
        # Display report
        if report.shape[0]:
            print("\nInvestigating <{0}>:\n\n{1}\n"
                .format(i, str_df(report)))


# -------------------------------------------------
# Report units not existing in Pint
# -------------------------------------------------
# Import
from datablend.core.settings import ureg

# Create report
report = \
    

# Show
print("Unit report:\n")
print(str_df(report))
"""


# -----------------------------------
# Methods
# -----------------------------------
def corrections_summary(data):
    """

    Parameters
    ----------
    data

    Returns
    -------

    """
    # ---------------------
    # Automatic corrections
    # ---------------------
    # Path to config file
    yaml_corrector = '../corrector.yaml'

    # Create corrector
    corrector = SchemaCorrectionTidy(filepath=yaml_corrector)

    # ORder
    order = ['name', 'dtype', 'unit', 'included', 'transform']

    # Create report
    report = corrector.features_summary(data)
    report = report.drop(columns=['transformations'])
    report = report[order + list(report.columns.difference(set(order)))]
    report = report.set_index('name')

    # Return
    return report


# -----------------------------------
# Configuration
# -----------------------------------

# -----------------------------------
# Constants
# -----------------------------------

# -------------------------------------------------------
# Main
# -------------------------------------------------------
# Path with data
path_tidy = Path('./resources/datasets/combined/combined_tidy.csv')
path_stack = Path('./resources/datasets/combined/combined_stacked.csv')

# ------------------------------
# Load data
# ------------------------------
# Load data
stack = pd.read_csv(path_stack, parse_dates=['date'])

# Load
tidy = pd.read_csv(path_tidy,
                   parse_dates=['date'],
                   low_memory=False)

# Create report
report = {
    'corrections':      corrections_summary(tidy),
    'counts':           report_tidy_feature_count_per_dataset(tidy),
    'dtypes':           report_tidy_dtypes_per_dataset(tidy),
    'units':            report_stack_units_per_dataset(stack),
    'units_undefined':  report_undefined_units(stack.unit.unique(), ureg),
    'units_duplicated': report_stack_duplicated_units(stack),
    'count_feature':    report_stack_feature_count(stack, cpid='study_no'),
    'count_date':       report_stack_date_count(stack, cpid='study_no'),
    'stay':             report_stack_stay(stack, cpid='study_no')
}

# Save report
save_df_dict(report,
             filepath='./resources/reports',
             filename='report',
             extension='xlsx',
             flat=False)