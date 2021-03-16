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

# -----------------------------
# Main
# -----------------------------
# Possible values
data = [
    {'study_no': '1', 'date': '10/11/2015', 'event_admission': False},
    {'study_no': '1', 'date': '11/11/2015', 'event_admission': True},
    {'study_no': '1', 'date': '12/11/2015', 'event_admission': False},
    {'study_no': '1', 'date': '13/11/2015', 'event_admission': False},
    {'study_no': '1', 'date': '14/11/2015', 'event_admission': False},
    {'study_no': '1', 'date': '15/11/2015', 'event_admission': False},

    {'study_no': '2', 'date': '07/11/2016', 'event_admission': None},
    {'study_no': '2', 'date': '08/11/2016', 'event_admission': True},
    {'study_no': '2', 'date': '09/11/2016', 'event_admission': None},
    {'study_no': '2', 'date': '10/11/2016', 'event_admission': None},
    {'study_no': '2', 'date': '11/11/2016', 'event_admission': None},
    {'study_no': '2', 'date': '12/11/2016', 'event_admission': None},

    {'study_no': '3', 'date': '07/11/2016', 'event_admission': None},

    {'study_no': '4', 'date': '07/11/2016', 'event_admission': True},

    {'study_no': '5', 'date': '07/11/2016', 'event_admission': False},

    {'study_no': '6', 'date': None, 'event_admission': True},


]

# Create DataFrame
data = pd.DataFrame(data)

# Convert to datetime
data['date'] = pd.to_datetime(data.date,
    format='%d/%m/%Y')

# Days from admission
data = \
    data.groupby('study_no') \
        .apply(day_from_first_true,
               event='event_admission',
               tag='admission')

# Show
print("\nData:")
print(data)

# -----------------------------
# Example oucru-32dx
# -----------------------------
# Create path
path = '../oucru/oucru-full/resources/datasets/tidy/32dx_data_tidy_corrected.csv'

# Create DataFrame
data = pd.read_csv(path,
    usecols=['date',
             'study_no',
             'event_admission',
             'day_from_admission'],
    parse_dates=['date'],
    low_memory=False)


# Days from admission
data = \
    data.groupby('study_no') \
        .apply(day_from_first_true,
               event='event_admission',
               tag='admission_recomputed')

# Show data
print("\n\nData:")
print(data)

# Check differences
print("\nComparison:")
print(data.day_from_admission.compare( \
    data.day_from_admission_recomputed))

print("\nShow count:")
print(data.day_from_admission \
          .value_counts()
          .sort_index())