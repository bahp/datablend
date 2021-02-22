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

# ---------------------------------------------------
# Helper methods
# ---------------------------------------------------
# Transformation functions
def mode(series):
    """"""
    if series.isnull().all():
        return np.nan
    return series.mode()[0]


def fbfill(x):
    """Computes forward and then backward fill."""
    return x.ffill().bfill()


def bffill(x):
    """Computes backward and then forward fill"""
    return x.bfill(x).ffill(x)


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
    if isinstance(d, str):
        if d in TRANSFORMATIONS:
            return TRANSFORMATIONS[d]
    # Return
    return d


def swap_day_month(x):
    """This method...

    .. note: Check that day/month can be swapped by
             ensuring they are in the range (1, 12)

    .. note: Should I return nan?
    """
    if (x.day > 12) or (x.month > 12):
        return np.nan
    return x.replace(month=x.day, day=x.month)


def one_year_more(x):
    return x.replace(year=x.year + 1)

def one_year_less(x):
    return x.replace(year=x.year - 1)

def swap_max_year(x, **kwargs):
    return x


# --------------------------------------------------------------------
# Corrections
# --------------------------------------------------------------------
def fillna_correction(series, method, groupby=None):
    return series.transform(method)


def static_correction(series, method, groupby=None):
    return series.transform(method)


def order_magnitude_correction(series, range=None, orders=[10, 100]):
    """Corrects issues with order of magnitudes.

    Data manually collected often has one/two degrees of magnitude
    higher because one or two digits are pressed accidentally. It
    also happens if the comma was no pressed properly.

    Parameters
    ----------
    series:
    orders:
    range:

    Returns
    -------
    pd.Series
    """
    # Create transform
    transform = series.copy(deep=True)
    # Range
    low, high = range
    # Loop
    for i in orders:
        aux = (transform / i)
        idx = aux.between(low, high)
        transform[idx] = aux[idx]
    # Return
    return transform


def range_correction(series, range=None, value=np.nan):
    """Corrects issues with ranges.

    Some values collected are not within the ranges. They could
    also be removed using the IQR rule, but if we know the limits
    we can filter them as errors instead of outliers.

    Parameters
    ----------
    series:
    range:
    value:

    Returns
    -------
    pd.Series
    """
    # Create transform
    transform = series.copy(deep=True)
    # Range
    low, high = range
    # Correction
    transform[~transform.between(low, high)] = value
    # Return
    return transform


def compound_feature_correction(series, compound):
    """Corrects compound boolean features.

    Some values are collected either in subcategories or a
    final compound category (e.g. bleeding, bleeding_skin
    and bleeding_mucosal). It might happen that there are
    inconsistencies between these data collection.

    The bleeding other assumes that if there is already
    one bleeding collected that agrees with bleeding, then
    it was collected with that purpose and it is set to false

    .. warning: Works with pd.NA but not with np.nan!

    .. note: To create sample dataframe.
        from itertools import product
        v = [True, False, np.nan]
        a = [v, v, v]
        combos = pd.DataFrame(list(product(*a)))
        combos = combos.convert_dtypes()

    Equivalent:
        bleeding = bleeding |
           tidy.bleeding_gi | \
           tidy.bleeding_gum | \
           tidy.bleeding_mucosal | \
           tidy.bleeding_nose | \
           tidy.bleeding_skin | \
           tidy.bleeding_urine | \
           tidy.bleeding_vaginal | \
           tidy.bleeding_vensite

    """
    # Copy data
    transform = series.copy(deep=True)

    # Convert to dtypes
    transform = transform.convert_dtypes()

    # Any true
    any = compound.convert_dtypes().any(axis=1)

    # Set transform
    transform = transform | any
    # other = transform & ~any

    # Return
    return transform


def unique_true_value_correction(series, keep='first'):
    """Corrects more than one True appearance.

    For example, for variable representing events such as
    event_admission where only one value should be True
    during the data collection period.

    .. note: Might not be needed to check with sum.
    .. note: Set to np.nan or False?
    .. warning: The name is miss-leading as unique value
                could be consistent value.

    Parameters
    ----------
    series:
    keep:

    Returns
    -------
    """
    # Ensure boolean input
    # More than one
    if series.sum() > 1:
        series[series.duplicated(keep=keep)] = np.nan
    # Return
    return series


