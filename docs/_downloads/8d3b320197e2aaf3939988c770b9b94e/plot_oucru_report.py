"""
oucru_report
=================================
"""

# Libraries
import pandas as pd

# Specific libraries
from pathlib import Path

# DataBlend libraries
from datablend.core.repair.report import oucru_report

# --------------------------
# Configuration
# --------------------------
# Create path data
path_data = Path('../oucru/oucru-full/resources/datasets/tidy')

# --------------------------
# Main
# --------------------------

# Loop filling data
for path in sorted(list(path_data.glob('*.csv'))):
    # Show information
    print("\n\nLoading... %s" % path.stem)
    # Read file
    data = pd.read_csv(path, low_memory=False)
    # Create report
    oucru_report(data)