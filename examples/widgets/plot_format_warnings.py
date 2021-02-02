"""
Warnings
===========================

BlenderTemplate warnings
 - duplicated from_name
 - null to_name
 - to_replace not a map
 - column does not exist in data
 - not a datetime.

"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.format import DateTimeMergeWidget
from datablend.core.widgets.format import ReplaceWidget
from datablend.core.widgets.format import RenameWidget
from datablend.core.widgets.format import DateFromStudyDayWidget
from datablend.core.widgets.format import EventWidget
from datablend.core.widgets.stack import StackWidget
from datablend.core.widgets.stack import StackUnitWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
]

# Data
data = [
    {'StudyNo': '32dx-001', 'enDate': '2020/12/01', 'enTime': '10:00'},
    {'StudyNo': '32dx-002', 'enDate': '2020/12/04', 'enTime': '11:00'},
    {'StudyNo': '32dx-003', 'enDate': '2020/12/08', 'enTime': '04:30'},
    {'StudyNo': '32dx-004', 'enDate': '2020/12/11', 'enTime': '09:07'},
    {'StudyNo': '32dx-004', 'enDate': '2020/12/11', 'enTime': '24:00'},
]

# Blender template
bt = BlenderTemplate().fit(template)

# Create data
data = pd.DataFrame(data)

# Create widgets and transform
trans = DateTimeMergeWidget(errors='warn').fit_transform(bt, data)
trans = ReplaceWidget(errors='warn').fit_transform(bt, data)
trans = DateFromStudyDayWidget(errors='warn').fit_transform(bt, data)
trans = EventWidget(errors='warn').fit_transform(bt, data)
trans = RenameWidget(errors='warn').fit_transform(bt, data)

# Why does it show unit in both??
stack = StackWidget(index=['StudyNo'], errors='warn').fit_transform(bt, data)
stack = StackWidget(index=['StudyNo'], with_unit=False, errors='warn').fit_transform(bt, data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(trans)