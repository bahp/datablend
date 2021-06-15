# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.utils.logger import load_logger


# ------------------------------------------
# Methods
# ------------------------------------------
def fix_hist(df_dm, df_hist):
    """This method fixes the DAILY worksheet

    issue 1: There is no date in all columns in daily
        It can be addressed including the enrolment date in ENROL.
        It can be addressed including the date in NS1STRIP.

    issue 2: The date of hospitalisation are sometimes wrong
        Th main issue is with the year and can be solved using
        the enrol dates.

    Parameters
    ----------

    Returns
    -------
    """

    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary DataFrame
    aux = df_dm[['SUBJID', 'ADMDTC', 'ADMTIME']]
    aux.columns = ['SUBJID', 'ADMDTC_DM', 'ADMTIME_DM']
    # Include date enrolment information
    df_hist = df_hist.merge(aux, how='left', on='SUBJID')
    # Return
    return df_hist

# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with raw data.
path_data = '{0}/resources/datasets/{1}'.format(
    curr_path, '20-1-2021-_01Nva_P1_Data.xlsx')

# Path to save fixed data.
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '01nva_data_fixed.xlsx')


# -------------------------------
# Read data
# -------------------------------
# Read all data sheets
data = pd.read_excel(path_data,
   sheet_name=None, engine='openpyxl')

# Logging information
logger.info("=" * 80)
logger.info("File: %s", path_data)
logger.info("")

# Logging worksheets
for k, v in data.items():
    logger.info("Worksheet %-15s | Rows %5s | Columns %3s",
                k, v.shape[0], v.shape[1])

# -------------------------------
# Fix data sheets
# -------------------------------
data['HIST'] = fix_hist(data['DM'], data['HIST'])

# ---------------------------------
# Save
# ---------------------------------
# Create path if it does not exist
pathlib.Path(path_fixed).parent.mkdir(parents=True, exist_ok=True)

# Creating Excel Writer Object from Pandas
writer = pd.ExcelWriter(path_fixed, engine='xlsxwriter')

# Save each frame
for sheet, frame in data.items():
    frame.to_excel(writer, sheet_name=sheet, index=False)

# critical last step
writer.save()

# Logging output
logger.info("")
logger.info("Output: %s", path_fixed)
logger.info("=" * 80)