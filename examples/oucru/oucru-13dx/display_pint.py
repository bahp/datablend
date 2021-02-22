# Libraries
import inspect
import pandas as pd

# Specific
from optparse import OptionParser

# Libraries for pint
from pint import UnitRegistry


# -----------------------------------------
# Main
# -----------------------------------------
# Create
ureg = UnitRegistry()  #auto_reduce_dimensions = False

# Define units
ureg.define('beat = count')
ureg.define('breath = count')
ureg.define('copy = count')
ureg.define('percent = count = %')

# Show all attributes
#print(vars(ureg).keys())
"""
methods = inspect.getmembers(ureg, predicate=inspect.ismethod)
functions = inspect.getmembers(ureg, predicate=inspect.isfunction)

#print(ureg.has_option('beat'))
print(ureg.get_name('beat'))
print(ureg.get_name('feo'))

#print(methods)
for e in methods:
    print(e[0])

# Show all units
supported_units = pd.DataFrame(vars(ureg)['_units'].keys()).sort_values(0)

#print(supported_units)

#supported_units.to_csv('units.csv')

#supported

distance = 42 * ureg.kilometers
"""

dictionary = {
    'hct': 1 * ureg('U/L'),                            # L/L
    'plt': 1 * ureg('kilocount/uL'),                 # K/uL
    'alb': 1 * ureg('mg/dL'),                        # g/dL, g/L, U/L, umol/L
    'wbc': 1 * ureg('kilocount/uL'),                 # K/uL
    'neutrophils': 1 * ureg('gigacount/L'),          # x10^9/L or % of WBC
    'lymphocytes': 1 * ureg('gigacount/L'),          # x10^9/L or % of WBC
    'monocytes': 1 * ureg('gigacount/L'),            # x10^9/L or % of WBC
    'haemoglobin': 1,                                # g/dL
    'ast': 1 * ureg('count/L'),                      # IU/L
    'alt': 1 * ureg('count/L'),                      # U/L
    'alp': 1 * ureg('count/L'),                      # U/L
    'bil': 1 * ureg('mg/dL'),                        # umol/L or mg/dL
    'creatinine': 1,                                 # mg/dL or umol/L
    'creatine_kinase': 1 * ureg('ng/mL'),            # u/L or ng/mL
    'sodium': 1 * ureg('mmol/L'),                    # mmol/L
    'potasium': 1 * ureg('mmol/L'),                  # mmol/L
    'urea': 1 * ureg('mg/dL'),                       # mmol/L or mg/dL
    'lactate': 1 * ureg('mmol/dL'),                  # mg/dL or mmol/dL
    'tk': 1,
    'tck': 1,
    'fibrinogen': 1 * ureg('g/L'),                   # g/L
    'inr': 1,
    'body_temperature': 1 * ureg.celsius,            # celsius
    'age': 2 * ureg.year,                            # year
    'height': 1 * ureg.cm,                           # cm
    'weight': 1 * ureg.kg,                           # kg
    'pcr_dengue_load': 1 * ureg('copy/mL'),          # copies/mL
    'igm': 1 * ureg('count/mL'),                     # u/mL
    'igg': 1 * ureg('count/mL'),                     # u/ml
    'dbp': 1 * ureg.mmHg,                            # mmHg or millimeter_Hg
    'sbp': 1 * ureg.mmHg,                            # mmHg or millimeter_Hg
    'pulse': 1 * ureg('beats/minute'),                # beats_per_minute  (not in pint)
    'respiratory_rate': 1 * ureg('breaths/minute'),   # breaths_per_minute (not in pint)
    'hct_percent': 1 * ureg('percent')
}

# Create DataFrame
df = pd.Series(dictionary).sort_index()

# Show
print("\n\nUnits")
print(df)

# -----------------
# Conversion
# -----------------
# Conversion
speed = 10 * ureg.meters / ureg.second

# Convert
print("\n\nConversion")
print(speed)
print(speed.to(ureg.inch / ureg.minute))

# Convert inplace
speed.ito(ureg.inch / ureg.minute)

# -----------------
# Readability
# -----------------
# Units more readable
wavelength = 1550 * ureg.nm

print("\n\nRadability")
print(wavelength)
print(wavelength.to_compact())

# ---------------------
# Convert to base units
# ---------------------
# Convert to base units
height = 5.0 * ureg.foot + 9.0 * ureg.inch

print("\n\nConvert to base")
print(height)
print(height.to_base_units())

# Convert to base inplace
height.ito_base_units()

# ------------------------
# Dimensionality reduction
# ------------------------
density = 1.4 * ureg.gram / ureg.cm**3
volume = 10*ureg.cc
mass = density*volume

print("Reduced")
print(mass)
print(mass.to_reduced_units())

# Convert units
mass.ito_reduced_units()

# ------------------------
# User input
# ------------------------
# Define user input
user_input = '2.54 * centimeter to inch'
src, dst = user_input.split(' to ')
Q_ = ureg.Quantity

# Show
print(Q_(src).to(dst))