"""
Ensure dtype (dtype)
===========================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import dtype_correction

# ------------------------
# Constants
# ------------------------
# Examples
sample0 = pd.Series([0, 1, 0, 1, None, pd.NA])                 # boolean
sample1 = pd.Series([True, False, True, None])                 # boolean
sample2 = pd.Series([1, 0, True, False,
    'True', 'False', 'Yes', 'No',
    'TRuE', 'FaLSE', 'Y', 'N', None, pd.NA])                   # boolean
sample5 = pd.Series([0, 1, 5, '12', '33', None, pd.NA])        # integers
sample6 = pd.Series([0, 4, 4.8, '12.24', '33.2', None, pd.NA]) # float
sample7 = pd.Series([0, 'not number', 4, 28, 23, None, pd.NA]) # Coerce

# ------------------------
# Main
# ------------------------
# Correct
bool1 = dtype_correction(sample0, dtype='boolean')
bool2 = dtype_correction(sample1, dtype='boolean')
bool3 = dtype_correction(sample2, dtype='boolean', errors='coerce')

num1 = dtype_correction(sample5, dtype='Int64', errors='coerce')
num2 = dtype_correction(sample6, dtype='Int64', errors='coerce')
num3 = dtype_correction(sample7, dtype='Int64', errors='coerce')

# Show
print("\nNote: If series has decimal values the returned series\n "
      "(num2) will also contain decimal values even when Int64\n "
      "is specified.")

print("\nNote: Coerce with booleans will transform Yes/No, Y/N\n "
      "and others to boolean. However, it will raise an exception\n "
      "when values (e.g. numbers) cant be cast to boolean.")

print("\n%s" % pd.concat([sample0, bool1], axis=1))
print("\n%s" % pd.concat([sample1, bool2], axis=1))
print("\n%s" % pd.concat([sample2, bool3], axis=1))

print("\n%s" % pd.concat([sample5, num1], axis=1))
print("\n%s" % pd.concat([sample6, num2], axis=1))
print("\n%s" % pd.concat([sample7, num3], axis=1))