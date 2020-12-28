# Libraries
import pandas as pd

# Specific libraries
from datablend.core.descriptors import Template
from datablend.core.descriptors import DataBlender
from datablend.utils.pandas import save_xlsx

# -------------------------------
# Create configuration from data
# -------------------------------
# Paths
path_output_temp = './resources/outputs/templates'
path_output_data = './resources/outputs/datasets'

# Filename
filename = '13dx_data_fixed.xlsx'

# Filepath to raw dataset
filepath_data = '{0}/{1}'.format(path_output_data, filename)
filepath_tmps = '{0}/tmp/ccfgs_{1}'.format(path_output_temp, filename)

# -------------------
# Main
# -------------------
# Read data (all sheets)
data = pd.read_excel(filepath_data, sheet_name=None)

# Create the configuration templates
templates = DBTemplate().fit(data)

# Create folder if it does not exist.
tmp = Template(templates['ENROL'])

print(tmp.has_timestamp())


import sys
sys.exit()
# Save templates
save_xlsx(templates, filepath_tmps, sheet_split=False)