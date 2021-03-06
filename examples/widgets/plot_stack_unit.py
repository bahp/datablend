"""
StackWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.stack import StackWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'DateEnrol', 'to_name': 'date_enrolment'},
    {'from_name': 'Sex', 'to_name': 'gender', 'timestamp': 'date_enrolment'},
    {'from_name': 'Tmp', 'to_name': 'body_temperature',
        'timestamp': 'date_enrolment', 'unit': 'celsius'}
]

# Data
data = [
    {'StudyNo': '32dx-001', 'DateEnrol': '2020/12/01', 'Sex': 1, 'Tmp': 37.5},
    {'StudyNo': '32dx-002', 'DateEnrol': '2020/12/04', 'Sex': 2, 'Tmp': 36.8},
    {'StudyNo': '32dx-003', 'DateEnrol': '2020/12/08', 'Sex': 1, 'Tmp': 39.2},
    {'StudyNo': '32dx-004', 'DateEnrol': '2020/12/11', 'Sex': 1},
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Stack data
stack = StackWidget(index=['StudyNo']).fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(data)
print("\nStack:")
print(stack)