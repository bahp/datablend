"""
Ensure range (range)
========================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import range_correction

# ------------------------
# Constants
# ------------------------
#
sample1 = pd.Series([1, 2, 3, np.nan, 2, 4, pd.NA])

# ------------------------
# Main
# ------------------------
# Correct
a = range_correction(sample1, range=(0, 5))
b = range_correction(sample1, range=(3, 4))
c = range_correction(sample1, range=(4, 3))
d = range_correction(sample1, range=(3, 4), value=333)

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample1, b], axis=1))
print("\n%s" % pd.concat([sample1, c], axis=1))
print("\n%s" % pd.concat([sample1, d], axis=1))
