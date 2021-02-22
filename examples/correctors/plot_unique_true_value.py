"""
Ensure only one True (unique_true)
==================================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import unique_true_value_correction

# ------------------------
# Constants
# ------------------------
# Samples
sample1 = pd.Series([np.nan, True, np.nan, np.nan, True])
sample2 = pd.Series([np.nan, 1, True, np.nan, True])
sample3 = pd.Series([np.nan, 'TRUe', True, np.nan, True])
sample4 = pd.Series([np.nan, 'Y', True, np.nan, True])
sample5 = pd.Series([np.nan, True, 1, 0, True, 'no boolean'])
sample6 = pd.Series([np.nan, True, False, True, False, False])

# ------------------------
# Main
# ------------------------
# Correct
a = unique_true_value_correction(sample1, keep='first')
b = unique_true_value_correction(sample1, keep='last')
c = unique_true_value_correction(sample2, keep='first')
d = unique_true_value_correction(sample3, keep='first')
e = unique_true_value_correction(sample4, keep='first')
#f = unique_true_value_correction(sample5, keep='first') # raise error
g = unique_true_value_correction(sample6, keep='first')

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample1, b], axis=1))
print("\n%s" % pd.concat([sample2, c], axis=1))
print("\n%s" % pd.concat([sample3, d], axis=1))
print("\n%s" % pd.concat([sample4, e], axis=1))
print("\n%s" % pd.concat([sample6, g], axis=1))