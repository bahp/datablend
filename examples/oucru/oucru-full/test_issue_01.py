# Libraries
import pandas as pd

# Import datablend
from datablend.core.repair.correctors import oucru_bleeding_correction
from datablend.core.repair.correctors import oucru_correction

STATUS = {
    True: 'SOLVED',
    False: 'PERSISTS'
}

# Path
path = './resources/datasets/20210401-v0.0.9/combined/combined_tidy.csv'

# Load data
data = pd.read_csv(path,
    parse_dates=['date'],
    low_memory=False)

# Convert dtypes
data = data.convert_dtypes()

# Apply full correction
#corrected = oucru_correction(data)

###########################################################################
# Issue 01: Oliver Stiff
# Date: 2021/04/01
# Dataset (issue): v0.0.8
# Description: Inconsistencies in oucru_bleeding_correction
# Problem:
#    The oucru_correction (which is the function that later calls
#    oucru_bleeding_correction) was being called before the schema
#    corrections. Thus, on a first instance the feature bleeding
#    was a compound features constructed from the various bleeding
#    sites. However, the generic corrections using 'bfill' were
#    applied afterwards and therefore were generating those
#    inconsistencies.
# Solution:
#    Call schema corrections first.
# Dataset (corrected): v0.0.9

# Libraries
from datablend.core.repair.correctors import find_bleeding_location_columns

# Find bleeding sites
sites = find_bleeding_location_columns(data.columns)

# Create auxiliary dataframe
aux = data[['bleeding'] + sites].copy(deep=True)

# Get inconsistent idxs
idxs = (aux.bleeding == False) & aux[sites].any(axis=1)

# Correct the data
#corrected = oucru_bleeding_correction(aux)

# Show status
print("Issue 01: %s" % STATUS[idxs.sum() == 0])

if idxs.sum() > 0:
    print(data[idxs])