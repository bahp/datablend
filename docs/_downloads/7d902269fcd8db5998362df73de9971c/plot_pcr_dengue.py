"""
Fix PCR dengue (load, sero and out)
===================================
"""

# Libraries
import numpy as np
import pandas as pd

# Specific
from itertools import product
from itertools import combinations

# DataBlend library
from datablend.core.repair.correctors import oucru_pcr_dengue_correction

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# pcr_dengue
# -----------------------------
# Possible values
pcr_dengue_load = [None, 0, 1000]
pcr_dengue_serotype = [None, '<LOD', 'DENV-1']
pcr_dengue_interpretation = [None, 'Confirmed', 'Suspected']

# Product
matrix = product(pcr_dengue_load,
                 pcr_dengue_serotype,
                 pcr_dengue_interpretation)

# Combinations
data = pd.DataFrame(matrix,
    columns=['pcr_dengue_load',
             'pcr_dengue_serotype',
             'pcr_dengue_interpretation'])

# Correction
correction = data.copy(deep=True)
correction = oucru_pcr_dengue_correction(correction)

# Show data any
print("\nData:")
print(data)
print("\nCorrection:")
print(correction)