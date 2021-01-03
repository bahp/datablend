"""
RenameWidget
===========================
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.widgets.tidy import LevelTidyWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Pain', 'to_name': 'pain_level'}
]

# Transformed data
trans = [
    {'study_number': '32dx-001', 'pain_level': 1},
    {'study_number': '32dx-001', 'pain_level': 4},
    {'study_number': '32dx-002'},
    {'study_number': '32dx-003', 'pain_level': 4},
    {'study_number': '32dx-003'}
]

# Create data
data = pd.DataFrame(trans)

# Create widget
widget = LevelTidyWidget().fit(template)

# Transform
transformed = widget.transform(data)

# Show
print("\nOriginal:")
print(data)
print("\nTransformed:")
print(transformed)
print("\nStacked:")