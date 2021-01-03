# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend library
from datablend.core import settings
from datablend.utils.display import str_dtypes

# -----------------------------------
# Configuration
# -----------------------------------
# Configuration
pd.set_option("display.max_rows", None,
              "display.max_columns", None)

# -----------------------------------
# Constants
# -----------------------------------
# Constants
path_data = './resources/datasets'
outp_path = './resources/outputs/datasets'


# Path with raw data.
path_data = Path('./resources/datasets')

# Path to save fixed data.
path_comb = Path('./resources/datasets')

# Create empty data
data = pd.DataFrame()

# Read all files
for path in sorted(list(path_data.glob('**/*.csv'))):
    aux = pd.read_csv(path)       # Read data
    print(str_dtypes(aux, path))  # Show dtypes
    data = data.append(aux)       # Append

# Show types
print(str_dtypes(data, 'Combined'))

# Show
print(str_dtypes(settings.prefix_sources(data)))

# Show sizes
for path in sorted(list(path_data.glob('**/*.csv'))):
    aux = pd.read_csv(path)
    profiles = aux.shape
    patients = aux.study_no.nunique()
    print('%s: Patients %5s | Days %5s | Features %3s' %
          (path.name, patients, profiles[0], profiles[1]))

# -----------------
# Save
# -----------------
# Create file name
tidy_files = list(path_data.glob('**/*.csv'))
tidy_ids = sorted([e.stem.split("_")[0] for e in tidy_files])
filename = '{0}_data_tidy.csv'.format('_'.join(tidy_ids))
filepath = '{0}/{1}'.format(path_comb, filename)

# Save
data.to_csv(filepath, index=False)