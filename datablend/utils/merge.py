# Libraries
import pandas as pd


def merge_day_month_year(data, day, month, year):
    """This method is not implemented yet."""
    pass


def merge_date_time(dates, times,
                    kwargs_date={'errors': 'raise'},
                    kwargs_time={'errors': 'coerce'}):
    """This method merges columns date and time

    .. note: If time is missing or erroneous is set to 00:00.

    Parameters
    ----------
    dates: str-array or pd.Series
        Array of dates.

    times: str-array or pd.Series
        Array of times.
    """

    # Create dates
    date = pd.to_datetime(dates, **kwargs_date)

    # Create times
    time = pd.to_datetime(times, **kwargs_time)
    time = time.fillna(pd.Timestamp('1960-01-01'))

    # Create strings
    date = date.dt.strftime('%Y-%m-%d')
    time = time.dt.strftime('%H:%M:%S')

    # Return
    return pd.to_datetime(date + ' ' + time)


def merge_date_time2(data, date_column, time_column=None):
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
    data[time_column] = pd.to_datetime(data[time_column], errors='coerce')
    data[time_column] = data[time_column].fillna(pd.Timestamp('1960-01-01'))

    print(data.dtypes)

    # Format
    date = data[date_column].dt.strftime('%Y-%m-%d')
    time = data[time_column].dt.strftime('%H:%M:%S')

    # Return
    return pd.to_datetime(date + ' ' + time)
