"""
ReplaceWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend import BlenderTemplate
from datablend.core.widgets.format import ReplaceWidget

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
     'to_replace': "{'Male': 1, 'Female': 2, 'Unknown': 8}"}
]

# Data
data = [
    {'StudyNo': '32dx-001', 'Temp': 37.2, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-002', 'Temp': 36.5, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-003', 'Temp': 39.8, 'Shock': True, 'Sex': 2},
    {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 1},

    # To test warnings
    # {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 3},
    # {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 4}
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = ReplaceWidget().fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)
