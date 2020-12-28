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

# Create path
p = Path(path_data)

# Create empty data
data = pd.DataFrame()

# Read all files
for path in list(p.glob('**/*.csv')):
    aux = pd.read_csv(path)       # Read data
    print(str_dtypes(aux, path))  # Show dtypes
    data = data.append(aux)       # Append

# Show types
print(str_dtypes(data, 'Combined'))

# Show
print(str_dtypes(settings.prefix_sources(data)))

# Show sizes
for path in list(p.glob('**/*.csv')):
    aux = pd.read_csv(path)
    profiles = aux.shape
    patients = aux.study_no.nunique()
    print('%s: Patients %5s | Days %5s | Features %3s' %
          (path.name, patients, profiles[0], profiles[1]))