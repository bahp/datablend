"""
StaticWidget
===========================

.. deprecated
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.widgets.tidy import StaticTidyWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Temp', 'to_name': 'bt'},
    {'from_name': 'Sex', 'to_name': 'gender', 'static': True},
    {'from_name': 'Age', 'to_name': 'age', 'static': True}
]

# Transformed data
trans = [
    {'study_number': '32dx-001', 'bt': 37.2, 'age': 12, 'gender': 1},
    {'study_number': '32dx-001', 'bt': 39.2},
    {'study_number': '32dx-002', 'bt': 36.5, 'age': 15, 'gender': 1},
    {'study_number': '32dx-002', 'bt': 39.3, 'age': 14},
    {'study_number': '32dx-003', 'bt': 39.8, 'age': 30, 'gender': 2},
    {'study_number': '32dx-004', 'bt': 37.4, 'age': 35, 'gender': 1}
]

# Create data
data = pd.DataFrame(trans)

# Create widget
widget = StaticTidyWidget(by='study_number').fit(template)

# Transform
transformed = widget.transform(data)

# Transform
transformed_manual = widget.transform(data, l=['gender', 'age'])

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nTransformed manual:")
print(transformed_manual)
print("\nAre they equal? %s" % transformed.equals(transformed_manual))