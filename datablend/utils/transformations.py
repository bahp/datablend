# Library
import re
import ast
import pandas as pd


def str2eval(x):
    if not pd.isnull(x):
        return ast.literal_eval(x)


def convert_dtypes_datetime(data):
    """This method converts columns to datetime.

    It converts to datetime64[ns] those columns containing
    the substring 'date' in the column name and has an
    string dtype (dtype == 'string').

    Parameters
    ----------
    data: pd.DataFrame
        The pandas dataframe.

    Returns
    -------
    """
    # Copy dta
    aux = data.copy(deep=True)

    # Fill DateTime information
    for c in aux.columns:
        if str(aux[c].dtype) != 'string':
            continue
        if 'date' in str(c).lower():
            aux[c] = pd.to_datetime(aux[c])

    # Return
    return aux


def convert_dtypes_categorical(data, nunique_threshold=5):
    """This method converts columns to categorical.

    It converts to categorical those columns that are not
    datetime64[ns] or boolean and have a small number of
    unique values (lower than the nunique_threshold).

    .. note: strings and ints can be categorical.
    .. note: floats are not likely to e categorical.

    Parameters
    ----------
    data: pd.DataFrame
        The pandas dataframe.

    nunique_threshold: int
        The maximum number of unique values to be considered
        of a column to be considered a categorical feature.

    Returns
    -------

    """
    # Copy dta
    aux = data.copy(deep=True)

    # Fill categorical information
    for c in aux.columns:
        if str(aux[c].dtype) in ['datetime64[ns]', 'boolean']:
            continue
        if aux[c].nunique() > nunique_threshold:
            continue
        aux[c] = pd.Categorical(aux[c])

    # Return
    return aux


def format_var_names(x):
    """This method formats an string into a variable name.

    It inserts an underscore before any number of consecutive
    uppercase letters not including uppercase at the beginning
    or end of the string.

    .. todo: TRIM!
    .. todo: Replace spaces with _


    .. todo: BirthDate_M --> birthdate_m instead of birthdate__m
    .. todo: SBP         --> sbp         instead of s_bp
    .. todo: ValueSBP    --> value_sbp   instead of
    .. todo: LungChestOutcome --> lung_chest_outcome instead of lung_chestoutcome

    RegExp1: r"(w)([A-Z]+[a-z]*)" (missing backslash before w)
    RegExp2: r"([a-z]+)([A-Z]+[a-z]*)"

    Parameters
    ----------
    x: str
        The string to format
    """
    x = re.sub(r"([a-z]+)([A-Z]+[a-z]*)", r"\1_\2", x)
    x = x.lower()
    return x
