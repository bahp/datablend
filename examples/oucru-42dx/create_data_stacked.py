# Libraries
import pathlib
import pandas as pd

# Specific libraries
from datablend.core.descriptors import DatasetDescriptor
from datablend.utils.methods import extract_records_from_tuples

# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path
data_path = '%s/resources/datasets' % curr_path
outp_path = '%s/resources/outputs' % curr_path
ccfg_path = '%s/resources/configuration' % curr_path

# Filename
data_file = '19-5-2020-CTU42DX_Data.xls'

# Include books
include_books = ['HIST_CMH', 'HIST_DM', 'EVO', 'LAB',
                 'HEMA', 'FU_WEEK']

# -------------------------------
# Format data
# -------------------------------
# Read all data sheets
data = pd.read_excel('%s/%s' % (data_path, data_file), sheet_name=None)

# For each excel sheet
for k, df in data.items():

    # Ignore some excel books
    if not k in include_books:
        continue

    # Show information
    print("Processing sheet... %s <%s>." % (data_path, k))

    # Filepath json
    csv_path = '%s/ccfg-%s.csv' % (ccfg_path, k)

    # Create descriptor
    descriptor = DatasetDescriptor()
    descriptor = descriptor.fit(filepath=csv_path)

    # Transform data according to descriptor
    data = descriptor.transform(df)

    # Extract events from tuples
    stacked = extract_records_from_tuples(dataframe=data,
         index='study_no', return_by_types=False,
         tuples=descriptor.get_timestamp_feature_tuples(),
         verbose=10)

    # Save
    stacked.to_csv('%s/stacked_data_%s.csv' % (outp_path, k), index=False)