def outlier_dates_correction(series, coef=2.0):
    """Corrects the dates that are outliers.

    It receives all the dates in which samples were collected,
    for example for a patient and tries to (i) identify
    outliers and (ii) correct them with the best possible
    date.

    .. note: Using mean/std for outliers...
    .. note: Should I use days which is more interpretable?

    .. warning: Remember to include always the raw value
                just in case that was the best! Should I
                check only values that are outside range?

    Parameters
    ----------
    series: series with datetime64[ns]
    coeff:


    Returns
    -------
        datetime64[ns] series with corrected dates.
    """
    # Check datetime series or str series (errors='raise)
    # Copy series too!

    # Find outliers
    outliers = np.abs(series - series.mean()) > coef * series.std()


    """
    print(outliers)
    print(np.abs(series - series.mean()))
    print(coef * series.std())
    print(series.quantile([0.05, 0.95]))

    from scipy.spatial.distance import pdist, cdist
    from itertools import product

    #e = np.abs(series - series.mean())

    e = (series - series.mean()).abs().dt.days
    p = np.array(list(product(e, e)))
    #p = np.array([series, series])
    print(p)
    a = pd.DataFrame(p)
    a = a.apply(lambda x: np.abs(x[0]-x[1]), axis=1)
    print(a)

    print(cdist(p))


    #e = series.astype(int)
    #print(e)
    #    / np.timedelta64(-1, 'D')

    print(e)

    import sys
    sys.exit()

    a = list(product(e, e))
    #print(a)

    print(pdist(np.array(a)))
    #print(cdist(series.values, series.values))

    import sys
    sys.exit()
    """

    """
    if len(series) < 3:
        return series

    d = 3
    ddiff = series.diff().dt.days.abs()
    mean = series[ddiff <= 3].mean()
    dff = (series - mean).abs()
    outliers = dff.dt.days > 10
    """
    """
    print("\n\n\nFinding outliers...")
    print("Consecutive distances:")
    print(ddiff)
    print("\nThe mean")
    print(mean)
    print("\nThe difference")
    print(dff)
    print("\nOutliers")
    print(outliers)
    """

    # Do corrections
    if outliers.any():
        print("EE")
        # Compute min and max
        mn, mx, mean = series[~outliers].min(), \
                       series[~outliers].max(), \
                       series[~outliers].mean()

        # Compute various corrections
        r = series[outliers] \
            .transform([lambda x: x,
                        swap_day_month,
                        one_year_more,
                        one_year_less])
        print("A")
        # Find the closest
        days = (r - mean).abs()
        idx = (r - mean).abs().idxmin(axis=1)
        print("O")
        print(r[idx].squeeze())
        # When two outliers it breaks!
        # Replace
        series[outliers] = r[idx].squeeze()
        print("U")
        # Return
        return series

    # Return
    return series


def schema_json_correction(dataframe, schema_json, columns=None):
    """This method...."""

    # Copy dataframe
    corrected = dataframe.copy(deep=True)

    # Loop json records
    for record in schema_json:

        # Get name
        name = record['name']

        if columns:
            if not name in columns:
                continue

        # Column does not exist
        if name not in corrected:
            continue

        # There are no transformations to apply
        if 'transformations' not in record:
            continue

        # Apply all the transformations
        for r in record['transformations']:
            print("Applying correction... | %25s | %30s |" % (name, r[0]), end="")

            function = globals()[r[0]]
            parameters = r[1]

            if r[0] == 'static_correction':
                corrected[name] = \
                    corrected.groupby(by=parameters['groupby'])[name] \
                        .transform(str2func(parameters['method']))

            elif r[0] == 'fillna_correction':
                corrected[name] = \
                    corrected.groupby(by=parameters['groupby'])[name]\
                        .fillna(str2func(parameters['method']))

            elif r[0] == 'unique_true_value_correction':
                # Apply correction
                corrected[name] = \
                    corrected.groupby(by=parameters['groupby'])[name] \
                        .transform(function, parameters['keep'])

            elif r[0] == 'outlier_dates_correction':
                # Apply correction
                corrected[name] = \
                    corrected.groupby(by=parameters['groupby'])[name] \
                        .transform(function, parameters['coef'])

            else:
                corrected[name] = \
                    corrected[name].transform(function, **parameters)

            print(" %5s | %s" % ((~(dataframe[name] == corrected[name])).sum(), r[1]))

    # Get all schema names
    schema_names = [record['name']
        for record in schema_json
            if 'name' in record]

    print("\n\n")
    print("Not configured: %s" % \
          corrected.columns.difference(set(schema_names)))


    #report = pd.DataFrame()
    #report['column'] = corrected.columns
    #print(report)


    """
    if 'default' in record:
        method = record['default']
        corrected[name] = corrected[name].fillna(method)
    """
    # Return
    return corrected


# --------------------------------------------------------------------
# Validations
# --------------------------------------------------------------------
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
