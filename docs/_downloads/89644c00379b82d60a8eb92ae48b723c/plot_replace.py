"""
Replace values (replace)
==========================
"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import replace_correction

# ------------------------
# Constants
# ------------------------
# Sample
sample1 = pd.Series(['DENV-1',
                     'DENV-2',
                     'DENV-1,DENV-2',
                     np.nan,
                     None,
                     'Empty',
                     'empty',
                     'NEG',
                     'No sample',
                     'No Sample'])

# values to replace
to_replace = {
    'Empty': None,
    'empty': None,
    'NEG': '<LOD',
    'No Sample': None,
    'No sample': None
}

# ------------------------
# Main
# ------------------------
# Correct
a = replace_correction(sample1, to_replace=to_replace)

# Show
print("\n%s" % pd.concat([sample1, a], axis=1))