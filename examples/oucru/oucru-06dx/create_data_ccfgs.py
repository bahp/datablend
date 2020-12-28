# Libraries
import pandas as pd

# Specific libraries
from datablend.core.blend import BlenderTemplate
from datablend.utils.pandas import save_xlsx

# -------------------------------
# Create configuration from data
# -------------------------------
# Paths
path_input_data = './resources/datasets/'
path_output_temp = './resources/outputs/templates'
path_output_data = './resources/outputs/datasets'

# Data input filename
filename = '19-5-2020-CTU06DX_Data.xls'

# Read all data sheets
data = pd.read_excel('%s/%s' %
    (path_input_data, filename), sheet_name=None)

# Create templates
templates = {}

# Fill templates
for k, df in data.items():
    # Show information
    print("Processing sheet... %s <%s>." % (path_input_data, k))
    # Create descriptor template
    templates[k] = BlenderTemplate().fit_from_data(df)

# Save
aux = {k:v.df for k,v in templates.items()}
save_xlsx(aux, '%s/tmp/ccfgs_06dx_data_fixed.xlsx' % path_output_temp)

import sys
sys.exit()
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