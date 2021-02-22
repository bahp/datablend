"""
Ensure consistent value (static)
================================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import static_correction

# ------------------------
# Constants
# ------------------------
#
sample1 = pd.Series([1, 2, 3, 2, 4, 5])
sample2 = pd.Series([np.nan, np.nan, np.nan])
sample3 = pd.Series([np.nan, 4, np.nan])
sample4 = pd.Series([4, pd.NA, pd.NA])
sample5 = pd.Series([4, 4, pd.NA])
sample6 = pd.Series([4, 4, 4, 4])
sample7 = pd.Series([True, False, False, False])
sample8 = pd.Series(['True', 'False', 'False'])
sample9 = pd.Series([1.55, 2.28, 3.34])
sample10 = pd.Series(
    data=['Feo', 'Guapo', 'Feo', 'Feo'],
    index=[4, 8, 12, 24])

# ------------------------
# Main
# ------------------------
# Correct
a = static_correction(sample1, method='max')
b = static_correction(sample2, method='max')
c = static_correction(sample3, method='max')
h = static_correction(sample5, method='max')
i = static_correction(sample6, method='max')
j = static_correction(sample7, method='max')
k = static_correction(sample8, method='max')

d = static_correction(sample1, method='min')
e = static_correction(sample1, method='mode')
f = static_correction(sample1, method='mean')
g = static_correction(sample1, method='median')
l = static_correction(sample9, method='mean')
m = static_correction(sample10, method='mode')

# Show
print("\nMax:")
print("%s" % pd.concat([sample1, a], axis=1))
print("\n%s" % pd.concat([sample2, b], axis=1))
print("\n%s" % pd.concat([sample3, c], axis=1))
print("\n%s" % pd.concat([sample5, h], axis=1))
print("\n%s" % pd.concat([sample6, i], axis=1))
print("\n%s" % pd.concat([sample7, j], axis=1))
print("\n%s" % pd.concat([sample8, k], axis=1))

print("\nMin:")
print("%s" % pd.concat([sample1, d], axis=1))
print("\nMode:")
print("%s" % pd.concat([sample1, e], axis=1))
print("\nMean:")
print("%s" % pd.concat([sample1, f], axis=1))
print("\nMedian:")
print("%s" % pd.concat([sample1, g], axis=1))
print("\nMedian:")
print("%s" % pd.concat([sample9, l], axis=1))
print("\nMode:")
print("%s" % pd.concat([sample10, m], axis=1))