"""
Issue 02
========

When building the templates we prefer to indicate the timestamp with
readable values such as date_analysis. However, the StackWidget uses
the original values such as AnalysisDate to parse elements.

This code is meant to try/test such behaviour.

.. note: We do the stack with the original because in some situations
         we might want to have two different columns mapped to the same
         'to_name'. For this to work we first need to stack the data
         based on 'from_name' and then rename the 'column' values.
"""

# Import
import pandas as pd

# DataBlend library
from datablend.core.blend.blender import Blender
from datablend.core.widgets.format import FullTemplateWidget

# ------------------------
# Constants
# ------------------------
# Template
template = [
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'AnalysisDate', 'to_name': 'date_analysis'},
    {'from_name': 'WBC', 'to_name': 'wbc', 'timestamp': 'date_analysis'},
    {'from_name': 'PLT', 'to_name': 'plt', 'timestamp': 'date_analysis'},
]

# Data
data = [
    {'StudyNo': '1-0016',
     'AnalysisDate': '10/25/10 12:00 AM',
     'WBC': 12.5,
     'PLT': 13.8},
]

# Convert to pd.DataFrame
template = pd.DataFrame(template)
data = pd.DataFrame(data)

# ------------------------
# Main
# ------------------------
# Create blender
blender = Blender(widgets=[FullTemplateWidget()])

# Fit blender to templates.
blender = blender.fit(info=template)

# Transform data
transformed = blender.transform(data)

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