# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.utils.logger import load_logger


# ------------------------------------------
# Methods
# ------------------------------------------
def fix_mdtienhist(df_mdtiendemo, df_mdtienhist):
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
    aux = df_mdtiendemo[['st_no', 'admctd_d']]
    # Include date enrolment information
    df_mdtienhist = df_mdtienhist.merge(aux, how='left', on='st_no')

    # Return
    return df_mdtienhist


def fix_elisaall(df_mdclinical, df_elisaall):
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
    aux = df_mdclinical[['st_no', 'admhtd_d', 'admstu_dt']]

    # Include date enrolment information
    df_elisaall = df_elisaall.merge(aux, how='left', on='st_no')

    # Return
    return df_elisaall


# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with raw data.
path_data = '{0}/resources/datasets/{1}'.format(
    curr_path, 'MD_compendium.xlsx')

# Path to save fixed data.
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, 'md_data_fixed.xlsx')


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
# Fix data sheets
data['MD_Tien_hist'] = fix_mdtienhist(data['MD_Tien_demo'], data['MD_Tien_hist'])
data['MD_Elisa_all'] = fix_elisaall(data['MD_clinical'], data['MD_Elisa_all'])

# Study selection
data['MD_Elisa_sum'] = data['MD_Elisa_sum'][data['MD_Elisa_sum'] \
    .st_code.str.upper().replace(" ", "") == 'MD']
data['MD_Elisa_all'] = data['MD_Elisa_all'][data['MD_Elisa_all'] \
    .st_code.str.upper().replace(" ", "") == 'MD']

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