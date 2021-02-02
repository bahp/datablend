"""
RenameWidget
===========================
"""

###############################################################################
# First of all, we need to import the modules and functions that will be used
# Import
import pandas as pd

# DataBlend library
from datablend.core.widgets.format import RenameWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Temp', 'to_name': 'body_temperature'},
    {'from_name': 'Shock', 'to_name': 'shock'},
    {'from_name': 'Sex', 'to_name': 'gender'}
]

# Data
data = [
    {'StudyNo': '32dx-001', 'Temp': 37.2, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-002', 'Temp': 36.5, 'Shock': False, 'Sex': 1},
    {'StudyNo': '32dx-003', 'Temp': 39.8, 'Shock': True, 'Sex': 2},
    {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 1}
]

# Create data
data = pd.DataFrame(data)

# Template (to check missing columns exception)
#template = pd.DataFrame(template)
#template = template.drop(columns=['to_name'])

# Create widget
widget = RenameWidget().fit(template)

# Transform
transformed = widget.transform(data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")