"""
Ensure compound features
========================
"""
# Libraries
import pandas as pd

# DataBlend library
from datablend.core.repair.correctors import compound_feature_correction



# Constant with compound definitions
OUCRU_COMPOUND_FEATURES = {
    'bleeding_gi': [
        'hematemesis',
        'melaena'],
    'bleeding_nose': [
        'hematemesis',
        'not exists'],
    'ventilation': [
        'ventilation_bool',
        'ventilation_level',
        'ventilation_mask',
        'ventilation_type'],
}

# Define data
data = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [0, 0, 0, 0, 0, pd.NA],
    [0, 0, 1, 0, 0, pd.NA],
    [0, 0, 0, 5, 0, pd.NA],
    [0, 0, 0, 0, 1, pd.NA],
    [0, 0, 0, 0, 0, 'CPAP'],
]

# Create
data = pd.DataFrame(data,
    columns=['hematemesis',
             'melaena',
             'ventilation_bool',
             'ventilation_level',
             'ventilation_mask',
             'ventilation_type'])

# Correction
corrected = data.copy(deep=True)

# Apply
for k, v in OUCRU_COMPOUND_FEATURES.items():

    # Get intersection columns
    columns = corrected.columns.intersection(set(v))
    if not columns.tolist():
        continue

    # Create column if not exists
    if not k in corrected.columns:
        corrected[k] = pd.NA

    # Create compound feature
    corrected[k] = \
        compound_feature_correction(
            corrected[k],
            corrected[columns],
            verbose=10)

# Show
print("\nData:")
print(data)
print("\nCorrection:")
print(corrected)