# Libraries
import pandas as pd
import warnings

# Specific libraries
from pathlib import Path

# Libraries
from pandas_profiling import ProfileReport
from dataprep.eda import create_report

# Ingore warnings
warnings.simplefilter("ignore")

# -----------------------------------
# Constants
# -----------------------------------
# Path with raw data.
path_data = Path('./resources/datasets/tidy')
path_report = Path('./resources/reports')

REPORT_PARTIAL = True
PANDAS_PROFILE = True
DATAPREP_PROFILE = True


# ------------------------------
# Load data
# ------------------------------
# Initialise
data = {}

# Loop filling data
for path in sorted(list(path_data.glob('**/*.csv'))):
    if not REPORT_PARTIAL:
        continue

    try:
        # Show information
        print("Loading... %s" % path.stem)

        # Load data
        data[path.name] = pd.read_csv(path,
            parse_dates=['date'])

        # Define information
        title = 'OUCRU - {0}'.format(path.name)

        # Columns with > 1 unique values
        columns = data[path.name].nunique() > 1
        columns = columns[columns].index.values
        datavld = data[path.name][columns]

        # Generate data-prep report
        # -------------------------
        if DATAPREP_PROFILE:
            report = create_report(datavld, title=title)
            report.save('{0}/profile-dataprep/{1}'
                .format(path_report, path.stem))

        # Generate pandas-profile report
        # ------------------------------
        if PANDAS_PROFILE:
            profile = ProfileReport(datavld, title=title)
            profile.to_file('{0}/profile-pandas/{1}.html'
                .format(path_report, path.stem))

    except Exception as e:
        print("Error", e)


# ------------------------------
# Load data
# ------------------------------
# Path
path = Path('./resources/datasets/combined/combined_tidy.csv')

# Data
data = pd.read_csv(path,
    parse_dates=['date'])

# Columns with > 1 unique values
columns = data.nunique() > 1
columns = columns[columns].index.values

# Filter
data = data[columns]

# Title
title = 'OUCRU - {0}'.format(path.name)

# Generate data-prep report
# -------------------------
if DATAPREP_PROFILE:
    report = create_report(data, title=title)
    report.save('{0}/profile-dataprep/{1}'
                .format(path_report, path.stem))

# Generate pandas-profile report
# ------------------------------
if PANDAS_PROFILE:
    profile = ProfileReport(data, title=title, explorative=True)
    profile.to_file('{0}/profile-pandas/{1}.html'
                    .format(path_report, path.stem))