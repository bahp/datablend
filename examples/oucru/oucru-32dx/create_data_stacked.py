# Libraries
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# DataBlend libraries
from datablend.core.blend import Blender
from datablend.core.widgets import DateTimeMergeWidget
from datablend.core.widgets import RenameWidget
from datablend.core.widgets import ReplaceWidget
from datablend.core.widgets import TemplateTransformWidget
from datablend.core.widgets import EventWidget
from datablend.core.widgets import StackWidget
from datablend.utils.logger import load_logger


# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with fixed data
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '32dx_data_fixed.xlsx')

# Path with templates
path_ccfgs = '{0}/resources/outputs/templates/{1}'.format(
    curr_path, 'ccfgs_32dx_data_fixed.xlsx')

# Path to save stacked data
path_stack = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '32dx_data_stacked.xlsx')


# Logging information
logger.info("=" * 80)
logger.info("File: %s", path_fixed)
logger.info("")

# -------------------------------
# Main
# -------------------------------
# Excel sheets to include
include = ['HIS', 'EXAM', 'EVO', 'MGMT', 'LAB',
           'PCR', 'SEROLOGY', 'LAB_DIAGNOSIS']

# Excel sheets to exclude
exclude = ['Category', 'SUM', 'FU', 'NS1']

# Read all data sheets
data = pd.read_excel(path_fixed, sheet_name=None)
tmps = pd.read_excel(path_ccfgs, sheet_name=None)

# Create blender
blender = Blender(widgets=[DateTimeMergeWidget(),
                           RenameWidget(),
                           ReplaceWidget(),
                           #TemplateTransformWidget(),
                           EventWidget()])

# Fit blender to templates.
blender = blender.fit(info=tmps)

# Transform data
transformed = blender.transform(data, include=include,
                                      exclude=exclude)

# Stack data
stacked = blender.stack(transformed, index='study_no',
                                     include=include,
                                     exclude=exclude)

# Save stack data
for k, df in stacked.items():
    df.to_csv(path_stack.replace('.xlsx', '_%s.csv' % k), index=False)