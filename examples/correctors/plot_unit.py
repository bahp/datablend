"""
Ensure range (range)
========================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import unit_correction

# ------------------------
# Constants
# ------------------------
#
sample1 = pd.Series([1, 2, 3, np.nan, 2, 4, pd.NA])
sample2 = pd.Series([350, 11600, 300000, np.nan, 200000, pd.NA])

# ------------------------
# Main
# ------------------------
# Correct
a = unit_correction(sample1, unit_from='gigacount/L', unit_to='megacount/L')
b = unit_correction(sample2, unit_from='megacount/L', unit_to='gigacount/L')

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample2, b], axis=1))