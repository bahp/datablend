"""


"""
# Libraries
import numpy as np
import pandas as pd

# Pint libraries
from pint.errors import UndefinedUnitError

# DataBlend libraries
from datablend.core.settings import textwrapper
from datablend.core.settings import ureg
from datablend.utils.pandas import nanunique
from datablend.utils.pandas_schema import schema_from_json

# -------------------
# Constants
# -------------------
TICK = u'\u2713'


def str_df(df):
    """"""
    return "\t{0}".format(df.to_string().replace('\n', '\n\t'))


# --------------------------------------------------
# Generic
# --------------------------------------------------
def report_undefined_units(units, unit_registry):
    """Checks that units exist in Pint UnitRegistry.

    Parameters
    ----------
    units: list
        The list of units to check.
    unit_registry: UnitRegistry (pint library)
        The UnitRegistry with all the units defined.

    Returns
    -------
    DataFrame

    Examples
    --------
    ============= ==================
    unit	      status
    ============= ==================
    IU	          UndefinedUnitError
    U/L	          ✓
    beat/minute	  ✓
    breath/minute ✓
    celsius	      ✓
    cm	          ✓
    ============= ==================
    """
    # Create list
    status = []

    # Loop
    for unit in units:
        try:
            unit_registry(str(unit))
            status.append([str(unit), TICK])
        except UndefinedUnitError as ue:
            status.append([str(unit), ue.__class__.__name__])
        except Exception as e:
            status.append([str(unit), e])

    # Create DataFrame
    status = pd.DataFrame(status, columns=['unit', 'status'])
    status = status.set_index('unit').sort_index()

    # Return
    return status


# --------------------------------------------------
# Stacked
# --------------------------------------------------
def report_stack_units_per_dataset(data):
    """This method....

    Examples
    --------
    ======= ====== ======
    column  06dx   13dx
    ======= ====== ======
    weight  kg     kg
    height  cm     m
    age     year   year
    albumin U/L    g/L
    ======= ====== ======
    """
    # Get only those where units are specified
    units = data[data.unit.notna()]
    units = units[['column', 'unit', 'dsource']]
    units = units.drop_duplicates()

    # Pivot table
    units = pd.pivot_table(units, index=['column'],
        columns=['dsource'], values=['unit'],
        aggfunc=','.join)

    # Return
    return units


def report_stack_duplicated_units(stack, keep='errors'):
    """Checks that units exist in Pint UnitRegistry.

    Parameters
    ----------
    units: list
        The list of units to check.
    unit_registry: UnitRegistry (pint library)
        The UnitRegistry with all the units defined.

    Returns
    -------
    """
    if 'column' not in stack:
        pass
    if 'unit' not in stack:
        pass

    # Create DataFrame with counts
    duplicates = pd.crosstab(stack.column, stack.unit)
    duplicates['n_units'] = (duplicates > 0).astype(int).sum(axis=1)
    #duplicates['status'] = duplicates['#units'].replace({1: TICK})

    # Keep only inconsistent
    if keep == 'errors':
        duplicates = duplicates[duplicates.n_units > 1]
        duplicates = \
            duplicates.loc[:, (duplicates != 0).any(axis=0)]

    # Return
    return duplicates


def report_stack_feature_count(stack, cpid='StudyNo'):
    """DataFrame with number of samples of each feature.

    .. warning: Assumes the column 'column' exists.

    Example
    -------
    ======== === === ===
    patient  alb alt wbc
    ======== === === ===
    patient1   1   1   2
    patient2   2  NA   1
    ======== === === ===

    """
    return stack.groupby(by=cpid) \
         .column.value_counts()\
         .to_frame('vcount') \
         .unstack()


def report_stack_date_count(stack, cpid='StudyNo'):
    """DataFrame with number of samples of each date.

    .. warning: Assumes the column 'date' exists.

    Example
    -------
    ======== ===== =====
    patient  date  count
    ======== ===== =====
    patient1 date1     1
    patient1 date2     5
    patient1 date3     2
    patient2 date1    10
    ======== ===== =====
    """
    return stack.groupby(by=cpid) \
        .date.value_counts() \
        .to_frame('vcount') \
        .sort_values(by=[cpid, 'date'])


