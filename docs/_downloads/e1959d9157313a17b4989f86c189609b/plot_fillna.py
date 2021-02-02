"""
Fill missing values (fillna)
============================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import fillna_correction

# ------------------------
# Constants
# ------------------------
#
sample1 = pd.Series([np.nan, 1, np.nan, 2, np.nan, np.nan, np.nan, 4])

# ------------------------
# Main
# ------------------------
# Correct
a = fillna_correction(sample1, method='ffill')
b = fillna_correction(sample1, method='bfill')
c = fillna_correction(sample1, method='fbfill')
d = fillna_correction(sample1, method='ffill', limit=1)

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample1, b], axis=1))
print("\n%s" % pd.concat([sample1, c], axis=1))
print("\n%s" % pd.concat([sample1, d], axis=1))