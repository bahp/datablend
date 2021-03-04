"""
Create dengue interpretation
============================
"""

# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend library
from datablend.core.repair.correctors import oucru_serology_interpretation_feature
from datablend.core.repair.correctors import oucru_serology_single
from datablend.core.repair.correctors import oucru_serology_paired

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# Example I: serology_single
# -----------------------------
# .. note: What if 'Equivocal,Positive' present?

# Possible values
igm_interpretation = ['Positive', 'Negative', 'Equivocal', None]
igg_interpretation = ['Positive', 'Negative', 'Equivocal', None]

# Product
matrix = product(igm_interpretation, igg_interpretation)

# Combinations
data = pd.DataFrame(matrix,
    columns=['igm_interpretation',
             'igg_interpretation'])

# Correction
correction = data.copy(deep=True)
correction['serology_single'] = \
    oucru_serology_single(data)

# Show data any
print("\n\n" + "-"*80)
print("Serology Single")
print("-"*80)
print("\nData:")
print(data)
print("\nCorrection:")
print(correction.to_string())

# -----------------------------
# Example II: serology_paired
# -----------------------------
# Show data
print("\n\n" + "-"*80)
print("Serology Paired")
print("-"*80)

# Path to data (create fake data?)
path = '../../oucru/oucru-full/resources/datasets/'
#path+= 'tidy/42dx_data_tidy_corrected.csv'
path+= 'combined/combined_tidy.csv'

# Columns that are required (for visualization mainly)
columns = [
    'study_no',
    'date',
    'igm_interpretation',
    'igg_interpretation',
#    'serology_interpretation'
]

# Load data
data = pd.read_csv(path, parse_dates=['date'])

# Intersection of columns
columns = set(columns).intersection(data.columns)

# Filter
data = data[columns]
data = data.drop_duplicates()

# Compute serology interpretation
data = \
    oucru_serology_interpretation_feature(data)

# Show data
print("\nData:")
print(data[columns])

# Show unique values
print("\nUnique values:")
if 'igm_interpretation' in data:
    print('\nigm:')
    print(data.igm_interpretation.value_counts())
if 'igg_interpretation' in data:
    print('\nigg:')
    print(data.igg_interpretation.value_counts())
if 'serology_single' in data:
    print("\nSerology single:")
    print(data.serology_single.value_counts())
if 'serology_paired' in data:
    print("\nSerology paired:")
    print(data.serology_paired.value_counts())
if 'serology_single_interpretation' in data:
    print("\nSerology single interpretation:")
    print(data.serology_single_interpretation.value_counts())
if 'serology_paired_interpretation' in data:
    print("\nSerology paired interpretation:")
    print(data.serology_paired_interpretation.value_counts())
if 'serology_interpretation' in data:
    print("\nSerology interpretation:")
    print(data.serology_interpretation.value_counts())

# Show corrected
print("\nCorrected:")
print(data)

import numpy as np

a = data.groupby('study_no')\
    .serology_interpretation \
    .agg(nunique='nunique',
         unique=lambda x: sorted(x.astype('str').unique()))
a.to_csv('counts.csv')

def f(x):
    print(x)
    import sys
    sys.exit()

from datablend.core.repair.correctors import mode

a = data.groupby('study_no')\
    .serology_interpretation.apply(mode)
a.to_csv('counts2.csv')

a = data.groupby('study_no')\
    .serology_interpretation.last()
a.to_csv('counts2.csv')