# Libraries
import pandas as pd

# Specific libraries
from datablend.core.descriptors import DatasetDescriptor

# -------------------------------
# Create configuration from data
# -------------------------------
# Path
data_path = './resources/datasets'
outp_path = './resources/outputs'
ccfg_path = './resources/configuration'

# Filename
data_file = '19-5-2020-CTU32DX_Data.xls'

# Read all data sheets
data = pd.read_excel('%s/%s' % (data_path, data_file), sheet_name=None)

# For each excel sheet create configuration
for k, df in data.items():
    # Show information
    print("Processing sheet... %s <%s>." % (data_path, k))

    # Create descriptor config file and save.
    ccfg = DatasetDescriptor().infer_cfg_file(df)
    ccfg.to_csv('%s/tmp/ccfg-%s.csv' % (ccfg_path, k))

# Show information
print("""Please review the sheets created and edit them accordingly 
before applying the DatesetDescriptor for format the data.""")
print("Sheets saved in <%s/tmp>." % ccfg_path)
#vplease review them and edit accordingly.