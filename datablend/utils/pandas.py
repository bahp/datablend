# Libraries
import pandas as pd

# Specific
from pathlib import Path


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