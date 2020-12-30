"""
Blender with single input
============================

Example using ``Blender`` works with data collected from a single sources.

"""

# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.core.blend import BlenderTemplate
from datablend.utils.pandas import save_xlsx


# --------------------
# Constants
# --------------------
# Data
data = [
    {'pid': '32dx-001', 'date_exam': '10/07/2020', 'Temp': 37.2, 'Sex': 1},
    {'pid': '32dx-002', 'date_exam': '08/07/2020', 'Temp': 37.5, 'Sex': 2},
    {'pid': '32dx-003', 'date_exam': '10/07/2020', 'Temp': 36.7, 'Sex': 2},
]

# --------------------
# Main
# --------------------
# Read all data sheets
data = pd.DataFrame(data)

# Create template
template = BlenderTemplate().fit_from_data(data)

# Show
print(template)