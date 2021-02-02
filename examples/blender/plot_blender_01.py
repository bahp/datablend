"""
Blender with single input
=========================

Example using ``Blender`` with data collected from a single sources.

"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import Blender
from datablend.core.widgets.format import ReplaceWidget


# ------------------------
# Constants
# ------------------------
# Templates
template = [
    # Body Temperature
    {'from_name': 'Temp',
     'to_name': 'body_temperature',
     'timestamp': 'date_exam',
     'unit': 'celsius'},

    # Gender
    {'from_name': 'Sex', 'to_name': 'gender',
     'to_replace': {1: 'Male', 2: 'Female'},
     'timestamp': 'date_exam'},
]

# Data
data = [
    {'pid': '32dx-001', 'date_exam': '10/07/2020', 'Temp': 37.2, 'Sex': 1},
    {'pid': '32dx-002', 'date_exam': '08/07/2020', 'Temp': 37.5, 'Sex': 2},
    {'pid': '32dx-003', 'date_exam': '10/07/2020', 'Temp': 36.7, 'Sex': 2},
]

# -------------------
# Main
# -------------------
# Create templates dictionary
templates = pd.DataFrame(template)
data = pd.DataFrame(data)

# Create blender
blender = Blender(widgets=[ReplaceWidget()])

# Fit blender to templates.
blender = blender.fit(info=templates)

# Transform data
transformed = blender.transform(data)

# Stack data
stacked = blender.stack(transformed, index='pid')

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")
print(stacked)