def report_stack_stay(stack, cpid='StudyNo'):
    """DataFrame with summary of patient stay.

    .. warning: Assumes the column 'date' exists.

    .. note: features=('column', 'unique')
             units=('unit', enumerate)

    Example
    -------
              dmin  dmax  dmedian stay nrecords nfeatures
    patient1
    patient2
    """
    def stay(x):
        return (x.max() - x.min()).days

    def median(x):
        return x.median()

    def enumerate(x):
        c = x.value_counts()
        return list(zip(c, c.index))

    df = stack.groupby(by=cpid).agg(
        dmin=('date', 'min'),
        dmax=('date', 'max'),
        dmedian=('date', median),
        stay=('date', stay),
        nrecords=('date', 'count'),
        nfeatures=('column', 'nunique')).reset_index()

    # Format
    df.dmin = df.dmin.dt.date
    df.dmax = df.dmax.dt.date

    df = df.set_index(cpid)

    return df


def report_stack_patients(stack, cpid='StudyNo'):
    """This method..."""
    vcount_f = \
        report_stack_feature_count(stack, cpid)
    vcount_d = \
        report_stack_date_count(stack, cpid)
    summary = \
        report_stack_stay(stack, cpid)
    return summary, vcount_f, vcount_d


def report_stack_corrections(original, corrected, cpid='StudyNo'):
    """This method...."""
    # Create summary
    summary = report_stack_stay(original)
    # Create comparison
    compare = original.compare(corrected)
    compare = compare.merge(corrected, \
        left_index=True, right_index=True)
    compare = compare.merge(summary, on=cpid)
    # Return
    return compare


# --------------------------------------------------
# Tidy
# --------------------------------------------------
def report_tidy_feature_count_per_dataset(data):
    """This method...

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    ======== ==== ==== ====
    feature  06dx 13dx 32dx
    ======== ==== ==== ====
    feature1   12   33   45
    feature2        44  300
    feature3   35  150
    ======== ==== ==== ====

    """
    # Count not nan for each dataset.
    count = data.groupby(by=['dsource']) \
        .agg(['count']) \
        .transpose() \
        .unstack() \
        .sort_index()

    # Count number of null values per row.
    count['n_sets'] = count[count > 0].count(axis=1)

    # Return
    return count


def report_tidy_dtypes_per_dataset(data):
    """

    Parameters
    ----------
    data

    Returns
    -------

    Examples
    --------
    ======== ==== ==== ====
    feature  06dx 13dx 32dx
    ======== ==== ==== ====
    feature1   22   33
    feature2   30  350 3000
    feature3   20
    ======== ==== ==== ====

    """
    # Initialise
    dtypes = pd.DataFrame()

    # Loop filling dtypes
    for k, df in data.groupby(by=['dsource']):
        series = df.dropna(axis=1, how='all') \
            .convert_dtypes().dtypes
        series.name = k
        dtypes = dtypes.merge(series, how='outer',
                              left_index=True, right_index=True)

    # Count number of null values per row.
    dtypes['n_sets'] = dtypes.count(axis=1)

    # Return
    return dtypes


def report_tidy_corrections(original, corrected, verbose=10):
    """This method reports a comparison of dataframes.

    .. note: There is an important difference between null values
             expressed as np.nan or pd.NA that affects the comparison
             to identify values within the columns that have been
             corrected. The main problem is hat pd.NA does not show
             those original values that were set to pd.NA.
                 - np.nan == 1 => False => good behaviour
                 - pd.NA == 1 => pd.NA => bad behaviour

    Parameters
    ----------
    original: pd.DataFrame
        The DataFrame with the original data.
    corrected: pd.DataFrame
        The DataFrame with the corrected data.
    verbose: int
        Level of verbosity.

    Returns
    ------
        String
    """
    # Set n according to verbose
    n = 10 if verbose == 1 else 1e5

    # Create report
    msg = "Report comparison tidy formats:\n"
    msg += "=" * 80 + "\n"

    # Loop
    for c in corrected.columns:
        # Newly created column (ignore)
        if c not in original:
            continue

        # Compare
        comparison = original[c].compare(corrected[c])
        comparison.columns = ['original', ' corrected']

        # Create report
        msg += "   -<{0}> had <{1}> inconsistent values\n" \
            .format(c, comparison.shape[0])
        if comparison.shape[0] and comparison.shape[0] < n:
            msg += "\n\n\tThe complete report:"
            msg += "\n\t\t{0}\n".format(comparison
                .to_string().replace('\n', '\n\t\t'))

    # Return report
    return msg


