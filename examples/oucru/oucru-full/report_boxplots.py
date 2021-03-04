# Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Specific libraries
from pathlib import Path

# -----------------------------------
# Configuration
# -----------------------------------
# Configure
sns.set_theme(style="ticks", palette="pastel")


# -----------------------------------
# Methods
# -----------------------------------
def select_dtypes_numeric(df):
    """Find those columns that can be casted to number.

    Parameters
    ----------
    df: pd.DataFrame

    Returns
    -------
        pd.DataFrame
    """
    # Numeric columns
    include = []

    # Loop
    for c in sorted(df.column.unique()):
        try:
            pd.to_numeric(df[df.column == c].result, errors='raise')
            include.append(c)
        except Exception as e:
            print("Ignoring.. %20s -> %s" % (c,e))

    # Return
    return include


# -----------------------------------
# Constants
# -----------------------------------
# Path with data
path_data = Path('./resources/datasets/combined/combined_stacked.csv')

# ------------------------------
# Load data
# ------------------------------
# Load data
data = pd.read_csv(path_data, parse_dates=['date'])

# -------------------------------------------
# Compare distributions for numeric variables
# ------------------------------------------

# Include
include = select_dtypes_numeric(data)

# Select numeric variables
#df_numbers = combined.select_dtypes(include='numbers')

# Select
df_numbers = data[data.column.isin(include)]
df_numbers = df_numbers.drop_duplicates()
df_numbers.result = pd.to_numeric(df_numbers.result)

# Loop plotting by uit
for idx, df in df_numbers.groupby('unit'):
    # Create figure
    plt.figure()
    # Draw a nested boxplot
    sns.boxplot(x="column", y="result",
                hue="dsource", whis=1.5,
                data=df)
    # Format
    sns.despine(offset=10, trim=True)
    plt.title(idx)
    plt.tight_layout()

# Show
plt.show()