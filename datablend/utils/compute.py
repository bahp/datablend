# Libraries
import numpy as np
import pandas as pd

# Specific
from datetime import date
from datetime import timedelta


def age(dob, date_reference=None):
    """This method calculates the age.

    Parameters
    ----------

    Returns
    --------

    """
    # Set the reference date
    if date_reference is None:
        date_reference = date.today()
    # Compute and return age
    return date_reference.year - dob.year - \
           ((date_reference.month, date_reference.day) < \
            (dob.month, dob.day))


def dob(age, date_reference=None):
    """This method calculates the date of birth.

    Parameters
    ----------

    Returns
    --------

    """
    # Set the reference date
    if date_reference is None:
        date_reference = date.today()
    # Ensure that is an integer
    try:
        age = int(age)
    except:
        return np.nan
    # Compute and return age
    return date_reference - timedelta(days=365*age)






def datetime(date, time):
    """This method merges columns date and time

    .. note: If time is missing default is 00:00.
    .. note: Also convert date using dt.apply(str).

    Parameters
    ----------

    Returns
    -------

    """
    # Format date
    date = pd.to_datetime(date)
    date = date.strftime('%Y-%m-%d')

    # Format time
    time = '00:00' if pd.isnull(time) else time

    # Return
    return pd.to_datetime(date + ' ' + time)


def add_days(dates, days):
    """This method....

    Parameters
    ----------

    Returns
    -------
    """
    # Cast both to pandas series
    dates = pd.Series(dates)
    days = pd.Series(days)

    # Format
    dates = pd.to_datetime(pd.Series(dates))
    days = pd.Series(days).apply(np.ceil)
    days = days.apply(lambda x: pd.Timedelta(x, unit='D'))

    # Return
    return dates + days