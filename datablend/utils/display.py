# Libraries
import numpy as np
import pandas as pd


# ----------------------------------------------
# Helper methods (move?)
# ----------------------------------------------
def categories_report(x):
    """Returns value counts report.

    Parameters
    ----------
    x: pd.Series
        The series with the values

    Returns
    -------
    string
        The value counts report.
        str1 = False      22 | True      20 | nan     34
        str2 = False (22) | True (20) | nan (34)
    """
    # Do counting and sorting
    counts = x.value_counts(dropna=False)
    counts.index = counts.index.map(str)
    counts = counts.sort_index()

    # Create different strings
    str1 = ' | '.join(str(counts).split("\n")[:-1])
    str2 = ' | '.join("%s (%s)" % (i, counts[i]) for i in counts.index)

    # Return
    return str2


def _df_dtypes(data):
    """This method..."""
    return data.convert_dtypes().dtypes.sort_index()


def _df_nan_percentage(data):
    """This method..."""
    return 100 - (data.notna().mean() * 100)


def _df_categories(data, max_nunique=8):
    """This method..."""
    # Select only columns with 5 or less unique values
    aux = data.loc[:, data.nunique() <= max_nunique]
    aux = aux.apply(categories_report)
    aux = aux.T
    return aux


def describe(data, reorder=None, drop=None, mode=None):
    """This method.....

    Parameters
    ----------
    data: pd.DataFrame
        The DataFrame to describe

    reorder: list
        Order of the columns in the describe DataFrame

    drop: list
        Columns to drop from describe

    mode: str
        - verbose

    Returns
    -------
    pd.DataFrame
        The resulting DataFrame
    """
    # ------------------------------------
    # configuration
    # ------------------------------------
    # Reorder columns
    if reorder is None:
        reorder = ['dtypes', '%nan', 'count', 'unique',
            'mean', 'std', 'min', '25%', '50%', '75%',
            'max', 'first', 'last', 'top', 'freq',
            'categories']

    # Drop columns
    if drop is None:
        drop = ['top', 'freq']

    # ------------------------------------
    # Create DataFrame
    # ------------------------------------
    # Create all the information
    aux = data.describe(include='all',
        datetime_is_numeric=True).T
    aux = aux.drop(columns=['count', 'unique'])

    # Create DataFrame
    df = pd.DataFrame()
    df['count'] = data.count()     # Override count
    df['unique'] = data.nunique()  # Override nunique
    df['%nan'] = _df_nan_percentage(data)
    df['categories'] = _df_categories(data)
    df['dtypes'] = _df_dtypes(data)

    # Merge with describe
    df = df.merge(aux, left_index=True, right_index=True)

    # Drop
    df = df.drop(columns=set(drop).intersection(set(df.columns)))

    # Reorder
    reorder = [e for e in reorder if e in df]
    df = df[reorder + list(set(df.columns)-set(reorder))]

    # Convert dtypes
    df = df.convert_dtypes()

    # Return
    return df


def str_dtypes(data, label=None):
    """Returns str with the dtypes"""
    # Create string
    s = "=" * 80
    s += "\nData Source: {0} {1}".format(label, data.shape)
    s += "\nData Types:"
    s += "\n\t{0}\n".format(data.convert_dtypes()
                           .dtypes.sort_index()
                           .to_string().replace('\n', '\n\t'))
    s += "=" * 80
    # Return
    return s


def str_description(data, label=None):
    """Returns str with the description"""

    # ------------------------------------
    # Configuration
    # ------------------------------------
    # Set display pandas format.
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    # Create DataFrame
    df = describe(data)

    df.to_csv('test2.csv')

    # ------------------------------------
    # Create string representation
    # ------------------------------------
    s = "=" * 80
    s += "\nData Source: {0} {1}".format(label, data.shape)
    s += "\nData Description:"
    s += "\n\t{0}\n".format(df.to_string().replace('\n', '\n\t'))
    s += "=" * 80

    # Return
    return s