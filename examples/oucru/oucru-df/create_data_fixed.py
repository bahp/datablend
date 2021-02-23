# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.utils.logger import load_logger


# ------------------------------------------
# Methods
# ------------------------------------------
def fix_elisa14(df_df, df_elisa14):
    """This method fixes the EXAM worksheet

    issue 1: There is no date in EXAM
        It can be addressed including the enrolment date in ENROL.
        It can be addressed including the date in NS1STRIP.
    """
    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_df[['st_no', 'admstu']]
    # Include date enrolment information
    df_elisa14 = df_elisa14.merge(aux, how='left', on='st_no')

    # Return
    return df_elisa14


# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with raw data.
path_data = '{0}/resources/datasets/{1}'.format(
    curr_path, 'DF_compendium.xlsx')

# Path to save fixed data.
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, 'df_data_fixed.xlsx')


# -------------------------------
# Read data
# -------------------------------
# Read all data sheets
data = pd.read_excel(path_data, sheet_name=None)

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
# Fix the various worksheets
data['FINAL_ELISA_14DEC2012_ALL_DATA'] = \
    fix_elisa14(data['DF'], data['FINAL_ELISA_14DEC2012_ALL_DATA'])

# Study selection
data['FINAL_ELISA_14DEC2012_ALL_DATA'] = \
    data['FINAL_ELISA_14DEC2012_ALL_DATA'][data['FINAL_ELISA_14DEC2012_ALL_DATA'] \
        .st_code.str.upper().replace(" ", "") == 'DF']
data['FINAL_ELISA_SUMMARY'] = \
    data['FINAL_ELISA_SUMMARY'][data['FINAL_ELISA_SUMMARY'] \
        .st_code.str.upper().replace(" ", "") == 'DF']

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