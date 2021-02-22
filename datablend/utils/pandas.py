# Libraries
import copy
import numpy as np
import pandas as pd

# Specific
from scipy import stats

# Specific
from pathlib import Path


# -----------------------------------------------------
#
# -----------------------------------------------------
def nanunique(x):
    if x.isnull().all():
        return []
    return x.dropna().unique().tolist()


def fbfill(x):
    """Computes forward and then backward fill."""
    return x.ffill().bfill()


def bffill(x):
    """Computes backward and then forward fill"""
    return x.bfill(x).ffill(x)

#def mode(series):
#    return series.mode()[0]

def mode(x):
    """Compute the mode and returns as a valid transform.

    .. note: The pd.Series mode function automatically
             removes the NaNs. Hence, if the series has
             all NaN values there wont be a mode and it
             will crash.

    .. note: An alternative use x.mode(dropna=True).
    .. note: stats.mode(x).mode[0

    """
    if x.isnull().all():
        return x
    return np.repeat(stats.mode(x).mode[0], len(x))


TRANSFORMATIONS = {
    'mode': mode,
    'fbfill': fbfill,
    'bffill': bffill
}


def str2func(d):
    """This method passes strings to functions

    Parameters
    ---------
    d: dict
        Dictionary where value is a function name."""
    # Create deep dictionary copy
    aux = copy.deepcopy(d)

    # Format some function names
    for k, v in aux.items():
        if v in TRANSFORMATIONS.keys():
            aux[k] = TRANSFORMATIONS[v]

    # Return
    return aux


# -----------------------------------------------------
#
# -----------------------------------------------------
def _save_dict_df_csv(d, filepath, filename, **kwargs):
    """

    Parameters
    ----------
    d
    filepath
    filename

    Returns
    -------

    """
    for k, df in d.items():
        # Create path
        path = "{0}/{1}_{2}.csv".format(filepath, filename, k)
        # Save DataFrame
        df.to_csv(path, **kwargs)


def _save_dict_df_xlsx(d, filepath, filename, **kwargs):
    """Save dictionary in xlsx file.

    Parameters
    ----------

    Returns
    -------
    """
    # Create full path
    fullpath = "{0}/{1}.xlsx".format(filepath, filename)

    # Creating Excel Writer Object from Pandas
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')

    # Save each frame
    for sheet, frame in d.items():
        frame.to_excel(writer, sheet_name=sheet, **kwargs)

    # critical last step
    writer.save()


def save_df_dict(d, filepath, filename, extension='xlsx',
                 flat=False, **kwargs):
    """This method saves a dictionary of DataFrames

    Parameters
    ----------
    d: dict-like
       The dictionary where key is the name of the worksheet
       and the value is the pandas DataFrame.

    filepath: str-like
        The path to store the output files.

    filename: str-like
        The name to use for the output files without the extension.

    ext: str-like (xlsx or csv)
        The extension

    flat: boolean
        To concatenate all DataFrames to save them together.

    Returns
    -------
    """
    # Check is dictionary
    if not isinstance(d, dict):
        d = {'': d}

    # Concatenate DataFrames
    # ----------------------
    if flat:
        # Create full name
        fullpath = "{0}/{1}.{2}".format(filepath, filename, extension)
        # Flat the DataFrames
        flat = pd.concat(d.values(), ignore_index=True)
        # Save
        if extension == 'csv':
            return flat.to_csv(fullpath, **kwargs)
        if extension == 'xlsx':
            return flat.to_excel(fullpath, **kwargs)
        # Return
        return

    # Split worksheets
    # ----------------
    # Save all dfs in same xlsx file
    if extension == 'xlsx':
        return _save_dict_df_xlsx(d, filepath, filename)

    # Save each df in a different csv file
    if extension == 'csv':
        return _save_dict_df_csv(d, filepath, filename, **kwargs)









def save_xlsx(d, filepath, sheet_split=False, **kwargs):
    """This method saves a dictionary in .xlsx

    Parameters
    ----------
    d: dict-like
        The dictionary where key is the name of the worksheet
        and value is the pandas DataFrame.

    filepath: str-like

    sheet_split: boolean

    Returns
    -------
    """
    # Check is dictionary
    if not isinstance(d, dict):
        d = {'': d}

    # Save independent worksheets
    if sheet_split:
        # Create path
        path = Path(filepath)
        # Loop keys
        for k, df in d.items():
            df.to_csv(str(path).replace('.xlsx', '_{0}.csv'.format(k)))
        # Return
        return None

    # Creating Excel Writer Object from Pandas
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    # Save each frame
    for sheet, frame in d.items():
        frame.to_excel(writer, sheet_name=sheet, index=False)

    # critical last step
    writer.save()