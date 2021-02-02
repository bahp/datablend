"""
Issue 01
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import Blender
from datablend.core.widgets.format import FullTemplateWidget
from datablend.core.widgets.format import RenameWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'DateEnrol', 'to_name': 'date_enrol'},
    {'from_name': 'TimeEnrol', 'to_name': 'time_enrol'},
    {'from_name': 'DateIllness', 'to_name': 'date_illness'},
    {'from_name': 'TimeIllness', 'to_name': 'time_illness'},

    {'from_name': 'MucosalBlHist',
     'to_name': 'bleeding_mucosal',
     'to_replace': {True:1, False: 2},
     'timestamp': 'date_onset'},

    {'from_name': 'SkinBlHist',
     'to_name': 'bleeding_skin',
     'to_replace': {True: 1, False: 2},
     'timestamp': 'date_onset'},

    {'from_name': 'MucosalBlExam',
     'to_name': 'bleeding_mucosal',
     'to_replace': {True: True, False: False},
     'timestamp': 'date_enrolment'},

    {'from_name': 'SkinBlExam',
     'to_name': 'bleeding_skin',
     'to_replace': {True: True, False: False},
     'timestamp': 'date_enrolment'},

    {'from_name': 'date_enrolment',
     'to_name': 'date_enrolment',
     'datetime_date': 'DateEnrol',
     'datetime_time': 'TimeEnrol',
     'event': 'event_enrolment'},

    {'from_name': 'date_onset',
     'to_name': 'date_onset',
     'datetime_date': 'DateIllness',
     'datetime_time': 'TimeIllness',
     'event': 'event_onset'}
]

# Data
data = [
    {'StudyNo': '1-0016',
     'DateEnrol': '10/25/10 12:00 AM',
     'TimeEnrol': '11:05',
     'DateIllness': '10/24/10 12:00 AM',
     'TimeIllness': '14:00',
     'MucosalBlHist': 1,
     'SkinBlHist': 1,
     'MucosalBlExam': False,
     'SkinBlExam': False},

    {'StudyNo': '1-0099',
     'DateEnrol': '12/3/10 12:00 AM',
     'TimeEnrol': '15:10',
     'DateIllness': '12/3/10 12:00 AM',
     'TimeIllness': '14:00',
     'MucosalBlHist': 2,
     'SkinBlHist': 2,
     'MucosalBlExam': False,
     'SkinBlExam': True},

]


# ISSUE 01: TO FIX
# ----------------
# It is necessary here to convert the template
# and the data to dataframes before passing to
# the blender object. This should be done auto,
# just check whether it is a list, use pandas and
# verify that it is a valid BlenderTemplate
template = pd.DataFrame(template)
data = pd.DataFrame(data)

# ISSUE 02: TO FIX
# ----------------
# Check within the BlenderTemplate if there is
# column unit, and if not, just create an empty
# one.
template['unit'] = None

# Create blender
blender = Blender(widgets=[FullTemplateWidget()])

# Fit blender to templates.
# Warning: if template is not a dataframe it crashes.
blender = blender.fit(info=template)

# Transform data
transformed = blender.transform(data)


# ISSUE 03: TO FIX
# ----------------
# For some reason, there is a weird behaviour
# when stacking data. Note that there are different
# dates date_onset and date_enrollment and there
# are also two different columns matched to the
# same to_name.

# They are duplicated because the Stack widget gets
# timestamps not only from those included manually
# but also from events?

# The problem is renaming to same name creates two
# columns with same name.. how to know which one is
# used for which.
# Stacked data
stacked = blender.stack(transformed, index='StudyNo')

# Show
print("\nTemplate:")
print(template)
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")
print(stacked.sort_values(by=['StudyNo', 'date', 'column']))