class ValidationReport:
    """This class contains the validation report"""

    # List of tuples containing the level of verbosity
    # and the message to display.
    messages = []

    def __init__(self):
        """Constructor"""
        self.messages = []

    def add(self, verbosity, message):
        """This method...."""
        self.messages.append((verbosity, message))

    def report(self, verbose):
        """This method...."""
        # Create empty message
        msg = ""

        # Loop
        for verbosity, message in self.messages:

            # Skip higher levels of verbosity
            if verbosity > verbose:
                continue
            # Create message
            if isinstance(message, str):
                msg += message
            if isinstance(message, pd.DataFrame):
                msg += "\n\n\tThe complete report:"
                msg += "\n\t\t{0}\n".format( \
                    message.to_string().replace('\n', '\n\t\t'))

        # Add separator
        msg = "\n{0}\n{1}\n{2}\n".format("=" * 80, msg, "=" * 80)

        # Return
        return msg

    def __str__(self):
        return self.report(verbose=1)

def stack_validate(stack, unit_registry, schema_json):
    """This methods validates the stack DataFrame.

    Parameters
    ----------
    stack: pd.DataFrame
        The stacked DataFrame which must have the following columns:
            StudyNo - id of the patient
            date - date in which data was collected
            column - the feature that was collected
            unit - the unit of such feature.

    unit_registry: UnitRegistry (pint library)
        The UnitRegistry with all the units defined.

    Returns
    -------

    """
    # Check required columns

    # Check that all the units are in the registry
    check1, report1 = has_undefined_units( \
        units=stack.unit.dropna().unique(),
        unit_registry=unit_registry)

    # Check that features have one single unit
    check2, report2 = has_duplicated_units_per_column(stack)

    # Check that schema is valid (range, dtype, ...)
    check3, report3 = schema_validate(stack, schema_json)

    # Overall
    checks = [check1, check2, check3]
    reports = [report1, report2, report3]

    # Return
    return all(checks), checks, reports


def has_undefined_units(units, unit_registry):
    """Checks that units exist in Pint UnitRegistry.

    Parameters
    ----------
    units: list
        The list of units to check.
    unit_registry: UnitRegistry (pint library)
        The UnitRegistry with all the units defined.

    Returns
    -------
    """
    # Create list
    status = []

    # Loop
    for unit in units:
        try:
            unit_registry(str(unit))
            status.append([str(unit), TICK])
        except UndefinedUnitError as ue:
            status.append([str(unit), ue.__class__.__name__])
        except Exception as e:
            status.append([str(unit), e])

    # Create DataFrame
    status = pd.DataFrame(status, columns=['unit', 'status'])

    # Create report
    report = ValidationReport()
    report.add(1, "Unsupported units")
    report.add(1, status)

    # Return
    return any(status.status != TICK), report


def has_duplicated_units_per_column(stack):
    """Check whether a feature has several units.

    Parameters
    ----------

    Returns
    -------
    """
    if 'column' not in stack:
        pass
    if 'unit' not in stack:
        pass

    # Create DataFrame with counts
    duplicates = pd.crosstab(stack.column, stack.unit)
    duplicates['#units'] = (duplicates > 0).astype(int).sum(axis=1)
    duplicates['status'] = duplicates['#units'].replace({1: TICK})

    # Create report
    report = ValidationReport()
    report.add(1, "Columns with more than one unit")
    report.add(1, duplicates)

    # Return
    return any(duplicates['#units'] > 1), report


def schema_validate(stack, schema_json):
    """Check that the schema is valid.

    .. warning: TidyWidget index is hardcoded!

    Parameters
    ----------
    stack: pd.DataFrame
        The stacked data.
    schema_json: json
        Full description

    Returns
    -------
    """
    # Import library
    from datablend.core.widgets.tidy import TidyWidget

    # Check if stack index has duplicates...
    # Should this be done outside in case our
    # reports might be useful in a way probably not.
    # Ensure that no index is repeated in stack
    stack = stack.reset_index()

    # Create schema
    schema = schema_from_json(schema_json)

    # Common columns
    cols_schema = set([c.name for c in schema.columns])
    cols_stack = set(stack.column.dropna().unique())
    columns = cols_schema.intersection(cols_stack)

    # Create report
    report = ValidationReport()
    report.add(1, "Processing schema validation...")

    # Loop
    for c in columns:
        aux = stack[stack.column.isin([c])].rename(columns={'result': c})

        # Validate schema
        errors = schema.validate(aux, columns=[c])

        # Complete report
        if len(errors):
            report.add(1, "\nTotal errors found in <{0}>: {1}".format(c, len(errors)))
            # for e in errors:
            #    print(e)
            report.add(2, stack.iloc[[error.row for error in errors]])

    # Return
    return True, report


