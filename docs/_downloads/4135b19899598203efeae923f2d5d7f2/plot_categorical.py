"""
Ensure categories (category)
============================
"""
# Import
import numpy as np
import pandas as pd

# Specific
from itertools import product
from itertools import combinations

# DataBlend library
from datablend.core.repair.correctors import categorical_correction

# -----------------------------
# Main
# -----------------------------
# Define categories
categories = ['DENV-1', 'DENV-2']

# -----------------------------
# pcr_dengue
# -----------------------------
# Possible values
pcr_dengue_serotype = [None,
                       pd.NA,
                       'DENV-1',
                       'DENV-2',
                       'DENV-8']

# Product
matrix = product(pcr_dengue_serotype,
                 pcr_dengue_serotype)

# Combine as strings
matrix = [','.join(map(str, tup)) for tup in matrix]

# Data
data1 = pd.Series(pcr_dengue_serotype)
data2 = pd.Series(matrix)
data3 = data1.append(data2)

# Corrections
correction1 = categorical_correction(data1,
    categories=categories, errors='coerce')

correction2 = categorical_correction(data2,
    categories=categories, errors='coerce',
    allow_combinations=True)

correction3 = categorical_correction(data3,
    categories=categories, errors='coerce',
    allow_combinations=True)

# Show
print("\nNote: The categorical_corrector is still being developed. In\n"
      "particular it does not raise errors and it assumes that\n"
      "allow_combinations=True (ignore correction 4).")
print("\n%s" % pd.concat([data1, correction1], axis=1))
print("\n%s" % pd.concat([data2, correction2], axis=1))
print("\n%s" % pd.concat([data3, correction3], axis=1))