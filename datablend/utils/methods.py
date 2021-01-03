# Libraries
import json
import numpy as np
import pandas as pd


def load_features_map(filepath):
    """This method loads the features map json file.

    Parameters
    ----------

    Return
    ------
    """
    # Reading the json as a dict
    with open(filepath) as json_data:
        data = json.load(json_data)

    # Read file
    config = pd.DataFrame(data)

    # Basic formatting
    config.name = config.name.str.title()
    config.code = config.code.str.upper()

    # Return
    return config


def load_columns_operations(filepath):
    """This method..."""
    pass


def merge_date_time(data, date_column, time_column=None):
    """This method merges columns date and time

    .. note: If time is missing default is 00:00.
    .. note: Also convert date using dt.apply(str).

    Parameters
    ----------

    Returns
    -------

    """
    if not date_column in data:
        print("Column <%s> not found!" % date_column)

    if not time_column in data:
        print("Column <%s> not found!" % time_column)

    # Fill empty times with default value
    data[time_column] = data[time_column].fillna('00:00')

    # Format
    date = data[date_column].dt.strftime('%Y-%m-%d')
    time = data[time_column]

    # Return
    return pd.to_datetime(date + ' ' + time)


def display(data, name):
    """This method..."""
    print("Name: %s" % name)
    print(data.dtypes)
    if 'code' in data:
        print("Codes: %s\n" % data['code'].unique())
    elif 'column' in data:
        print("Columns: %s\n" % data['column'].unique())
    print(data)
    print("\n\n")


def extract_stacked(dataframe, index, keep=None, source=None,
                    name_column='column',
                    name_result='result'):
    """This method to extract stacked information from the dataframe.

    Example:

    The dataframe parameter:
        date patient  bt   hr  rr
         d1    p1    35.5  67  18
         d2    p1     -    -    -
         d1    p2     -    -    -

    The index parameter: ['date', 'patient']
    The keep parameter:  ['bt', 'hr', 'rr']

    The output:
        date  patient column result
         d1      p1      bt    35.5
         d1      p1      hr     67
         d1      p1      rr     18
         d2      p1      bt     -

    Parameters
    ----------
    dataframe: pd.DataFrame
        The dataframe with the data

    index: list
        List of column names that will be set as index.

    keep: list
        List of column names that will be stacked. The name
        of the column will be in the column named 'column'
        and the corresponding value in the column named
        'result'.

    source:

    name_column:

    name_result:

    Returns
    -------
    The stacked dataframe
    """

    # Check inputs
    if keep is None:
        keep = set(dataframe.columns)

    # Format inputs
    index = list(index)
    keep = list(set(keep) - set(index))

    # Format to stack dataset
    df = dataframe.copy(deep=True)
    df = df[index + keep]
    df = df.set_index(index)
    df = df.stack()
    df = df.reset_index()
    df.columns = index + [name_column, name_result]

    # Add source
    if source is not None:
        df['source'] = source

    # Return
    return df


# -----------------------------------
# Methods
# -----------------------------------
def extract_events(dataframe, index, keep):
    """This method...."""
    # Format the inputs
    index = list(index)
    keep = list(keep)

    # Remove those in index
    print(index)
    print(keep)

    # Format to stack dataset
    df = dataframe.copy(deep=True)
    df = df[index + keep]
    df = df.set_index(index)
    df = df.stack()
    df = df.reset_index()
    df.columns = index + ['column', 'date']
    df['result'] = 1.0
    df.column = df.column.apply(lambda x: '_'.join(x.split("_")[1:]))  # do it better with replace
    df['source'] = '32dx_evo'

    # Return
    return df


def stacked_display(dataframe, title='', top=10):
    """This method displays the dataframes.

    Parameters
    ---------
    datafame:

    title:

    top:

    Returns
    --------
    """
    # Display
    print("\n\n%s" % title)
    print("=" * 80)
    print("Column counts:")
    print("-" * 30)
    if 'column' in dataframe:
        print(dataframe.column.value_counts().sort_index())
    print("\nResult counts:")
    print("-" * 30)
    #if 'result' in dataframe:
    #    print(dataframe.result.value_counts().sort_index())
    print("\nDataFrame:")
    print("-" * 50)
    print(dataframe.head(top))


def extract_records_from_tuples(dataframe, index, tuples,
          bool2int=False, verbose=0, return_by_types=True):
    """This method extracts the events from tuples.

    This approach is used when there are specific columns for
    the different symptoms indicating the status (true or false),
    the date it started and/or the level.

    The input is an array of tuples containing (date, status, level) where
    status indicates the column with the status (True or False),
    date indicates the column with the dates (datetime64[ns]) and
    level indicates the column with the acuity (number).

    =============== ====== =========== ======== ============= ==============
    date_enrollment chills chills_date headache headache_date headache_level
    =============== ====== =========== ======== ============= ==============
         10-10-2020      1   9-10-2020        1     8-10-2020              3
          5-10-2020      1   1-10-2020        1     8-10-2020              1
          1-10-2020      0           -        1     8-10-2020              1
         12-10-2020      1   7-10-2020        1     8-10-2020              2
    =============== ====== =========== ======== ============= ==============

    Returns
    -------
    dict
        The result
    """
    # Check inputs
    if isinstance(index, str):
        index = [index]

    # What if tuples is None

    # Output
    stacked_by_dtype = {}

    # Loop over all the tuples
    for date, result in tuples:
        # Both status and level are None
        if date is None or result is None:
            print("Tuple (%s, %s) has a None." % (date, result))
            continue

        # Get stacked DataFrame
        aux = extract_stacked(dataframe,
            index=index + [date], keep=[result])
        aux = aux[aux[date].notna()]
        aux = aux.rename(columns={date: 'date'})

        # Convert booleans to int (0 or 1)
        #if bool2int:
        #    print(result, dataframe[result].dtype.name == 'boolean')
        #   if dataframe[result].dtype.name == 'boolean':
        #        aux.result = pd.to_numeric(aux.result)

        #aux = aux.convert_dtypes()

        # .. note: String could be string or class.

        # Add to dictionary
        key = str(aux.result.dtype)
        if not key in stacked_by_dtype:
            stacked_by_dtype[key] = []
        stacked_by_dtype[key].append(aux)


        """
        # Display
        if verbose > 0:
            stacked_display(aux, status.title())
        """

    # Concatenate
    for k,v in stacked_by_dtype.items():
        stacked_by_dtype[k] = \
            pd.concat(v).reset_index(drop=True)

    # Return stacked grouped by types
    if return_by_types:
        return stacked_by_dtype

    """
    .. warning: The order of the concatenation matters. If we start with
                concatenating ints and then bools, the boolean will be
                converted to 0 or 1. To solve this issue...
                
                1. Quick fix: start with booleans... 
                   Will this generate an issue converting ints with only
                   0s or 1s to boolean?
                   
                2. Good fix: keep the types from original data.
                   Do as types with the types...
                
                3. Other fix: Create object dataframe before concatenating?
                
                ['float64', 'int64', 'bool', 'object'])
    """
    # Careful if no datetime column ccfg aux will not exist.
    # Merge all no matter their types
    result = pd.DataFrame(columns=aux.columns, dtype=object)
    for k in sorted(stacked_by_dtype.keys()):  # Quick fix
        result = result.append(stacked_by_dtype[k])

    # Return
    return result
