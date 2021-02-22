# Units
import numpy as np

"""Describing which variables are static.

.. note: We define as static those variables that do not
         change during the data collection period. Note
         that does not usually vary during the time the
         patient is admitted to the hospital.

.. todo: haematocrit_max because it contains the word
         haematocrit it should be automatically classified
         as laboratory
"""


# ------------------------------------------------------
# TextWrapper config
# ------------------------------------------------------
# Import library
import textwrap

# Create object
textwrapper = textwrap.TextWrapper(width=80,
    break_long_words=False, replace_whitespace=False)


# ------------------------------------------------------
# Unit registry config
# ------------------------------------------------------
# Libraries for pint
from pint import UnitRegistry

# Create
ureg = UnitRegistry()  #auto_reduce_dimensions = False

# Define units
ureg.define('beat = count')
ureg.define('breath = count')
ureg.define('copy = count = copies')
ureg.define('percent = count')
#ureg.define('reaction')


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
]

default_false = [

    'lathargy_severe',

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

"""

    STATIC
    ======

    The functions that have been considered so far to input data 
    for static features and their implications are described in
    the list below:
     
    - max: Completes all the for the patient with max.
    
        age: if patient's birthday occurs during stay and
             he passes from 4 to 5 years, then 5 will be
             selected and he was indeed closer to 5.
        
        Bool: For those bool columns, it prioritises a
              positive finding. For instance, if shock is
              1 at least once, then all rows for the 
              patient will be completed with 1.
              
    - mode: Completes all rows for the patient with the mode.
    
        gender: If several genders (it should not happen) it
                will complete with the most common. If no value
                found they will remain nan.
     
    - mean Completes all rows for the patient with the mean.
    
        weight: If several values found, it will compute the
                mean over all the rows for the patient. Thus
                small variations will not be taken into 
                account.
             

"""

GROUPBY = 'StudyNo'

units = [

    #
    {'name': 'date',
     'transformations': [
         ('outlier_dates_correction', {'groupby': GROUPBY, 'coef':2.5})
    ]},

    # Demographics
    # ------------
    {'name': 'age',
     'unit': 'year',
     'dtype': int,
     'range': {
         'absolute': (0, 100, 'year'),
     },
     'source': 'demographics',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ]},

    {'name': 'gender',
     'categories': ['Male', 'Female'],
     'source': 'demographics',
     'static': 'mode'},

    {'name': 'weight',
     'unit': 'kg',
     'dtype': np.float64,
     'range': {
         'absolute': (2, 100, 'kg')
     },
     'source': 'demographics',
     'static': 'mean'},

    {'name': 'height',
     'unit': 'cm',
     'dtype': np.float64,
     'range': {
         'absolute': (50, 200, 'cm'),
     },
     'source': 'demographics',
     'static': 'mean',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'mean'}),
     ]},

    {'name': 'anorexia',
     'dtype': np.bool,
     'source': 'demographics',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'default': False},

    {'name': 'pregnant',
     'dtype': np.bool,
     'source': 'demographics',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'default': False},

    {'name': 'diabetes',
     'dtype': np.bool,
     'source': 'demographics',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'default': False},

    {'name': 'asthma',
     'dtype': np.bool,
     'source': 'demographics',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'default': False},

    {'name': 'anemia',
     'dtype': np.bool,
     'source': 'demographics',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'static': 'max'},

    {'name': 'hypertension',
     'dtype': np.bool,
     'source': 'demographics',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'static': 'max'},

    {'name': 'peptic_ulcer',
     'dtype': np.bool,
     'source': 'demographics',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'static': 'max'},

    {'name': 'chronic_hepatitis',
     'dtype': np.bool,
     'source': 'demographics',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
     ],
     'static': 'max'},

    # Vital signs
    # -----------
    {'name': 'body_temperature',
     'unit': 'celsius',
     'dtype': np.float64,
     'range': {
         'absolute': (35, 43, 'celsius'),
     },
     'source': 'vital',
     'transformations': [
         ('order_magnitude_correction', {'range': (35, 43), 'orders': [10, 100]}),
         ('range_correction', {'range': (35, 43)})
     ]},

    {'name': 'respiratory_rate',
     'unit': 'breath/minute',
     'dtype': int,
     'range': {
         'absolute': (10, 60, 'breath/minute'),
     },
     'transformations': [
         ('range_correction', {'range': (10, 60)})
     ],
     'source': 'vital'},

    {'name': 'pulse',
     'unit': 'beat/minute',
     'dtype': int,
     'range': {
         'absolute': (50, 200, 'beat/minute'),
     },
     'source': 'vital',
     'transformations': [
         ('range_correction', {'range': (50, 200)})
     ]},

    {'name': 'dbp',
     'unit': 'mmHg',
     'dtype': np.float64,
     'range': {
         'absolute': (40, 100, 'mmHg'),
     },
     'transformations': [
         ('range_correction', {'range': (40, 100)})
     ],
     'source': 'vital'},

    {'name': 'sbp',
     'unit': 'mmHg',
     'dtype': np.float64,
     'range': {
         'absolute': (50, 200, 'mmHg'),
     },
     'transformations': [
         ('range_correction', {'range': (50, 200)})
     ],
     'source': 'vital'},

    # Examination
    # -----------
    {'name': 'abdominal_pain',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'abdominal_tenderness',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'agitated', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'ascites', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'breath', 'source': 'examination'},
    {'name': 'dehydration', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'jaundice', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'diarrhoea',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'impairment', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'hepatomegaly', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'liver_acute', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'liver_involved', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'movement', 'dtype': np.bool, 'source': 'examination'},

    {'name': 'vomiting',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'skin_clammy',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'fbfill'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'skin_flush', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'skin_rash', 'dtype': np.bool, 'source': 'examination'},

    {'name': 'restlessness',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    {'name': 'cns_abnormal', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'cns_abnormal_signs', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'gcs_eye_movement', 'dtype': int, 'source': 'examination'},
    {'name': 'gcs_motor_response', 'dtype': int, 'source': 'examination'},
    {'name': 'gcs_verbal_response', 'dtype': int, 'source': 'examination'},

    {'name': 'bleeding',
     'dtype': np.bool,
     'static': 'fbfill',
     'default': False,
     'source': 'examination',
     },

    {'name': 'bleeding_gi', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_gum', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_mucosal', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_nose', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_severe', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_skin', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_urine', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_vaginal', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'bleeding_vensite', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'conjunctival_injection', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'lathargy_severe', 'dtype': np.bool, 'source': 'examination', 'static': 'fbfill', 'default': False},
    {'name': 'oedema_pulmonary', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'nasal_packing', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'respiratory_distress', 'dtype': np.bool, 'source': 'examination'},
    {'name': 'pulse_status', 'source': 'examination'},
    {'name': 'pleural_effusion',
     'dtype': np.bool,
     'source': 'examination',
     'static': 'fbfill',
     'default': False,
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'fbfill'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False}),
     ]},

    # ------------------
    # Laboratory results
    # ------------------
    {'name': 'haematocrit_percent',
     'unit': '%',
     'dtype': np.float64,
     'range': {
         'absolute': (0, 100, '%'),
         'normal': (10, 60, '%')
     },
    'transformations': [
         ('range_correction', {'range': (0, 100)})
     ],
     'source': 'laboratory'},

    {'name': 'haematocrit_max', 'dtype': np.float64, 'source': 'laboratory'},

    {'name': 'plt',
     'unit': 'kilocount/uL',
     'dtype': np.float64,
     'range': {
         'absolute': (1, 1600, 'kilocount/uL'),
     },
     'transformations': [
         ('range_correction', {'range': (1, 1600)})
     ],
     'source': 'laboratory'},

    {'name': 'wbc',
     'unit': 'kilocount/uL',
     'dtype': np.float64,
     'range': {
         'absolute': (0.1, 50, 'kilocount/uL'),
     },
     'source': 'laboratory'},

    {'name': 'neutrophils_percent',
     'unit': '%',
     'dtype': np.float64,
     'source': 'laboratory'},

    {'name': 'lymphocytes_percent', 'unit': '%', 'dtype': np.float64, 'source': 'laboratory'},

    {'name': 'monocytes_percent', 'unit': '%', 'dtype': np.float64, 'source': 'laboratory'},

    {'name': 'haemoglobin',
     'unit': 'g/dL',
     'dtype': np.float64,
     'range': {
         'absolute': (1, 30, 'g/dL'),
     },
     'source': 'laboratory'},

    {'name': 'albumin',
     'unit': 'g/dL',
     'dtype': np.float64,
     'range': {
         'absolute': (10, 60, 'g/dL'),
     },
     'source': 'laboratory'},

    {'name': 'ast',
     'unit': 'u/L',
     'dtype': np.float64,
     'range': {
         'absolute': (0, 1000, 'U/L')
     },
     'source': 'laboratory'},

    {'name': 'alt',
     'unit': 'u/L',
     'dtype': np.float64,
     'range': {
       'absolute': (0, 1000, 'U/L')
     },
     'source': 'laboratory'},

    {'name': 'alb',
     'unit': 'g/dL',
     'dtype': np.float64,
     'range': {
         'absolute': (10, 60, 'g/dL'),
     },
     'source': 'laboratory'},

    {'name': 'bili_total',
     'unit': 'umol/L',
     'dtype': np.float64,
     'range': {
         'absolute': (0.1, 99.9, 'umol/L'),
     },
     'source': 'laboratory'},

    {'name': 'bili_direct',
     'unit': 'umol/L',
     'dtype': np.float64,
     'range': {
         'absolute': (0.1, 99.9, 'umol/L'),
     },
     'source': 'laboratory'},

    {'name': 'sodium',
     'unit': 'mmol/L',
     'dtype': np.float64,
     'range': {
         'absolute': (100, 170, 'mmol/L'),
     },
     'source': 'laboratory'},

    {'name': 'potassium',
     'unit': 'mmol/L',
     'dtype': np.float64,
     'range': {
         'absolute': (1, 7, 'umol/L'),
     },
     'source': 'laboratory'},

    {'name': 'urea',
     'unit': 'mmol/L',
     'dtype': np.float64,
     'range': {},
     'source': 'laboratory'},

    {'name': 'creatinine', 'unit': 'umol/L', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'creatine_kinase', 'unit': 'u/L', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'lymphocytes', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'neutrophils', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'monocytes', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'tk', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'tck', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'fibrinogen', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'inr', 'dtype': np.float64, 'source': 'laboratory'},
    {'name': 'rbc'},
    {'name': 'ffp'},

    # PCR
    {'name': 'pcr_dengue_load', 'unit': 'copies/mL', 'dtype': np.float64},
    {'name': 'pcr_dengue_interpretation', 'static': 'mode'},
    {'name': 'pcr_dengue_serotype',
     'categories': ['<LOD', 'DENV-1', 'DENV-2', 'DENV-3', 'DENV-4'],
     'static': 'mode'},

    # Serology
    {'name': 'igm', 'unit': 'g/L', 'dtype': np.float64, 'source': 'serology'},
    {'name': 'igg', 'unit': 'g/L', 'dtype': np.float64, 'source': 'serology'},
    {'name': 'igm_interpretation', 'source': 'serology'},
    {'name': 'igg_interpretation', 'source': 'serology'},

    # --------
    # Outcomes
    # --------
    {'name': 'shock',
     'source': 'outcome',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False})
     ]},

    {'name': 'shock_multiple',
     'source': 'outcome',
     'static': 'max',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'max'}),
         ('fillna_correction', {'groupby': GROUPBY, 'method': False})
     ]},

    {'name': 'icd_code',
     'source': 'outcome',
     'static': 'mode',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'fbfill'}),
         # ('fillna_correction', {'groupby': GROUPBY, 'method': 'mode'}) # issues why?
     ]},

    {'name': 'outcome',
     'source': 'outcome',
     'static': 'mode',
     'transformations': [
         ('static_correction', {'groupby': GROUPBY, 'method': 'mode'}),
         #('fillna_correction', {'groupby': GROUPBY, 'method': False})
     ]},

    # --------
    # Events
    # --------
    {'name': 'event_admission',
     'transformations': [
         ('unique_true_value_correction', {'groupby': GROUPBY, 'keep': 'first'})
     ]},

    {'name': 'event_onset',
     'transformations': [
         ('unique_true_value_correction', {'groupby': GROUPBY, 'keep': 'first'})
     ]},

    {'name': 'event_enrolment',
     'transformations': [
         ('unique_true_value_correction', {'groupby': GROUPBY, 'keep': 'first'})
     ]},

    {'name': 'event_discharge',
     'transformations': [
         ('unique_true_value_correction', {'groupby': GROUPBY, 'keep': 'first'})
     ]},

    {'name': 'event_shock'}

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
