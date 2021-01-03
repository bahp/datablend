# Libraries
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# Specific
from datetime import date

# DataBlend libraries
from datablend.utils.compute import age
from datablend.utils.compute import dob
from datablend.utils.compute import add_days  # change name?
from datablend.utils.logger import load_logger

# ------------------------------------------
# Methods
# ------------------------------------------
def fix_enrol(df):
    """This method fixes the ENROL worksheet

     issue 1: Inconsistency with age and dob collection
         It can be addressed by completing both.
     """

    # Issue 1: Inconsistent dob and/or age.
    # -------------------------------------
    # Compute ages and dobs.
    ages = df.apply(lambda x: age(x['DateBirth'], x['DateEnrol']), axis=1)
    dobs = df.apply(lambda x: dob(x['Age'], x['DateEnrol']), axis=1)

    # Fill missing values.
    df['Age'] = df.Age.fillna(ages)
    df['DateBirth'] = df.DateBirth.fillna(dobs)

    # Return
    return df


def fix_daily(df_enrol, df_daily):
    """This method fixes DAILY worksheet

     issue 1: There is no date in daily
         It can be addressed including the enrolment date in ENROL.
         It can be addressed including the date in NS1STRIP.
     """

    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_daily = df_daily.merge(aux, how='left', on='StudyNo')
    # Convert days to timedelta
    df_daily['date_sample'] = \
        add_days(df_daily.DateEnrol, df_daily.StudyDay)

    # Return
    return df_daily


def fix_inpfu(df):
    """This method fixes the INPFU worksheet.

    issue 1: The dates are indicated as the day of study.
        It can be addressed by creating a new column with the
        date the patients were enrolled (therefore study day is 0)
        and then add the corresponding day of study.

    """
    df['date_haematocrit_max'] = add_days(df.DateHosp, df.DayHighestHct)
    df['date_platelets_min'] = add_days(df.DateHosp, df.DayLowestPlt)

    return df


def fix_ns1platelia(df_enrol, df_ns1):
    """This method fixes the NS1PLATELIA worksheet

    issue 1: There is no date in NS1PLATELIA
        It can be addressed including the enrolment date in ENROL.
        It can be addressed including the date in NS1STRIP.
    """
    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_ns1 = df_ns1.merge(aux, how='left', on='StudyNo')

    # Return
    return df_ns1


def fix_pcr(df_enrol, df_pcr):
    """This method fixes the PCR worksheet

    issue 1: There is no date in PCR
        It can be addressed including the enrolment date in ENROL.
        It can be addressed including the sample date in LAB_DIAGNOSIS.

    """
    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_pcr = df_pcr.merge(aux, how='left', on='StudyNo')

    # Return
    return df_pcr


# -------------------------------
# Create configuration from data
# -------------------------------
# Current path
curr_path = pathlib.Path(__file__).parent.absolute()

# Create logger
logger = load_logger('%s/logging.yaml' % curr_path)

# Path with raw data.
path_data = '{0}/resources/datasets/{1}'.format(
    curr_path, '13DX_Data_sharing.xlsx')

# Path to save fixed data.
path_fixed = '{0}/resources/outputs/datasets/{1}'.format(
    curr_path, '13dx_data_fixed.xlsx')


# -------------------------------
# Format data
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

# Fix the various worksheets
data['ENROL'] = fix_enrol(data['ENROL'])
data['DAILY'] = fix_daily(data['ENROL'], data['DAILY'])
data['INPFU'] = fix_inpfu(data['INPFU'])
data['PCR'] = fix_pcr(data['ENROL'], data['PCR'])
data['NS1PLATELIA'] = fix_ns1platelia(data['ENROL'], data['NS1PLATELIA'])

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
logger.info("Output: %s" % path_fixed)
logger.info("=" * 80)