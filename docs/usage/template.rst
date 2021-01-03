Template
==========

The ``BlenderTemplate`` instance represents the transformations to be applied
to each of the columns in the data. Some examples of these transformation are
renaming columns, replacing values, merging date and time columns into a single
datetime column, etc. However, in order to ``fit`` a ``BlenderTemplate`` we
first need to define the transformations (see below).

.. note:: This table can be a list of dicts or a pandas DataFrame. Thus, it
          can be easily loaded from a csv, xlsx or json file.

============ ============== ============== ========== =============== ====
from_name    to_name        timestamp      to_replace event           unit
============ ============== ============== ========== =============== ====
StudyNo      study_number   str
DateAd       date_admission datetime64[ns]            event_admission year
Age          age            date_admission
Sex          gender         date_admission {'Male':1}
============ ============== ============== ========== =============== ====

Let's understand each of the columns supported:

from_name: str
    Refers to the name of the column in the original dataset.

to_name: str (``RenameWidget``)
    Refers to the name of the column in the formatted dataset.

type: str
    Indicates the type of the column (serves as guidance).

to_replace: dict-like (``ReplaceWidget``)
    These dictionaries indicate the values that need to be replaced from
    the original dataset into the formatted one. For instance, if the
    original dataset used the following coding system (1 is True, 2 False)
    the dictionary would be {True: 1, False: 2}. Note that strings should
    be quoted (e.g. {'Positive': 1, 'Negative': 2, 'Equivocal': 3). It
    is also possible to include None (e.g. {True: 1, False: 2, None: 3})

datetime: boolean
    Indicates whether the feature is a datetime. It is redundant because
    type already includes the datetime64[ns] type. The aim of the datetime
    information is to combine columns containing date and time information
    separately.

datetime_date: str (``DateTimeMergeWidget``)
    Refers to the from_name of the column with the date information.

datetime_time: str (``DateTimeMergeWidget``)
    Refers to the from_name of the column with the time information.

event: str (``EventWidget``)
    Name to use for the newly created event. Note that can only be used
    for data columns which contain dates.

study_day_col: str (``DateFromStudyDayWidget``)
    Refers to the name of the column in the formatted dataset with the
    study day information. Note that the column in the dataset should
    contain integer representing the study day (e.g 1st, 2nd, 3rd, ...)

study_day_ref: str (``DateFromStudyDayWidget``)
    Refers to the name of the column in the formatted dataset with the
    date in which the study commenced. Note that the column in the
    dataset should represent a date(time).

timestamp: str (``StackWidget``)
    Refers to the name of the column in the formatted dataset with the
    date associated to the feature. This date will be used when
    stacking data.

unit: str (``StackUnitWidget``)
    The unit of measurement.
