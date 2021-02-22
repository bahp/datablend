# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend library
from datablend.core.validation.reports import str_df
from datablend.core.validation.reports import report_undefined_units
from datablend.core.validation.reports import report_stacked_duplicated_units

# -----------------------------------
# Configuration
# -----------------------------------

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
    report_undefined_units(data.unit.unique(), ureg)

# Show
print("Unit report:\n")
print(str_df(report))


# -------------------------------------------------
# Warn of possible wrong units based on data
# -------------------------------------------------

import yaml

# Read yaml configuration
configuration = yaml.load(open('../corrector.yaml', 'r'),
                          Loader=yaml.FullLoader)

# Set as dictionary for simplicity
features_ = {r['name']: r for r in configuration['features']}

# Keep only rows with unit
data = data[data.unit.notna()]

# Features
f = ['age', 'dbp', 'albumin']

# Example
#data = data[data.column.isin(f)]

m = {
    'age': [0, 120, 'year'],
    'creatine_kinase': [0, 9999, 'U/L'],
    'dbp': [40, 90, 'mmHg'],
    'albumin': [3.5, 4.8, 'g/dL']
}
"""
ref1: [35, 55, g / L]  # wiki | scymed
ref2: [3.5, 4.8, g / dL]  # wiki
ref3: [540, 740, umol / L]  # wiki
"""
# Library
import numpy as np
from pint import UnitRegistry
from datablend.core.settings import ureg

import warnings
warnings.simplefilter("ignore")



msg = "{0:5} | {1:10} | from: {2:5} | to: {3:5} |"
msg+= " [{4}, {5}] | % out is {6:.0f} | {7}"

TICK = u'\u2713'

r = pd.DataFrame()

# Group by
for (f, unit_from, dataset), df in data.groupby(['column', 'unit', 'dsource']):

    if not f in features_:
        continue
    if not 'range' in features_[f]:
        continue



    # Max and min
    #mn, mx = np.max(values), np.min(values)

    # Values to compare
    values = pd.to_numeric(df.result.dropna()).values

    if len(values) == 0:
        continue

    mn, mx = min(values), max(values)

    for name, (low, high, unit_to) in features_[f]['range'].items():

        if name != 'absolute':
            continue

        try:

            #print(f, name, unit_from, unit_to)


            # Convert to unit
            v = (values * ureg(unit_from)).to(unit_to)

            # Check in between
            between = pd.Series(v).between(low, high)

            # Compute percent
            percent = ((~between).sum() * 100) / between.size

            # Show
            status = 'good' if percent < 30 else 'bad'

            data = [dataset, f, name, unit_from, unit_to, low, high, mn, mx, percent, status]
            index = ['dataset', 'f', 'name', 'unit_from', 'unit_to', 'low', 'high', 'max', 'min', 'percent', 'status']

            #print(msg.format(dataset, f, unit_from, unit_to,
            #    low, high, percent, status))

            s = pd.Series(data=data, index=index).to_frame()


            r = pd.concat([r, s], axis=1)
        except Exception as e:
            print(e)


print(r.T)

aux = r.T

aux.to_csv('./resources/reports/units_ranges_stack.csv')


aux = aux.drop(columns=['percent'])
aux = aux.set_index(['f', 'name', 'unit_from', 'unit_to', 'low', 'high', 'max', 'min', 'dataset'])
aux = aux.unstack()

print(aux)

aux.to_csv('./resources/reports/units_ranges.csv')



