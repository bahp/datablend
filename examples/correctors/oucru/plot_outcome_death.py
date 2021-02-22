"""
Fix outcome from event_death
============================
"""

# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend Library
from datablend.core.repair.correctors import oucru_outcome_death_correction

# -----------------------------
# Main
# -----------------------------
# .. note: According to our definition event_death
#          is only pd.NA or True. It is never false.
data = [
    ['0', None, None],
    ['1', None, None],
    ['2', None, None],
    ['2', None, True],
    ['3', 'Died', False],
    ['4', 'Died', True],
    ['5', 'Alive', True],
    ['6', 'Alive', False],
    ['7', 'Alive', None],
]

# -----------------------------
# event_death
# -----------------------------
# Combinations
data = pd.DataFrame(data,
    columns=['study_no',
             'outcome',
             'event_death'])

# Correction
correction = data.copy(deep=True)
correction = oucru_outcome_death_correction(correction)

# Show data any
print("\nNote:\nThe events columns as defined in oucru "
      "should never contain False values.\nSince they "
      "are only flagged when appearing in the spreadsheets "
      "and\ntherefore contain only True or pd.NA.")

print("\nData:")
print(data)
print("\nCorrection:")
print(correction)