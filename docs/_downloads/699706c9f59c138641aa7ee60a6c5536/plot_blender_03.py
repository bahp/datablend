"""
Blender with various widgets
====================================

.. warning:: The order of the ``Widgets`` passed to ``Blender`` matters.

"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend import Blender
from datablend.core.widgets import RenameWidget
from datablend.core.widgets import ReplaceWidget
from datablend.core.widgets import DateTimeMergeWidget
from datablend.core.widgets import DateFromStudyDayWidget
from datablend.core.widgets import EventWidget
from datablend.core.widgets import StackWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo',
     'to_name': 'study_number'},

    # Example datetime merge
    {'from_name': None,
     'to_name': 'date_enrolment',
     'datetime_date': 'enDate',
     'datetime_time': 'enTime'},

    # Example parameters to be stacked
    {'from_name': 'Temp',
     'to_name': 'body_temperature',
     'timestamp': 'date_enrolment',
     'unit': 'celsius'},

    {'from_name': 'Shock',
     'to_name': 'shock',
     'timestamp': 'date_enrolment'},

    # Example replace widget
    {'from_name': 'Sex', 'to_name': 'gender',
     'to_replace': {'Male': 1, 'Female': 2},
     'timestamp': 'date_enrolment'},

    # Example parameters to be stacked.
    # Note that uses a different date.
    {'from_name': 'CoughLevel',
     'to_name': 'cough_level',
     'timestamp': 'cough_date'},

    {'from_name': 'CoughDate',
     'to_name': 'cough_date',
     'datetime': True},

    # Example event
    {'from_name': 'DateIllness',
     'to_name': 'date_onset',
     'datetime': True,
     'event': 'event_onset'},

    # Example study day
    {'from_name': 'LabSampleStudyDay',
     'to_name': 'lab_study_day'},

    {'from_name': None,
     'to_name': 'date_laboratory',
     'study_day_col': 'lab_study_day',
     'study_day_ref': 'date_enrolment'},

    {'from_name': 'hct',
     'to_name': 'hct',
     'timestamp': 'date_laboratory',
     'unit': '%'},

    {'from_name': 'wbc',
     'to_name': 'wbc',
     'timestamp': 'date_laboratory',
     'unit':'10^9U/L'}

]

# Data
data = [
    {'StudyNo': '32dx-001',
     'enDate': '11/07/2020', 'enTime': '10:00',
     'DateIllness': '05/07/2020',
     'Temp': 37.2, 'Shock': False, 'Sex': 1,
     'CoughLevel': 1, 'CoughDate': '12/07/2020',
     'hct': 2.0, 'wbc': 3.5, 'LabSampleStudyDay': 3},

    {'StudyNo': '32dx-002',
     'enDate':'12/07/2020', 'enTime': '11:00',
     'DateIllness': '09/07/2020',
     'Temp': 36.5, 'Shock': False, 'Sex': 1,
     'CoughLevel': 5, 'CoughDate': '14/07/2020',
     'hct': 3.0, 'wbc': 2.0, 'LabSampleStudyDay': 5},

    {'StudyNo': '32dx-003',
     'enDate': '13/07/2020', 'enTime': '12:00',
     'Temp': 39.8, 'Shock': True, 'Sex': 2,
     'CoughLevel': 2, 'CoughDate': '13/07/2020',
     'hct': 4.0, 'wbc': 3.0, 'LabSampleStudyDay': 1},

    {'StudyNo': '32dx-004',
     'enDate':'14/07/2020', 'enTime': '13:00',
     'Temp': 37.4, 'Shock': False, 'Sex': 1,
     'hct': 7.0, 'wbc': 1.0, 'LabSampleStudyDay': 2},

]

# Create DataFrames
template = pd.DataFrame(template)
data = pd.DataFrame(data)

# Create blender
blender = Blender(widgets=[DateTimeMergeWidget(),
                           RenameWidget(),
                           ReplaceWidget(),
                           DateFromStudyDayWidget(),
                           EventWidget()])

# Fit blender to templates.
blender = blender.fit(info=template)

# Transform data
transformed = blender.transform(data)

# Stack data
stacked = blender.stack(transformed, index='study_number')

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")
print(stacked)

