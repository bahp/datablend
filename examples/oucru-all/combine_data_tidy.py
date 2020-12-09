# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path


# -----------------------------------
# Methods
# -----------------------------------
def print_dtypes(data, label=None):
    """Displays the dtypes"""
    # Show types
    print("=" * 80)
    if label is not None:
        print("SOURCE: %s\n" % label)
    print("Date Types:\n")
    print(data.convert_dtypes().dtypes.sort_index())
    print("=" * 80)


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
data_path = './resources/datasets'
outp_path = './resources/outputs'

# Create path
p = Path(data_path)

# Create empty data
data = pd.DataFrame()

# Read all files
for path in list(p.glob('**/*.csv')):
    aux = pd.read_csv(path)     # Read data
    print_dtypes(aux, path)     # Show dtypes
    data = data.append(aux)     # Append

    print('%s :%s' % (path.name, str(aux.shape)))

# Show types
print_dtypes(data)

# Show sizes
for path in list(p.glob('**/*.csv')):
    aux = pd.read_csv(path)
    profiles = aux.shape
    patients = aux.study_no.nunique()
    print('%s: Patients %5s | Days %5s | Features %3s' %
          (path.name, patients, profiles[0], profiles[1]))