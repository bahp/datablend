# Units

"""Describing which variables are static.

.. note: We define as static those variables that do not
         change during the data collection period. Note
         that does not usually vary during the time the
         patient is admitted to the hospital.

.. todo: haematocrit_max because it contains the word
         haematocrit it should be automatically classified
         as laboratory
"""


def find_static():
    return None


static = [
    'age',
    'gender',
    'height',
    'weight',
    'pregnant',
    'diabetes',
    'anemia',
    'asthma',
    'hypertension',
    'peptic_ulcer',
    'renal_disease',
    'chronic_hepatitis',
    'coronary_heart_disease'
]

"""Describing levels.

.. note: If the variable has the suffix level, it contains just
         numbers and it has not been collected (null value) it 
         probably means that the minimum level should have beeen
         recorded.
         
         For example, clinicians will not recorded the abdominal
         pain if there wasn't any pain and therefore it could be
         represented with a 0.
"""


def find_levels(variable_names):
    """This method...

    .. note: Might need the dataframe to check ints!

    Returns
    -------
    list
        Variables with the word levels in it.
    """
    return [c for c in variable_names if 'level' in c]


"""Describing the units of the variables.

vital signs
laboratory
demographics
serology
pcr
ultrasound
urinalisis
xray
"""
units = [

    # Demographics
    # ------------
    {'name': 'age',
     'unit': 'year',
     'source': 'demographics'},

    {'name': 'gender',
     'source': 'demographics'},

    {'name': 'weight',
     'unit': 'Kg',
     'source': 'demographics'},

    {'name': 'height',
     'unit': 'cm',
     'source': 'demographics'},

    # Vital signs
    # -----------
    {'name': 'body_temperature',
     'unit': 'celsius',
     'source': 'vital'},

    {'name': 'respiratory_rate',
     'unit': 'breaths per minute',
     'source': 'vital'},

    {'name': 'pulse',
     'unit': 'bpm',
     'source': 'vital'},

    {'name': 'dbp',
     'unit': 'mmHg',
     'source': 'vital'},

    {'name': 'sbp',
     'unit': 'mmHg',
     'source': 'vital'},

    # Laboratory
    {'name': 'haematocrit_percent', 'unit': '%', 'source': 'laboratory'},
    {'name': 'haematocrit_max', 'source': 'laboratory'},
    {'name': 'plt', 'unit': 'K/uL', 'source': 'laboratory'},
    {'name': 'wbc', 'unit': 'K/uL', 'source': 'laboratory'},
    {'name': 'neutrophils_percent', 'unit': '%', 'source': 'laboratory'},
    {'name': 'lymphocytes_percent', 'unit': '%', 'source': 'laboratory'},
    {'name': 'monocytes_percent', 'unit': '%', 'source': 'laboratory'},
    {'name': 'haemoglobin', 'unit': 'g/dL', 'source': 'laboratory'},
    {'name': 'albumin', 'unit': 'g/dL', 'source': 'laboratory'},
    {'name': 'ast', 'unit': 'u/L', 'source': 'laboratory'},
    {'name': 'alt', 'unit': 'u/L', 'source': 'laboratory'},
    {'name': 'alb', 'source': 'laboratory'},
    {'name': 'creatinine', 'unit': 'umol/L', 'source': 'laboratory'},
    {'name': 'creatine_kinase', 'unit': 'u/L', 'source': 'laboratory'},
    {'name': 'lymphocytes', 'source': 'laboratory'},
    {'name': 'neutrophils', 'source': 'laboratory'},
    {'name': 'tk', 'source': 'laboratory'},
    {'name': 'tck', 'source': 'laboratory'},
    {'name': 'fibrinogen', 'source': 'laboratory'},
    {'name': 'inr', 'source': 'laboratory'},

    # PCR
    {'name': 'pcr_dengue_load', 'unit': 'copies/mL'},

    # Serology
    {'name': 'igm', 'unit': 'g/L', 'source': 'sero'},
    {'name': 'igg', 'unit': 'g/L', 'source': 'sero'},
    {'name': 'igm_interpretation', 'source': 'sero'},
    {'name': 'igg_interpretation', 'source': 'sero'},
]


def prefix_sources(tidy):
    """This method..."""
    # Get sources
    sources = {r['name']: '%s_%s' % (r['source'], r['name'])
               for r in units if 'source' in r}
    # Replace
    tidy = tidy.rename(columns=sources)
    # Retur
    return tidy


def find_sources():
    pass

# Maybe I need to create a default template here just with
# the name, unit, static, etc.

# Names

# Etc