def report_unique_value(data, groupby, verbose=10):
    """Check whether columns have more than one unique value.

    .. todo: probably counting and unique can be done more efficiently.

    Parameters
    ----------
    data: pd.DataFrame
        The DataFrame with the columns to investigate.
    groupby: mapping, function, label, or list of labels
        Used to determine the groups for the groupby.
    verbose: int
        The higher the more detailed the report is.

    Returns
    -------
    """
    # Create report
    msg = ""

    # Count the number of unique values
    unique = data.groupby(by=groupby).nunique()

    # Find those columns with more than one unique value
    warn = unique.columns[(unique > 1).any(axis=0)].tolist()

    if warn:
        # Raise simple warning
        txt = "The following columns have more than one unique" \
              "value. Please ensure that these columns are meant to" \
              "be constant; that is, same value over the data. Otherwise," \
              "there could be an inconsistent behaviour: {0}".format(warn)
        msg += "{0}\n\n".format(textwrapper.fill(txt))

        if verbose > 1:

            for column in warn:
                # Create inconsistency DataFrame
                aux = data.groupby(by=groupby)[column] \
                    .agg([nanunique, 'nunique'])
                aux = aux[aux['nunique'] > 1]

                if verbose > 1:
                    msg += "  -<{0}> has {1} inconsistencies.\n" \
                        .format(column, aux.shape[0])

                if verbose > 5:
                    msg += "\n\t\t{0}\n\n".format(aux.to_string().replace('\n', '\n\t\t'))

    # Return
    return msg + '\n'


def consistency_bleeding(tidy, verbose=10):
    """Check the consistency of the bleeding parameters.

    Ensure that there is consistency between the bleeding columns. In
    particular, check that if bleeding (overall) is True then at least
    one of the bleeding categories has to be true. Otherwise, set
    bleeding other to True.

    rule: if bleeding==1 then any(bleeding categories)==1

    .. note: It adds by default a bleeding other category with all
             values to false. If at least one value is true leave it
             otherwise drop column.

    .. warning: Note that we assume that if bleeding is not indicated
                then there was no bleeding. However, it might be also
                possible to forward fill the existing value for each
                individual patient.

    """
    # Add bleeding other
    if not 'bleeding_other' in tidy:
        tidy['bleeding_other'] = False

    # Bleeding can be defined as:
    bleeding = tidy.bleeding_gi | \
               tidy.bleeding_gum | \
               tidy.bleeding_mucosal | \
               tidy.bleeding_nose | \
               tidy.bleeding_skin | \
               tidy.bleeding_urine | \
               tidy.bleeding_vaginal | \
               tidy.bleeding_vensite | \
               tidy.bleeding_other

    # Bleeding not recorded is assumed false
    # tidy.bleeding = tidy.groupby(by='StudyNo').bleeding.ffill()
    tidy.bleeding = tidy.bleeding.fillna(False)

    # Record number of inconsistencies
    idxs = bleeding != tidy.bleeding

    # --------
    # Report
    # --------
    msg = ""

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)
        msg += 'Evaluating bleeding...\n\n'
        msg += '  -<bleeding> has {0} inconsistent values\n'.format(idxs.sum())

    if verbose > 5:
        if np.sum(idxs):
            # Bleeding Comparison
            bldcmp = tidy[['StudyNo', 'date']].copy(deep=True)
            bldcmp['computed'] = bleeding
            bldcmp['recorded'] = tidy.bleeding

            # Inconsistency indexes
            idxs = bldcmp.computed != bldcmp.recorded

            msg += '\nThe \'consistency_bleeding\' report:\n\n'
            msg += '\t\t%s\n' % bldcmp[idxs].sort_index() \
                .to_string() \
                .replace('\n', '\n\t\t')

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)

    # Fix inconsistencies
    tidy.loc[tidy.bleeding & ~bleeding, 'bleeding_other'] = True
    tidy.loc[~tidy.bleeding & bleeding, 'bleeding'] = True

    """
    # Show information
    print("Inconsistencies <bleeding>... {0} corrected!\n"
          .format(np.sum(idxs)))
    if verbose > 10:
        print("\n" + "=" * 80)
        # Bleeding Comparison
        bldcmp = tidy[['StudyNo', 'date']].copy(deep=True)
        bldcmp['computed'] = bleeding
        bldcmp['recorded'] = tidy.bleeding

        # Inconsistency indexes
        idxs = bldcmp.computed != bldcmp.recorded

        # Show
        print("\n\n\t{0}\n".format(bldcmp[idxs].sort_index()
                           .to_string()
                           .replace('\n', '\n\t')))
        print("=" * 80)
    """

    # Return
    return tidy, msg


