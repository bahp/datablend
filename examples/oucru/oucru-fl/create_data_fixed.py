# Libraries
import pathlib
import pandas as pd

# DataBlend libraries
from datablend.utils.logger import load_logger


# ------------------------------------------
# Methods
# ------------------------------------------
def fix_diagnostic(df_sum, df_diagnostic):
    """This method fixes the EXAM worksheet

     issue 1: There is no examination day.
         It can be addressed by completing both. In this case
         assuming that examination day is the admission date.

     Parameters
     ----------
     df_demo: pd.DataFrame
        Demographics sheet.

     df_exam: pd.DataFrame
        Examination sheet.
     """

    # Issue 1: No date found (date_examination)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_sum[['Number', 'Enrolment day']]
    # Include date enrolment information
    df_diagnostic = df_diagnostic.merge(aux, how='left',
                                             left_on='StudyNo',
                                             right_on='Number')
    # Return
    return df_diagnostic


def fix_exam(df_sum, df_exam):
    """This method fixes the EXAM worksheet

     issue 1: There is no examination day.
         It can be addressed by completing both. In this case
         assuming that examination day is the admission date.

     Parameters
     ----------
     df_demo: pd.DataFrame
        Demographics sheet.

     df_exam: pd.DataFrame
        Examination sheet.
     """

    # Issue 1: No date found (date_examination)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_sum[['Number', 'Enrolment day']]
    # Include date enrolment information
    df_exam = df_exam.merge(aux, how='left',
                                 left_on='StudyNo',
                                 right_on='Number')
    # Return
    return df_exam

# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with raw data.
path_data = '{0}/resources/datasets/{1}'.format(
    curr_path, 'FL_compendium.xlsx')

# Path to save fixed data.
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, 'fl_data_fixed.xlsx')


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
data['FL_DIAGNOSTIC'] = fix_diagnostic(data['FL_CLINICAL_SUM'], data['FL_DIAGNOSTIC'])
data['FL_EXAM'] = fix_diagnostic(data['FL_CLINICAL_SUM'], data['FL_EXAM'])

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