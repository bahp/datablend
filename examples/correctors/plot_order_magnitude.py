"""
Repair order of magnitude (order)
==================================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import order_magnitude_correction

# ------------------------
# Constants
# ------------------------
#
sample1 = pd.Series([30, 35.5, 37.4, np.nan, 376, 3600, pd.NA])

# ------------------------
# Main
# ------------------------
# Correct
a = order_magnitude_correction(sample1, range=(30, 45))
b = order_magnitude_correction(sample1, range=(30, 45), orders=[10])

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample1, b], axis=1))