def consistency_shock(tidy, verbose=10):
    """Check the consistency of the shock parameters.

    Ensure that there is consistency between the shock columns. In
    particular, check that if shock_multiple == 1 then the column
    shock == 1

    rule = if shock_multiple==1 then shock==1
    """
    # c
    columns = ['StudyNo', 'shock', 'shock_multiple']

    # Get idxs
    idxs = (tidy.shock != tidy.shock_multiple) & tidy.shock_multiple

    # Create msg
    msg = ""

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)
        msg += 'Evaluating Shock...\n\n'
        msg += '  -<shock> has {0} inconsistent values\n'.format(idxs.sum())

    if verbose > 5:
        if np.sum(idxs):
            msg += '\nThe \'consistency_shock\' report:\n\n'
            msg += '\t\t%s\n' % tidy.loc[idxs, columns] \
                .sort_index().to_string() \
                .replace('\n', '\n\t\t')

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)

    # Fix inconsistencies
    tidy.loc[idxs, 'shock'] = 1

    # Return
    return tidy, msg


def consistency_events(tidy, verbose=10):
    """Check the consistency of the events.

    Ensure that an event has only one True value.

    rule: np.sum(event) <= 1

    .. note: It depends on the events. Some events such as
             event_admission or event_enrolment should have
             only one value. However, other events such as
             event_pcr or event_lab might have more.
    """
    # Events to consider
    events = ['event_admission',
              'event_discharge',
              'event_enrolment',
              'event_onset',
              'event_shock']

    events = [e for e in events if e in tidy]

    # Count number of events per patient.
    aux = tidy[['StudyNo'] + events].groupby('StudyNo').sum()

    # Filter to keep those with issues
    aux = aux[(aux > 1).any(1)]

    # Create msg
    msg = ""

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)
        msg += 'Evaluating Events...\n\n'
        for e in events:
            msg += '  -<{0}> has {1} inconsistent values.\n'.format(e, (aux[e] > 1).sum())

    if verbose > 5:
        msg += '\nThe \'consistency_shock\' report:\n\n'
        msg += '\t\t%s\n' % aux.sort_index() \
            .to_string() \
            .replace('\n', '\n\t\t')

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)

    # Fix inconsistencies

    # Return
    return tidy, msg


def consistency_stay(tidy, verbose=10):
    # Remove time information
    tidy.date = tidy.date.dt.date

    # Patient information lengths
    aux = tidy.groupby(by=['StudyNo']).agg(
        date_min=('date', 'min'),
        date_max=('date', 'max'))

    # Add difference between dates
    aux['range'] = (aux['date_max'] - aux['date_min']).dt.days
    aux = aux[aux['range'] > 30]

    # Sort
    aux = aux.sort_values(by='range', ascending=False)

    # Create msg
    msg = ""

    if verbose > 0:
        msg += '\n{0}\n'.format('=' * 80)
        msg += 'Evaluating dates...\n\n'
        msg += "Date Range: {0} - {1}\n\n".format(
            aux.date_min.min(), aux.date_max.max())
        msg += '  -<{0}> has {1} inconsistent values.\n'.format('stay', (aux.shape[0]))
        msg += '\nThe \'consistency_stay\' report:\n\n'
        msg += '\t\t%s\n' % aux.to_string() \
            .replace('\n', '\n\t\t')
        msg += "\n" + "=" * 80

    # Return
    return tidy, msg
