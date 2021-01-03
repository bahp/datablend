"""
Blender with multiple inputs
============================

Example using ``Blender`` with data collected from several sources.

.. note:: Each data source has a different ``BlenderTemplate``.

.. note:: ``Pandas`` reads xlsx files with different sheets as a dictionary
          where the key is the worksheet name and the value is the
          dataframe. Therefore, xlsx files loaded with pandas can be
          inputed to ``Blender`` as in the example below.

"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend import Blender
from datablend.core.widgets import RenameWidget
from datablend.core.widgets import ReplaceWidget

# ------------------------
# Constants
# ------------------------
# Templates
template_exam = [
    # Body Temperature
    {'from_name': 'Temp',
     'to_name': 'body_temperature',
     'timestamp': 'date_exam',
     'unit': 'celsius'},

    # Gender
    {'from_name': 'Sex', 'to_name': 'gender',
     'to_replace': {'Male': 1, 'Female': 2},
     'timestamp': 'date_exam'},
]

# .. note: The same blender instance will be used for the data. Thus,
#          since the ReplaceWidget is used, the column to_replace needs
#          to be included in both templates (see to_replace: None below).

template_lab = [
    # HCT
    {'from_name': 'hct',
     'to_name': 'hct',
     'timestamp': 'date',
     'unit': '%'},

    # WBC
    {'from_name': 'wbc',
     'to_name': 'wbc',
     'timestamp': 'date',
     'unit': '10^9U/L',
     'to_replace': None}

]

# Data
data_exam = [
    {'pid': '32dx-001', 'date_exam': '10/07/2020', 'Temp': 37.2, 'Sex': 1},
    {'pid': '32dx-002', 'date_exam': '08/07/2020', 'Temp': 37.5, 'Sex': 2},
    {'pid': '32dx-003', 'date_exam': '10/07/2020', 'Temp': 36.7, 'Sex': 2},
]

data_lab = [
    {'pid': '32dx-001', 'date': '11/07/2020', 'hct': 1.0, 'wbc': 1.5},
    {'pid': '32dx-001', 'date': '12/07/2020', 'hct': 2.0, 'wbc': 2.5},
    {'pid': '32dx-001', 'date': '13/07/2020', 'hct': 3.0, 'wbc': 3.5},
    {'pid': '32dx-001', 'date': '14/07/2020', 'hct': 4.0, 'wbc': 4.5},
    {'pid': '32dx-001', 'date': '15/07/2020', 'hct': 5.0, 'wbc': 5.5},
    {'pid': '32dx-002', 'date': '09/07/2020', 'hct': 1.0, 'wbc': 3.5},
    {'pid': '32dx-002', 'date': '10/07/2020', 'hct': 3.0, 'wbc': 3.2},
    {'pid': '32dx-002', 'date': '11/07/2020', 'hct': 3.0, 'wbc': 4.3},
    {'pid': '32dx-003', 'date': '20/07/2020', 'hct': 2.0, 'wbc': 1.5},
    {'pid': '32dx-003', 'date': '21/07/2020', 'hct': 4.0, 'wbc': 2.5},
]


# Create templates dictionary
templates = {
    'EXAM': pd.DataFrame(template_exam),
    'LAB': pd.DataFrame(template_lab)
}

# Create data dictionary
data = {
    'EXAM': pd.DataFrame(data_exam),
    'LAB': pd.DataFrame(data_lab)
}

# Create blender
blender = Blender(widgets=[RenameWidget(),
                           ReplaceWidget()])

# Fit blender to templates.
blender = blender.fit(info=templates)

# Transform data
transformed = blender.transform(data)

# Stack data
stacked = blender.stack(transformed, index='pid')

# Show
print("\nOriginal:")
for k,v in data.items():
    print("\n%s:" % k)
    print(v)

print("\nTransformed:")
for k,v in transformed.items():
    print("\n%s:" % k)
    print(v)

print("\nStacked:")
for k,v in stacked.items():
    print("\n%s:" % k)
    print(v)

