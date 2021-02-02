"""
Consistent columns (bool_level)
===============================
"""
# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend
from datablend.core.repair.correctors import bool_level_correction

# -----------------------------
# Main
# -----------------------------
# Possible values
booleans = [False, True, None]
numbers = [0, 1, 2, 3, None]

# Product
matrix = product(booleans, numbers)

# Combinations
data = pd.DataFrame(matrix,
    columns=['abdominal_pain',
             'abdominal_pain_level'])

# Corrections
correction = bool_level_correction(
    data.copy(deep=True),
    sbool='abdominal_pain',
    slevel='abdominal_pain_level')

# Show data any
print("\nNote: When both abdominal_pain (bool) and abdominal_pain_level\n "
      "(int) are both None, the resulting value is False and 0\n "
      "respectively. They could/should be left as None.")

print("\nData:")
print(data)
print("\nCorrections:")
print(correction)