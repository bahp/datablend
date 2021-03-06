"""
DateFromStudyDayWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.format import RenameWidget
from datablend.core.widgets.format import DateFromStudyDayWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'DateEnrol', 'to_name': 'date_enrolment'},
    {'from_name': 'LabStudyDay', 'to_name': 'lab_study_day'},

    # Example date from study day widget
    {'from_name': None,
     'to_name': 'date_laboratory',
     'study_day_col': '-lab_study_day',
     'study_day_ref': 'date_enrolment'},
]

# Data
data = [
    {'StudyNo': '32dx-001', 'DateEnrol': '2020/12/01', 'LabStudyDay': 1},
    {'StudyNo': '32dx-002', 'DateEnrol': '2020/12/04', 'LabStudyDay': 5},
    {'StudyNo': '32dx-003', 'DateEnrol': '2020/12/11', 'LabStudyDay': 10},
    {'StudyNo': '32dx-004', 'DateEnrol': '2020/12/08 04:30', 'LabStudyDay': 0},
    {'StudyNo': '32dx-005', 'LabStudyDay': 3},
    {'StudyNo': '32dx-005', 'DateEnrol': '2020/12/07'}
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = RenameWidget().fit_transform(bt, data)
trans = DateFromStudyDayWidget().fit_transform(bt, trans)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)