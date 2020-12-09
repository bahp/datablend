# Libraries
import textwrap
import pathlib
import pandas as pd

# Specific libraries
from pathlib import Path

# -----------------------------------
# Configuration
# -----------------------------------
# Configuration
pd.set_option("display.max_rows", None,
              "display.max_columns", None)

# -----------------------------------
# Constants
# -----------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Constants
outp_path = '%s/resources/outputs' % curr_path
comb_file = '42dx-combined-books.csv'
comb_path = '%s/%s' % (outp_path, comb_file)

# Create path
p = Path(outp_path)

# Create empty data
data = pd.DataFrame()

# Read all files
for path in list(p.glob('**/stacked_*.csv')):
    data = data.append(pd.read_csv(path))

# Basic formatting
data.date = pd.to_datetime(data.date)
data.date = data.date.dt.date
data = data.convert_dtypes()
data = data.drop_duplicates()
data = data.sort_values(by=['study_no', 'date', 'column'])

# Convert to tidy format
tidy = data.copy(deep=True)
tidy = tidy.set_index(['study_no', 'date', 'column'])

# Look for index duplicates
duplicates = tidy.index.duplicated(keep=False)

# Show
print("=" * 80)
print("The data size: %s" % str(data.shape))
print('The following duplicates were found:\n')
print(tidy[duplicates])
print("\n")
print(*textwrap.wrap(('Duplicates might be because the '
                      'data is being group by day and therefore the time '
                      'information is dropped. By the default the LAST '
                      'row is kept.'), width=80), sep='\n')
print("=" * 80)

# Keep only last row
tidy = tidy[~tidy.index.duplicated(keep='last')]  # keep only last row
tidy = tidy.unstack(level=2)  # Unstack
tidy.columns = tidy.columns.droplevel(level=0)  # Drop...
tidy = tidy.reset_index()

# --------------------------
# Format
# --------------------------

# Set static
# ----------
# Features that do not change over time the course of the admission.
static = ['gender', 'age', 'diabetes', 'height', 'pregnant',
          'weight', 'anemia', 'asthma', 'coronary_heart_disease',
          'hypertension', 'peptic_ulcer', 'chronic_hepatitis',
          'renal_disease']

for c in static:
    if c in tidy:
        tidy[c] = tidy.groupby(by='study_no')[c].ffill()
        tidy[c] = tidy.groupby(by='study_no')[c].bfill()

# Set Levels
# ----------
# Features in which level is indicated with a number. Thus if no
# level indicated (np.nan) then the level is 0.
levels = [c for c in tidy.columns if 'level' in c]
tidy[levels] = tidy[levels].fillna(0)

# Date of onset
# -------------
# For some parameters, it is indicated the date of onset.
#
# The dataset is a combination of history, examination and
# evolution spreadsheets. Thus the following assumptions
# are made.
#
# - We use bfill for those results in which the first value
#   is False. This means that if the value obtained on
#   examination was false there was no previous symptoms
#   of such either.
#
#
onset = ['chills', 'anorexia', 'nausea', 'vomiting', 'diarrhoea',
         'sore_throat', 'cough', 'bleeding_skin', 'feeling_faint']

for c in onset:
    if c in tidy:
        tidy[c] = tidy[c].ffill()

# Date admission / discharge
# --------------------------

# Haematocrit
# ------------
# Save
tidy.to_csv('%s/%s' % (outp_path, comb_file), index=False)

# Show types
print("=" * 80)
print("Date Types:\n")
print(tidy.dtypes.convert_dtypes().sort_index())
print("\nThe outfile is: %s" % comb_path)
print("=" * 80)