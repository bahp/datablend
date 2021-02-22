# Libraries
import pandas as pd
import numpy as np

# DataBlend libraries
from datablend.utils.pandas import nanunique

# Check other consistencies
from datablend.core.consistency import report_unique_value
from datablend.core.consistency import consistency_bleeding
from datablend.core.consistency import consistency_shock
from datablend.core.consistency import consistency_events
from datablend.core.consistency import consistency_stay

# ----------------------------------
#   Create data
# ----------------------------------
# Create sample DataFrame
data = {
    'StudyNo': [1, 1, 1, 2, 2, 2],
    'date': ['18/10/2020', '20/10/2020', '23/10/2023', '21/10/2020', '22/10/2020', '23/10/2020'],
    'gender': ['M', 'M', 'F', 'None', 'Female', 'Female'],
    'beauty': [True, False, None, False, False, False],
    'age': [2, 10, None, False, 5, 8],
    'bleeding': [1, 1, 0, 0, 0, 0],
    'bleeding_skin': [1, 0, 1, 0, 0, 0],
    'shock': [1, 0, 1, 0, 1, 0],
    'shock_multiple': [1, 1, 1, 0, 0, 0],
    'event_admission': [0, None, None, 1, 1, 0],
    'event_discharge': [1, 0, 0, 1, 0, 0]
}

# Create DataFrame
df = pd.DataFrame(data)
df.date = pd.to_datetime(df.date)

print(df)

# -------------------------
# Useful code
# -------------------------
# Aggregation example
print("\n" + "="*80)
print("Aggregation example:\n\n")
aux = df[['StudyNo', 'gender', 'beauty', 'age']] \
        .groupby(by='StudyNo') \
        .agg(['max', 'nunique', nanunique])
print(aux)
print("\n" + "="*80)


# How to count elements of each value.
print("\n" + "="*80)
print("Crosstab example:\n")
print(pd.crosstab(df.StudyNo, df.gender))
print("\n" + "="*80)

# -------------------------
# Consistency
# -------------------------
tidy, msg1 = consistency_shock(df, verbose=10)
tidy, msg2 = consistency_events(df, verbose=10)
tidy, msg3 = consistency_stay(df, verbose=10)

print(msg1)
print(msg2)
print(msg3)


# -------------------------
# Check date filtering
#--------------------------
# Library
from datablend.core.consistency import outlier_dates_correction

# Ensure that it is date.
dates = ['2020/10/19',
         '2020/10/20',
         '2020/10/21',
         '2020/10/22',
         '2020/10/24',
         '2022/10/25']


df = pd.DataFrame()
df['date'] = pd.to_datetime(dates)
df['vals'] = np.arange(6)
df['StudyNo'] = np.repeat(['StudyNo'], 6)

print("----")
print(df)

df.date = \
    df.groupby(by=['StudyNo']) \
        .date.transform(outlier_dates_correction, coef=1)

print(df)

"""
print(df)
print(df.dtypes)

def f(x):
    print(x)
    print(x.mean())
    import sys
    sys.exit()

#print(tidy.groupby(['StudyNo']).date.mean())
"""

print(df)
