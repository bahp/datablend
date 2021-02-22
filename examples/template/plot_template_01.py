"""
Fitting a blender template
===========================
"""

# Import
import pandas as pd

# DataBlend libraries
from datablend.core.blend.template import BlenderTemplate

# ------------------------
# Constants
# ------------------------
# Template
template = [
    # Example rename widget
    {'from_name': 'StudyNo', 'to_name': 'study_number'},
    {'from_name': 'Temp', 'to_name': 'body_temperature'},
    {'from_name': 'Shock', 'to_name': 'shock'},
    {'from_name': 'Sex', 'to_name': 'gender'}
]

# ------------------------
# Main
# ------------------------
# Create blender DataFrame template
bt_df = pd.DataFrame(template)

# Create blender template
bt1 = BlenderTemplate().fit(bt_df)
bt2 = BlenderTemplate().fit(template)

# Show templates
print(bt1)
print(bt2)

# Replace from_name to to_name values.
print("\nMap replace {from_name: to_name}")
print(bt1.map_kv(key='from_name',
                 value='to_name'))