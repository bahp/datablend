"""
Repair Tidy data from .yaml
=================================

See :download:`corrector.yaml <./../../../examples/correctors/corrector.yaml>`.

"""
# Import
import numpy as np
import pandas as pd

# DataBlend library
from datablend.core.widgets.tidy import TidyWidget
from datablend.core.repair.schema import SchemaCorrectionTidy

# ------------------------
# Constants
# ------------------------
# Transformed data
data = [
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'bt', 'result': 7.2, 'unit': 'celsius'},
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'age', 'result': 32, 'unit': 'year'},
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'gender', 'result': 'Male'},
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'pregnant', 'result': False},
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'pcr_dengue_serotype', 'result': 'DENV-1'},
    {'id': '32dx-001', 'date': '2020/12/05', 'column': 'pcr_dengue_serotype', 'result': 'DENV-2'},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'bt', 'result': 38.2},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'bt', 'result': 39.7},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'age', 'result': 4},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'gender', 'result': 'Female'},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'pregnant', 'result': True},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'pregnant', 'result': False},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'pcr_dengue_serotype', 'result': 'DENV-3'},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'pcr_dengue_serotype', 'result': 'DENV-4'},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'wbc', 'result': '15'},
    {'id': '32dx-002', 'date': '2020/12/05', 'column': 'wbc', 'result': '18'},
    {'id': '32dx-002', 'date': '2020/12/06', 'column': 'wbc', 'result': '19'},
    {'id': '32dx-002', 'date': '2020/12/07', 'column': 'wbc', 'result': '20'},
    {'id': '32dx-003', 'date': '2020/12/05', 'column': 'vomiting', 'result': 'False'},
    {'id': '32dx-003', 'date': '2020/12/05', 'column': 'vomiting', 'result': False},
    {'id': '32dx-004', 'date': '2020/12/04', 'column': 'wbc', 'result': 5},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'vomiting', 'result': 'False'},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'vomiting', 'result': False},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'vomiting', 'result': 'True'},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'vomiting', 'result': True},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'bt', 'result': 36.5},
    {'id': '32dx-004', 'date': '2020/12/06', 'column': 'wbc', 'result': 4},
    {'id': '32dx-004', 'date': '2020/12/08', 'column': 'bt', 'result': 39.5},
    {'id': '32dx-004', 'date': '2020/12/04', 'column': 'event_admission', 'result': True},
    {'id': '32dx-004', 'date': '2020/12/05', 'column': 'event_admission', 'result': True},
    {'id': '32dx-004', 'date': '2020/12/06', 'column': 'event_admission', 'result': False}
]

# Parameters
index = ['id', 'date', 'column']
value = 'result'

# Filepath
filepath = 'corrector.yaml'

# --------------------
# Main
# --------------------
# Create data
data = pd.DataFrame(data)

# Create wid1get
widget = TidyWidget(index=index, value=value)

# Transform (keep all)
transform, duplicated = \
    widget.transform(data, report_duplicated=True)

# Create schema corrector
schema_corrector = \
    SchemaCorrectionTidy(filepath=filepath)

# Show schema transformations summary

# Correct schema
corrected, report = \
    schema_corrector.transform(transform)

"""
# Show report
for k,v in report.items():
    print("\n\nReport for {0}".format(k))
    print(v)
"""

# Show
print("\nStacked:")
print(data)
print("\nDuplicated:")
print(duplicated)
print("\nTidy (all):")
print(transform)
print("\nCorrected:")
print(corrected)
print("\nDtypes:")
print(corrected.dtypes)