"""
ReplaceWidget
===========================
"""

###############################################################################
# First of all, we need to import the modules and functions that will be used
# Import
import pandas as pd

# DataBlend library
from datablend.core.blend import BlenderTemplate
from datablend.core.widgets import RenameWidget
from datablend.core.widgets import ReplaceWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Temp', 'to_name': 'body_temperature'},
    {'from_name': 'Shock', 'to_name': 'shock'},
    {'from_name': 'Sex', 'to_name': 'gender',
     'to_replace': "{'Male': 1, 'Female': 2}"}
]

# Data
data = [
    {'StudyNo': '32dx-001', 'Temp': 37.2, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-002', 'Temp': 36.5, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-003', 'Temp': 39.8, 'Shock': True, 'Sex': 2},
    {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 1}
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = RenameWidget().fit_transform(bt, data)
trans = ReplaceWidget().fit_transform(bt, trans)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)