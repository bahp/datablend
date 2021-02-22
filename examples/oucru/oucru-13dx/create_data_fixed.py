# Libraries
import yaml
import logging
import pathlib
import pandas as pd
import logging.config

# Specific
from datetime import date

# DataBlend libraries
from datablend.utils.compute import age_from_dob
from datablend.utils.compute import dob_from_age
from datablend.utils.compute import add_days  # change name?
from datablend.utils.logger import load_logger


# ------------------------------------------
# Methods
# ------------------------------------------
def fix_enrol(df):
    """This method fixes the ENROL worksheet

    issue 1: Inconsistency with age and dob collection
        It can be addressed by completing nan in both.

    Parameters
    ----------
    df: pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    # Issue 1: Inconsistent dob and/or age.
    # -------------------------------------
    # Compute ages
    ages = df.apply(lambda x: \
        age_from_dob(dob=x.DateBirth,
                     date_reference=x.DateEnrol), axis=1)

    # Compute dobs
    dobs = df.apply(lambda x:
        dob_from_age(age=x.Age,
                     date_reference=x.DateEnrol), axis=1)

    # Fill missing values.
    df.Age = df.Age.fillna(ages)
    df.DateBirth = df.DateBirth.fillna(dobs)

    # Return
    return df


def fix_daily(df_enrol, df_daily):
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
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_daily = df_daily.merge(aux, how='left', on='StudyNo')
    # Convert days to timedelta
    #df_daily['date_sample'] = \
    #    add_days(df_daily.DateEnrol, df_daily.StudyDay)

    """
    # Issue 2: Wrong dates of hospitalisation
    # ---------------------------------------
    # Create auxiliary method
    def replace_year(x):
        x.DateHosp = x.DateHosp.replace(year=x.DateEnrol.year)
        return x

    # Convert to dates
    df_daily.DateHosp = pd.to_datetime(df_daily.DateHosp)
    df_daily.DateEnrol = pd.to_datetime(df_daily.DateEnrol)

    # Create mask
    mask1 = ~pd.isnull(df_daily.DateHosp)
    mask2 = df_daily.DateHosp.dt.year < 2010
    mask3 = df_daily.DateHosp.dt.year > 2014
    mask4 = ~df_daily.DateHosp.dt.year.between(2010, 2014)

    df_daily[mask1 & mask4] = \
        df_daily[mask1 & mask4].apply(replace_year, axis=1)
    """

    # Return
    return df_daily


def fix_inpfu(df):
    """This method fixes the INPFU worksheet.

    issue 1: The dates are indicated as the day of study.
        It can be addressed by creating a new column with the
        date the patients were enrolled (therefore study day is 0)
        and then add the corresponding day of study.

    Parameters
    ----------

    Returns
    -------
    """
    # Issue 1: Inconsistent dob and/or age.
    # -------------------------------------
    # Compute ages
    ages = df.apply(lambda x:
        age_from_dob(dob=x.BirthDate,
                     date_reference=x.DateAssess), axis=1)

    # Compute dobs
    dobs = df.apply(lambda x:
        dob_from_age(age=x.Age,
                     date_reference=x.DateAssess), axis=1)

    # Fill missing values.
    df.Age = df.Age.fillna(ages)
    df.BirthDate = df.BirthDate.fillna(dobs)

    # Return
    return df


def fix_ns1platelia(df_enrol, df_ns1):
    """This method fixes the NS1PLATELIA worksheet

    issue 1: There is no date in NS1PLATELIA
        It can be addressed including the enrolment date in ENROL.
        It can be addressed including the date in NS1STRIP.

    Parameters
    ----------

    Returns
    -------
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

    Parameters
    ----------

    Returns
    -------

    """
    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary dataframe
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_pcr = df_pcr.merge(aux, how='left', on='StudyNo')

    # Return
    return df_pcr


def fix_bio(df_enrol, df_bio):
    """This method fixes the BIO worksheet.

    Parameters
    ----------
    df_enrol
    df_bio

    Returns
    -------

    """
    # Issue 1: No date found (sample_date)
    # ------------------------------------
    # Create auxiliary DataFrame
    aux = df_enrol[['StudyNo', 'DateEnrol', 'TimeEnrol']]
    # Include date enrolment information
    df_bio = df_bio.merge(aux, how='left', on='StudyNo')
    # Convert days to timedelta
    #df_daily['date_sample'] = \
    #    add_days(df_daily.DateEnrol, df_daily.StudyDay)

    """
    # Issue 2: Wrong dates of hospitalisation
    # ---------------------------------------
    # Create auxiliary method
    def replace_year(x):
        x.AnalysisDate = x.AnalysisDate.replace(year=x.DateEnrol.year)
        return x

    # Convert to dates
    df_bio.AnalysisDate = pd.to_datetime(df_bio.AnalysisDate)
    df_bio.DateEnrol = pd.to_datetime(df_bio.DateEnrol)

    # Create mask
    mask1 = ~pd.isnull(df_bio.AnalysisDate)
    mask2 = df_bio.AnalysisDate.dt.year < 2010
    mask3 = df_bio.AnalysisDate.dt.year > 2014
    mask4 = ~df_bio.AnalysisDate.dt.year.between(2010, 2014)

    df_bio[mask1 & mask4] = \
        df_bio[mask1 & mask4].apply(replace_year, axis=1)
    """
    # Return
    return df_bio


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
data['BIO'] = fix_bio(data['ENROL'], data['BIO'])

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