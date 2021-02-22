# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.core.blend.template import BlenderTemplate
from datablend.utils.pandas import save_xlsx

# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Path with raw data.
path_data = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '06dx_data_fixed.xlsx')

# Path to save fixed data.
path_ccfgs = '{0}/resources/outputs/templates/tmp/{1}'.format(
    curr_path, 'ccfgs_06dx_data_fixed.xlsx')

# --------------------
# Main
# --------------------
# Read all data sheets
data = pd.read_excel(path_data, sheet_name=None)

# Create templates
templates = {}

# Fill templates
for k, df in data.items():
    # Show information
    print("Processing sheet... %s <%s>." % (path_data, k))
    # Create descriptor template
    templates[k] = BlenderTemplate().fit_from_data(df)

# -----------
# Save
# -----------
# Create path if it does not exist
path = pathlib.Path(path_ccfgs)
path.parent.mkdir(parents=True, exist_ok=True)

# Format templates (improve this)
aux = {k:v.df for k,v in templates.items()}

# Save
save_xlsx(aux, path_ccfgs)
