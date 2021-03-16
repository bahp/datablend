"""
Compute day
================
"""
# Libraries
import pandas as pd

# Specific
from itertools import product

# DataBlend
from datablend.core.repair.correctors import day_from_first_true
from datablend.core.repair.correctors import day_from_day_values

# -----------------------------
# Main
# -----------------------------
# Possible values
data = [
    {'study_no': '1', 'date': '10/11/2015', 'day_from_illness': 0},
    {'study_no': '1', 'date': '11/11/2015', 'day_from_illness': 1},
    {'study_no': '1', 'date': '12/11/2015', 'day_from_illness': 2},
    {'study_no': '1', 'date': '13/11/2015', 'day_from_illness': 3},
    {'study_no': '1', 'date': '14/11/2015', 'day_from_illness': 4},
    {'study_no': '1', 'date': '15/11/2015', 'day_from_illness': 5},

    {'study_no': '2', 'date': '07/11/2016', 'day_from_illness': None},
    {'study_no': '2', 'date': '08/11/2016', 'day_from_illness': 1},
    {'study_no': '2', 'date': '09/11/2016', 'day_from_illness': None},
    {'study_no': '2', 'date': '10/11/2016', 'day_from_illness': None},
    {'study_no': '2', 'date': '11/11/2016', 'day_from_illness': 4},
    {'study_no': '2', 'date': '12/11/2016', 'day_from_illness': 5},

    {'study_no': '3', 'date': '07/11/2016', 'day_from_illness': 3},
    {'study_no': '3', 'date': '08/11/2016', 'day_from_illness': 1},
    {'study_no': '3', 'date': '09/11/2016', 'day_from_illness': 2},
    {'study_no': '3', 'date': '10/11/2016', 'day_from_illness': 3},
    {'study_no': '3', 'date': '11/11/2016', 'day_from_illness': 4},
    {'study_no': '3', 'date': '12/11/2016', 'day_from_illness': 5},

    {'study_no': '4', 'date': '10/11/2016', 'day_from_illness': None},
    {'study_no': '4', 'date': '11/11/2016', 'day_from_illness': None},
    {'study_no': '4', 'date': '12/11/2016', 'day_from_illness': None},

]

# Create DataFrame
data = pd.DataFrame(data)

# Convert to datetime
data['date'] = pd.to_datetime(data.date,
    format='%d/%m/%Y')

# Compute day
data['day_aux'] = \
    data.groupby('study_no') \
        .apply(day_from_day_values) \
        .droplevel(level=0, axis=0) \
        .dt.days

# Correct event onset
data['event_onset'] = \
    data.day_aux == 0

# Show
print("\n\nData:")
print(data)

import sys
sys.exit()

"""
Old code for records...

data['date_onset_aux'] = \
    add_days(data.date, -data.day_from_illness)

# Count the date_onsets.
counts = data.groupby('study_no')\
    .date_onset_aux.value_counts()

# Keep only the most frequent one.
onsets = counts.groupby('study_no' )\
    .head(1).index.to_frame() \
    .reset_index(drop=True)

# Merge
data = data.merge(onsets, how='left',
    left_on='study_no',  right_on='study_no')

# Compute day_from_illness
data['day_from_illness_aux'] = \
    (data.date - data.date_onset_aux_y).dt.days
"""