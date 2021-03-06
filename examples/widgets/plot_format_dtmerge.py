"""
DateTimeMergeWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import BlenderTemplate
from datablend.core.widgets.format import DateTimeMergeWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},

    # Example datetime merge
    {'from_name': None,
     'to_name': 'date_enrolment',
     'datetime_date': 'enDate',
     'datetime_time': 'enTime'},
]

# Data
data = [
    {'StudyNo': '32dx-001', 'enDate': '10/25/10', 'enTime': '10:00'},
    {'StudyNo': '32dx-002', 'enDate': '10/11/12', 'enTime': '11:00'},
    {'StudyNo': '32dx-003', 'enDate': '10/11/12', 'enTime': '04:30'},
    {'StudyNo': '32dx-004', 'enDate': '10/11/12', 'enTime': '09:07'},
    {'StudyNo': '32dx-004', 'enDate': '10/11/12', 'enTime': '24:00'}, # MM/DD/YY
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = DateTimeMergeWidget().fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)