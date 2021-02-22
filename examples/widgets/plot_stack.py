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
    {'from_name': 'StudyNo',
     'to_name': 'study_number'},

    {'from_name': 'DateEnrol',
     'to_name': 'date_enrolment',
     'event': 'event_enrolment'},

    {'from_name': 'Sex',
     'to_name': 'gender',
     'timestamp': 'date_enrolment'},

    {'from_name': 'Tmp',
     'to_name': 'body_temperature',
     'timestamp': 'date_enrolment',
     'unit': 'celsius'},

    {'from_name': 'Tmp2',
     'to_name': 'body_temperature',
     'timestamp': 'date_enrolment',
     'unit': 'celsius'}
]

# Data
data = [
    {'StudyNo': '32dx-001', 'DateEnrol': '2020/12/01', 'Sex': 1, 'Tmp': 37.5},
    {'StudyNo': '32dx-002', 'DateEnrol': '2020/12/04', 'Sex': 2, 'Tmp': 36.8},
    {'StudyNo': '32dx-003', 'DateEnrol': '2020/12/08', 'Sex': 1, 'Tmp': 39.2, 'Tmp2': 35.0},
    {'StudyNo': '32dx-004', 'DateEnrol': '2020/12/11', 'Sex': 1},
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# This breaks because the EventWidget is used on the FullTemplate
# but is not implemented within the StackWidget. However, the
# stack widget creates tuples from both time stamp and events.
# EventWidget was not executed and therefore event_enrolment does
# not exist.

# Stack data
stack = StackWidget(index=['study_number']).fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nStack:")
print(stack)