"""
Fix pleural effusion (from sides)
=================================
"""

# Libraries
import numpy as np
import pandas as pd

# Specific
from itertools import product
from itertools import combinations

# DataBlend library
from datablend.core.repair.correctors import oucru_pleural_effusion_correction

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# pcr_dengue
# -----------------------------
# Possible values
pleural_effusion_left = [None, False, True]
pleural_effusion_right = [None, False, True]

# Product
matrix = product(pleural_effusion_left,
                 pleural_effusion_right)

# Combinations
data = pd.DataFrame(matrix,
    columns=['pleural_effusion_left',
             'pleural_effusion_right'])

# Correction
correction = data.copy(deep=True)
correction = oucru_pleural_effusion_correction(correction)

# Show data any
print("\nData:")
print(data)
print("\nCorrection:")
print(correction)