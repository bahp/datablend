"""
TidyDefault
===========================

.. deprecated
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.widgets.tidy import DefaultTidyWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Temp', 'to_name': 'bt'},
    {'from_name': 'Pain', 'to_name': 'pain_level', 'default': 0},
    {'from_name': 'Pregnant', 'to_name': 'pregnant', 'default': False}
]

# Transformed data
trans = [
    {'study_number': '32dx-001', 'bt': 37.2, 'pain_level': 1, 'pregnant': True},
    {'study_number': '32dx-001', 'bt': 39.2},
    {'study_number': '32dx-002', 'bt': 36.5, 'pain_level': 2, 'pregnant': True},
    {'study_number': '32dx-003', 'bt': 39.8},
    {'study_number': '32dx-004', 'bt': 37.4}
]

# Create data
data = pd.DataFrame(trans)

# Create widget
#widget = DefaultTidyWidget().fit(template)

# Transform
#transformed = widget.transform(data)

# Transform
#transformed_manual = widget.transform(data, map={'pain_level': 0, 'pregnant': False})

# Show
#print("\nOriginal:")
#print(data)
#print("\nTransformed:")
#print(transformed)
#print("\nTransformed manual:")
#print(transformed_manual)
#print("\nAre they equal? %s" % transformed.equals(transformed_manual))