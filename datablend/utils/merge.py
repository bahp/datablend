# Libraries
import pandas as pd


def merge_day_month_year(data, day, month, year):
    """This method is not implemented yet."""
    pass


def merge_date_time(data, date_column, time_column=None):
    """This method merges columns date and time

    .. note: If time is missing default is 00:00.
    .. note: Also convert date using dt.apply(str).

    import datetime
    datetime.time.fromisoformat()

    Parameters
    ----------

    Returns
    -------

    """
    if not date_column in data:
        print("Column <%s> not found!" % date_column)

    if not time_column in data:
        print("Column <%s> not found!" % time_column)

    # Convert dates
    data[date_column] = pd.to_datetime(data[date_column])

    # Fill empty times with default value
    data[time_column] = data[time_column].fillna('00:00')

    # Format
    date = data[date_column].dt.strftime('%Y-%m-%d')
    time = data[time_column]

    # Return
    return pd.to_datetime(date + ' ' + time)
