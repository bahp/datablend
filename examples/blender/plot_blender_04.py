"""
Blender with various widgets
============================

Generic example to show the functionality of Blender. It focuses
on the transformations: (i) DateTimeMergeWidget, (ii) ReplaceWidget,
(iii) EventWidget and (iv) DataFromStudyDayWidget. In addition it
converts the data to stacked and tidy structures.

.. warning: The order of the ``Widgets`` passed to ``Blender`` matters.

"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import Blender
from datablend.core.widgets.format import ReplaceWidget
from datablend.core.widgets.format import DateTimeMergeWidget
from datablend.core.widgets.format import DateFromStudyDayWidget
from datablend.core.widgets.format import EventWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo',
     'to_name': 'study_number'},

    # Example datetime merge
    {'from_name': 'date_enrolment',
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
     'timestamp': 'date_enrolment',
     'default': False},

    # Example replace widget
    {'from_name': 'Sex', 'to_name': 'gender',
     'to_replace': {1: 'Male', 2: 'Female'},
     'timestamp': 'date_enrolment',
     'static': True},

    # Example parameters to be stacked.
    # Note that uses a different date.
    {'from_name': 'CoughLevel',
     'to_name': 'cough_level',
     'timestamp': 'cough_date',
     'default': 0},

    {'from_name': 'CoughDate',
     'to_name': 'cough_date',
     'datetime': True},

    # Example event
    {'from_name': 'DateIllness',
     'to_name': 'date_onset',
     'datetime': True,
     'event': 'event_onset',
     'default': False},

    # Example study day
    {'from_name': 'LabSampleStudyDay',
     'to_name': 'lab_study_day'},

    {'from_name': 'date_laboratory',
     'to_name': 'date_laboratory',
     'study_day_col': 'LabSampleStudyDay',
     'study_day_ref': 'date_enrolment'},

    {'from_name': 'hct',
     'to_name': 'hct',
     'timestamp': 'date_laboratory',
     'unit': '%'},

    {'from_name': 'wbc',
     'to_name': 'wbc',
     'timestamp': 'date_laboratory',
     'unit': '10^9U/L'}

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
     'enDate': '12/07/2020', 'enTime': '11:00',
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
     'enDate': '14/07/2020', 'enTime': '13:00',
     'Temp': 37.4, 'Shock': False, 'Sex': 1,
     'hct': 7.0, 'wbc': 1.0, 'LabSampleStudyDay': 2},

]

# -----------------------
# Main
# -----------------------
# Create DataFrames
template = pd.DataFrame(template)
data = pd.DataFrame(data)

# Create blender
blender = Blender(widgets=[DateTimeMergeWidget(),
                           ReplaceWidget(),
                           EventWidget(),
                           DateFromStudyDayWidget()])

# Fit blender to templates.
blender = blender.fit(info=template)

# Transform data
transformed = blender.transform(data)

# Stack data
stacked = blender.stack(transformed, index='StudyNo')

# Remove time information to group by day.
stacked.date = stacked.date.dt.date

# Tidy data
tidy = blender.tidy(stacked, index=['StudyNo', 'date', 'column'])

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")
print(stacked)
print("\nTidy:")
print(tidy)