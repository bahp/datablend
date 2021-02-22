# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path


# -----------------------------------
# Methods
# -----------------------------------


# -----------------------------------
# Configuration
# -----------------------------------

# -----------------------------------
# Constants
# -----------------------------------

# -------------------------------------------------------
# Main
# -------------------------------------------------------
# Path with data
path_tidy = Path('./resources/datasets/combined/combined_tidy.csv')
path_tidy = Path('./resources/datasets/tidy/06dx_data_tidy_corrected.csv')

"""
# Load
data = pd.read_csv(path_tidy,
    parse_dates=['date'],
    low_memory=False)
"""


data = [
    ['1', '2001-11-10', True, True],
    ['1', '2001-11-12', None, None],
    ['1', '2001-11-13', None, None],
    ['1', '2001-11-14', None, None],
    ['1', '2001-11-15', None, None],
    ['2', '2001-11-10', None, True],
    ['2', '2001-11-12', None, None],
    ['2', '2001-11-13', True, None],
    ['2', '2001-11-14', None, None],
    ['2', '2001-11-10', None, None],
    ['3', '2001-11-11', None, None],
    ['3', '2001-11-12', None, None],
    ['3', '2001-11-13', None, True],
    ['3', '2001-11-14', None, None],
    ['3', '2001-11-15', None, None],
]

# Create dataframe
data = pd.DataFrame(data,
    columns=['study_no',
             'date',
             'event_enrolment',
             'event_admission'])

# Cast to dates
data.date = pd.to_datetime(data.date)

# ----------------------------
# Length of stay
# ----------------------------
# Group by patient
g = data.groupby('study_no')

# Length of stay
length = g.date.max() - g.date.min()

# Show
print("\n\n")
print(length)


# ----------------------------
# Day from start point
# ----------------------------
def day_from_first_true(x, event, tag):
    """"""
    # Keep not nan
    notna = x.dropna(how='any', subset=[event])
    # Create column
    if notna.size:
        x['day_from_%s' % tag] = \
            (x.date - notna.date.values[0]).dt.days
        return x
    x['day_from_%s' % tag] = None
    # Return
    return x


data_aux = \
    data.groupby('study_no') \
        .apply(day_from_first_true,
           event='event_enrolment',
           tag='enrolment')


data_aux = \
    data_aux.groupby('study_no') \
        .apply(day_from_first_true,
           event='event_admission',
           tag='admission')

print("\n\n")
print(data)

print("\n\n")
print(data_aux)

#print(data.date - date_enrolment.date)

"""
# At least one shock event
idxs = tidy \
           .groupby(by='study_no') \
           .event_shock.transform('sum') > 0
tidy.loc[idxs, 'shock'] = True
"""