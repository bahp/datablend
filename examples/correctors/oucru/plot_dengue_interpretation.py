"""
Create dengue interpretation
============================
"""

# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend library
from datablend.core.repair.correctors import oucru_dengue_interpretation_feature

# -----------------------------
# Main
# -----------------------------

# -----------------------------
# pcr_dengue
# -----------------------------
# Possible values
pcr_dengue_serotype = [None, '<LOD', 'DENV-1', 'DENV-2', 'DENV-1,DENV-2']
ns1_interpretation = ['Positive', 'Negative', None, 'Equivocal', 'Equivocal,Positive']
igm_interpretation = ['Positive', 'Negative', None, 'Equivocal', 'Equivocal,Positive']

# Product
matrix = product(pcr_dengue_serotype,
                 ns1_interpretation,
                 igm_interpretation)

# Combinations
data = pd.DataFrame(matrix,
    columns=['pcr_dengue_serotype',
             'ns1_interpretation',
             'igm_interpretation'])

# Correction
correction = data.copy(deep=True)
correction['dengue_interpretation'] = \
    oucru_dengue_interpretation_feature(correction)
correction['dengue_interpretation_pcr'] = \
    oucru_dengue_interpretation_feature(correction,
        pcr=True, ns1=False, igm=False)
correction['dengue_interpretation_ns1'] = \
    oucru_dengue_interpretation_feature(correction,
        pcr=True, ns1=False, igm=False)
correction['dengue_interpretation_igm'] = \
    oucru_dengue_interpretation_feature(correction,
        pcr=True, ns1=False, igm=False)

# Show data any
print("\nData:")
print(data)
print("\nCorrection:")
print(correction.to_string())