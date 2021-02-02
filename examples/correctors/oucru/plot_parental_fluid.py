"""
Fix parental fluid and load (mL)
=================================
"""

# Libraries
import numpy as np
import pandas as pd

# Specific
from itertools import product
from itertools import combinations

# DataBlend library
from datablend.core.repair.correctors import oucru_parental_fluid_correction

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# pcr_dengue
# -----------------------------
# Possible values
parental_fluid = [None, False, True]
parental_fluid_volume = [None, 0, 500]

# Product
matrix = product(parental_fluid, parental_fluid_volume)

# Combinations
data = pd.DataFrame(matrix,
    columns=['parental_fluid', 'parental_fluid_volume'])

# Correction
correction = data.copy(deep=True).drop(columns=['parental_fluid'])
correction = oucru_parental_fluid_correction(correction)

# Show data any
print("\nData:")
print(data)
print("\nCorrection:")
print(correction)