"""
Fix shock, multiple and event_shock
===================================
"""

# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend Library
from datablend.core.repair.correctors import oucru_shock_correction

# -----------------------------
# Main
# -----------------------------
data = [
    ['0', None, None, None],
    ['1', None, None, True],
    ['2', None, None, None],
    ['2', None, None, True],
    ['2', None, None, True],
    ['3', None, True, None],
    ['4', False, True, None],
    ['5', True, False, None],
    ['6', True, False, True],
    ['7', True, False, True],
    ['7', True, False, True],
    ['8', False, True, None],
    ['9', None, True, None],
    ['10', pd.NA, pd.NA, pd.NA]
]

# -----------------------------
# pcr_dengue
# -----------------------------
# Combinations
data = pd.DataFrame(data,
    columns=['study_no',
             'shock',
             'shock_multiple',
             'event_shock'])

#data = data.drop(columns=['shock'])

# Correction
correction = data.copy(deep=True)
correction = oucru_shock_correction(correction)

# Show data any
print("\nData:")
print(data)
print("\nCorrection:")
print(correction)