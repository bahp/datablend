"""
Create dengue interpretation
============================
"""

# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend library
from datablend.core.repair.correctors import oucru_ns1_interpretation_feature

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# Example I: serology_single
# -----------------------------
# .. note: What if 'Equivocal,Positive' present?

# Possible values
values = ['Positive', 'Negative', 'Equivocal', None]

# Product
matrix = product(values,
                 #values,
                 #values,
                 values)

# Combinations
data = pd.DataFrame(matrix,
    columns=['ns1_interpretation',
             #'ns1_platelia_interpretation',
             #'ns1_plasma_interpretation',
             'ns1_urine_interpretation'])

# Correction
correction = data.copy(deep=True)
correction['ns1_interpretation_bool'] = \
    oucru_ns1_interpretation_feature(data)

# Show data any
print("\n\n" + "-"*80)
print("NS1 interpretation")
print("-"*80)
print("\nData:")
print(data)
print("\nCorrection:")
print(correction.to_string())