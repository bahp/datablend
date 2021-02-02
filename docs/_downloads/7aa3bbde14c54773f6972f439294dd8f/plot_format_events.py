"""
EventWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import BlenderTemplate
from datablend.core.widgets.format import EventWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'LabStudyDay', 'to_name': 'lab_study_day'},

    # Example event
    {'from_name': 'DateEnrol',
     'to_name': 'date_enrolment',
     'event': 'event_enrolment'},
]

# Data
data = [
    {'StudyNo': '32dx-001', 'DateEnrol': '2020/12/01', 'LabStudyDay': 1},
    {'StudyNo': '32dx-002', 'DateEnrol': '2020/12/04', 'LabStudyDay': 5},
    {'StudyNo': '32dx-003', 'DateEnrol': '2020/12/08', 'LabStudyDay': 0},
    {'StudyNo': '32dx-004', 'DateEnrol': '2020/12/11', 'LabStudyDay': 10},
    {'StudyNo': '32dx-005', 'LabStudyDay': 3},
    {'StudyNo': '32dx-005', 'DateEnrol': '2020/12/07'}
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = EventWidget().fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)