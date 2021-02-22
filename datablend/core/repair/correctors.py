"""


"""
# Libraries
import itertools
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


def add_to_date(x, year=0, month=0, day=0):
    """This method...

    .. note: Should I return nan?
    """
    try:
        return x.replace(year=x.year + year,
                         month=x.month + month,
                         day=x.day + day)
    except:
        return x


# --------------------------------------------------------------------
# Corrections
# --------------------------------------------------------------------
def combinations_lower_upper(word):
    return list(map(''.join, itertools.product(\
        *zip(word.upper(), word.lower()))))


# Create map
MAP = {1: True, 0: False, '1': True, '0': False}
MAP.update({k: True for k in combinations_lower_upper('True')})
MAP.update({k: False for k in combinations_lower_upper('False')})
MAP.update({k: True for k in combinations_lower_upper('Yes')})
MAP.update({k: False for k in combinations_lower_upper('No')})
MAP.update({k: True for k in combinations_lower_upper('Y')})
MAP.update({k: False for k in combinations_lower_upper('N')})


def to_boolean(series, copy=True, errors='raise',
            replace_map=MAP):
    """

    Parameters
    ----------
    series: pd.Series
    copy: boolean
    errors: string
    replace_map: dict-like

    Returns
    -------
    pd.Series
        The corrected series.
    """
    # Library
    from pandas.api.types import is_bool_dtype

    # Return series
    if is_bool_dtype(series):
        return series
    # Replace and convert type
    return series.replace(MAP) \
        .astype('boolean', copy, errors)


def dtype_correction(series, dtype, copy=True,
        errors='raise', downcast=None, **kwargs):
    """Enforces specificy dtype.

    .. warning: If series contain decimal values, the output
                will also contain decimal values even when
                dtype Int64 is specified.

    .. note: The astype errors parameter only supports raise
             or ignore. In order to allow coerce for numbers
             we will handle it ourselves in this method.

    .. note: series.astype params are dtype, copy, errors.
    .. note: pd.to_numeric params are errors, downcast
    .. note: pd.to_datetime params are many (**kwargs)

    Parameters
    ----------
    series: pd.Series
        The series to correct
    dtype: str (pandas dtypes)
        The dtype to convert the series
    errors: str (coerce, raise, ignore), default raise
        Whether to raise, ignore or coerce errors
    copy: boolean, default True
        Whether to return a copy
    downcast:
        downcast parameters as per pd.to_numeric
    **kwargs:
        arguments for pd.to_datetime

    Returns
    -------
    pd.Series
        The corrected series.

    Examples
    --------
    >>> dtype_correction(pd.Series(['1', '2']), dtype='Int64', errors='coerce')
    """
    # Enable coerce functionality
    if errors == 'coerce':
        if dtype in ['Int64', 'Float64', 'number']:
            return pd.to_numeric(series, errors, downcast)
        elif dtype in ['datetime64']:
            return pd.to_datetime(series, errors, **kwargs)
        elif dtype in ['boolean']:
            return to_boolean(series, copy, 'raise')

    # Use astype method
    return series.astype(dtype, copy, errors)


def bool_level_correction(df, sbool, slevel):
    """Corrects values of boolean and numeric series.

    It handles boolean and numeric columns representing either the
    presence of a condition (True/False) or the presence of such
    condition through its level (0, 1, 2, 3).

    - If level > 0 then bool condition is True
    - If level == 0 then bool condition is False
    - If level is NaN then bool condition remains

    .. todo: Think carefully whether we should copy the data
             to avoid corrections in place. Also consider whether
             pass all the DataFrame, or exclusively the two
             columns with values to correct. Something like
             bool_level_correction(series_bool, series_level)

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe
    sbool: str
        Label of column with boolean values
    slevel: str
        Label of column with numeric values

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_bool_level.py`.

    Examples
    --------
    >>> abdominal_pain = [False, True, False, True]
    >>> abdominal_pain_level = [0, 0, 1, 2]

    """
    # Convert dtypes
    df[[sbool, slevel]] = df[[sbool, slevel]].convert_dtypes()

    # Indexes
    #idxs = df.notna().any(axis=1)

    # Correct both series
    df[sbool] = df[sbool] | df[slevel].fillna(0) > 0
    df.loc[df[slevel] == 0, sbool] = False

    #df.loc[idxs, sbool] = df.loc[idxs, [sbool, slevel]].any(axis=1)
    #df.loc[idxs, slevel] = df.loc[idxs, slevel].replace(to_replace=0, value=pd.NA)
    #df.loc[idxs, slevel] = df.loc[idxs, slevel].fillna(df[sbool])

    # Return
    return df


def fillna_correction(series, **kwargs):
    """Corrects filling nan with a strategy

    It implements the fillna function from pandas including
    two additional methods:

      - bffill: concatenate backwards then forwards fill
      - fbfill: concatenate forwards then backwards fill

    Parameters
    ----------
    series: pd.Series
        The series
    **kwargs:
        pd.fillna arguments

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_fillna.py`.

    Examples
    --------
    """
    if 'method' in kwargs:
        if kwargs['method'] == 'bffill':
            return series.transform(bffill)
        if kwargs['method'] == 'fbfill':
            return series.transform(fbfill)
    return series.fillna(**kwargs)


def static_correction(series, method, **kwargs):
    """Corrects filling with a consistent value.

    .. note: Mode might return a series with two values with the
             same frequency yet only the first will be considered.

    .. note: max, min, median, mean might have an inconsistent
             behaviour when applied to strings (objects) and
             similarly median and mean might have inconsistent
             behaviour when applied to boolean.

    tidy.shock = \
        tidy.groupby(by='StudyNo').shock \
            .transform(static_correction, method='max')

    Parameters
    ----------
    series: pd.Series
        The pandas series
    method: string or function
        The method which can be a function or a string supported
        by the pandas apply function such as [max, min, median,
        mean, mode, ...]

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_static.py`.

    Examples
    --------
    """
    #if series.isna().all():
    #    return series

    # The series is static already
    if series.nunique(dropna=False) == 1:
        return series

    # Get value to fill with.
    value = series.apply(method)

    # For mode a series is returned
    if isinstance(value, pd.Series):
        value = value[0]

    #print("---")
    #print(series)
    #print(value)

    # Transform
    transform = series.copy(deep=True)
    transform.values[:] = value
    #transform.update(np.repeat(value, series.size))
    #print(transform)

    # Return
    return transform


def categorical_correction(series, categories=[],
        allow_combinations=True, errors='coerce', sep=',',
        value=pd.NA):
    """Corrects ensuring only categories specified are included.

    .. warning: It assumes combinations are comma separated
                without spaces. The user will have to handle
                empty spaces issues with replace or trim.

    .. note: It sorts the output to facilitate comparison of
             multiple combinations. Thus DENV-1,DENV-2 and
             DENV-2,DENV-1 will be corrected as DENV-1,DENV2.

    .. note: It removes duplicates 'DENV-1,DENV-1' as DENV-1

    .. todo: How to raise errors?

    Parameters
    ----------
    series: pd.Series
        The data to correct.
    categories: list
        The categories allowed for the series.
    allow_combinations: boolean, default True
        Whether combinations (e.g. DENV-1,DENV-2) are allowed
    errors: string [raise, coerce], default raise
        - raise raises an exception
        - coerce sets inconsistent values as None

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_categorical.py`.
    """
    # Copy series
    corrected = series.copy(deep=True)

    # Correct single elements
    isin = corrected.isin(categories)
    issep = series.apply(str).str.contains(sep)

    # Allowing combinations
    if allow_combinations:
        # Correct combinations
        combs = corrected[issep]\
            .apply(lambda x: sep.join(sorted(
                set(x.split(sep))
                   .intersection(set(categories)))))
        # Fix empty set
        combs[combs == ''] = value

    if errors == 'raise':
        if (~isin & ~issep).sum() > 0:
            print("ERROR!")
        a = combs.compare(corrected)
        pass

    if errors == 'coerce':
        corrected[~isin] = value
        if allow_combinations:
            corrected.update(combs)

    # Returns
    return corrected


def replace_correction(series, **kwargs):
    """Corrects replacing values.

    Parameters
    ----------
    series: pd.Series
        The pandas series
    **kwargs:
        Arguments as per pandas replace function

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_replace.py`.
    """
    return series.replace(**kwargs)


def order_magnitude_correction(series, range, orders=[10, 100]):
    """Corrects issues related with the order of magnitude.

    It attempts to correct errors that occurs when inputting data
    manually and the values have one or two degrees of magnitude
    higher because one or two digits are pressed accidentally (e.g.
    pressing/missing extra 0s) or a comma is missing (e.g. 37.7 as
    377).

    Parameters
    ----------
    series: pd.Series
        The series to correct.
    range:
        The desired range to accept the correction.
    orders: list, default [10, 100]
        The orders of magnitude to try.

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_order_magnitude.py`.

    Examples
    --------
    .. doctest::

        >>> body_temperature = pd.Series([36, 366, 3660])
        >>> order_magnitude_correction(body_temperature, range=[30, 43])
        [36, 36.6, 36.66]
    """
    # Create transform
    transform = pd.to_numeric(series.copy(deep=True))
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

    .. todo: Check if any outside first otherwise return series.
    .. todo: Warn if replace value is outside range.
    .. todo: Include several options for value:
                value=np.nan
                value=number
                value=(low, high)
                value='edges'

    tidy.dbp = \
        tidy.dbp.transform(range_correction, range=(40, 100))

    Parameters
    ----------
    series: pd.Series (numeric series)
        The pandas series to correct
    range: range or tuple (min, max)
        The range
    value: default np.nan
        The value to use for corrections

    Returns
    -------
    pd.Series

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_range.py`.

    Examples
    --------
    """
    # Create transform
    transform = pd.to_numeric(series.copy(deep=True))
    # Range
    low, high = range
    # Correction
    transform[~transform.between(low, high)] = value
    # Return
    return transform


def unique_true_value_correction(series, value=np.nan, **kwargs):
    """Ensure there is only one True value.

    For example, for variable representing events that can only
    occur once such as event_death, we can correct inconsistent
    series so that only one True value appears.

    .. note: If len(series) <=1 return series
    .. note: Set to value=np.nan or value=False
    .. note: What if there is no true value?
    .. note: Rename to one_true_value_correction

    tidy.event_admission = \
        tidy.groupby(by=['StudyNo']) \
            .event_admission \
            .transform(unique_true_value_correction)

    Parameters
    ----------
    series: pd.Series
        The boolean series to correct.
    **kwargs:
        Arguments to pass to the pandas duplicated function. In
        particular the argument 'keep' which allows (i) 'first'
        to keep first appearance, (ii) 'last' to keep last
        appearance or (iii) 'False' which keeps all appearences.

    Returns
    -------
    pd.Series
        The corrected series

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_unique_true_value.py`.

    Examples
    --------
    """
    # Ensure that it is boolean
    transform = series.copy(deep=True)
    transform = to_boolean(transform)

    # There is no true value!
    if transform.sum() == 0:
        #print("No value found!")
        return series

    # It is already unique
    if transform.sum() == 1:
        return series

    # More than one
    #transform[transform.duplicated(**kwargs)] = value

    # Find duplicates only for Trues
    idxs = transform[transform].duplicated(**kwargs)

    # From those duplicated set values
    transform.loc[idxs[idxs].index] = value

    # Return
    return transform


def causal_correction(x, y):
    """This method is not implemented yet."""
    # if x is one then y must be one.
    pass


def compound_feature_correction(series, compound):
    """Corrects compound boolean features.

    Ensures that the values of a compound feature (e.g. bleeding)
    and its subcategories (e.g. bleeding_skin, bleeding_nose, ...)
    are consistent. The bleeding feature is set to True if the
    current value is True or if any of the bleeding sites is True;
    that is, series | compound.any().

    .. note: Option to return bleeding other if it is not included
             in the compound and the series (bleeding) has True but
             no subcategory (bleeding site) is found.

    .. warning: Works with pd.NA but not with np.nan!

    Parameters
    ----------
    series: pd.Series
        The series to correct
    compound: pd.DataFrame
        The DataFrame with subcategories.

    Returns
    -------
    pd.Series
        The corrected series.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_plot_compound.py`.

    Examples
    --------
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


def date_corrections(x, years=None, use_swap_day_month=True):
    """Applies various possible date corrections

    Parameters
    ----------
    x:
    years:
    swap_day_month:

    Returns
    -------
    """
    # Original value
    corrections = [x]
    # Swapping day month
    corrections += [swap_day_month(x)]
    corrections += [add_to_date(x, year=1)]
    corrections += [add_to_date(x, year=-1)]
    corrections += [add_to_date(x, month=1)]
    corrections += [add_to_date(x, month=-1)]
    # Range of possible years
    if years is not None:
        corrections += [x.replace(year=int(y)) for y in years]
    # Return
    return pd.Series(pd.Series(corrections).unique())


def date_outliers_correction(series,
                             max_days_to_median=20,
                             outliers_as_nat=False):
    """
    This method...

    .. warning: The selection of the first column should not be
                necessary. It should work just with the indx.

                series[outliers] = r[idx].iloc[:, 0]

    .. todo: Include different modes to compute the outliers
             and different methods to correct the dates if
             required:

             outliers = np.abs(series - series.mean()) > coef * series.std()
             outliers = np.abs(series - series.median()) > coef * series.std()

    Parameters
    ----------
    series
    max_day_difference

    Returns
    -------

    """
    # Compute days of difference between day and median
    outliers = (series - series.median()) \
                   .dt.days.abs() > max_days_to_median

    # Return original
    if not outliers.any():
        return series

    # Unique years
    years = series[~outliers].dropna().dt.year.unique()

    # Compute various corrections
    r = series[outliers].apply( \
        date_corrections, years=years)

    # Compute days
    r_days = (r - series.median()).abs()
    r_days = r_days / np.timedelta64(1, 'D')

    # Date closer enough not found
    if not (r_days < max_days_to_median).any(axis=1).any():
        if outliers_as_nat:
            transform = series.copy(deep=True)
            transform[outliers] = pd.NaT

        """
        print("------")
        print(r_days)
        print()
        print(r)
        print()
        print(series.dt.normalize().median())
        print()
        print(series.dt.normalize().value_counts())
        """
    # Find index with smaller days of difference
    idx = (r - series.median()).abs().idxmin(axis=1)

    # Replace in series
    transform = series.copy(deep=True)
    transform[outliers] = r[idx].iloc[:, 0]

    # Return transformed
    return transform


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

    if len(series) < 3:
        return series

    ddiff = series.diff().dt.days.abs()
    mean = series[ddiff <= 3].mean()
    dff = (series - mean).abs()
    outliers = dff.dt.days > 10

    # Do corrections
    if outliers.any():
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

        # Find the closest
        days = (r - mean).abs()
        idx = (r - mean).abs().idxmin(axis=1)
        #print(series)
        #print(r[idx].squeeze())
        # When two outliers it breaks!
        # Replace
        series[outliers] = r[idx].squeeze()
        #print("U")
        # Return
        return series

    # Return
    return series


"""
def schema_correction_stack(dataframe, schema_features, columns=None):
    This method applies all corrections from the schema.

    .. warning: The groupby value is hard coded.!

    Parameters
    ----------
    dataframe: pd.DataFrame
        The DataFrame in stack format. Thus, it needs to have
        the following columns StudyNo, date, column, result and
        unit.

    schema_features: list
        List of dictionaries with all the information of the features
        including the following attributes (explained with a full example
        for simplicity). For more information see xxx

          {'name': 'age',
           'unit': 'year',
           'dtype': 'Int64',
           'transformations': [
              {'range_correction': {'range': [0, 120]},
              {'replace_correction': {'to_replace': {15: 88}},
              {'static_correction': {'method': 'max'},
              {'fillna_correction': {'method': 'ffill'}
            ]}

    columns: list
        List of column names to consider.

    Returns
    -------
    pd.DataFrame

    # Copy DataFrame
    corrected = dataframe.copy(deep=True)

    # Features available in the stacked dataset.
    corrected_features = corrected.column.unique()

    # Include
    if columns is None:
        columns = corrected_features

    # Loop
    for record in schema_features:
        if 'name' not in record:
            continue
        if record['name'] not in columns:
            continue
        if record['name'] not in corrected_features:
            continue
        if 'transformations' not in record:
            continue

        # Get indexes
        idxs = corrected.column == record['name']

        # Apply transformations
        for f, params in record['transformations'].items():
            if f in TRANSFORMATIONS_STACK:

                # Logging information
                print("Applying... %20s | %30s | %s" % \
                      (record['name'], f, params))

                if f in TRANSFORMATION_GROUPBY:
                    # Transformation by patient.
                    corrected.loc[idxs, 'result'] = \
                        corrected[idxs].groupby(by='StudyNo') \
                            .result.transform(globals()[f], **params)
                else:
                    # Transformation whole column.
                    corrected.loc[idxs, 'result'] = \
                        corrected[idxs].result \
                            .transform(globals()[f], **params)

    features_in_schema = [e['name'] for e in schema_features]
    features_in_transformation = \
        [e['name'] for e in schema_features
         if 'transformations' in e]
    features_common = set(columns).intersection(set(features_in_schema))

    # Helpful information
    print("\n\nFeatures in data but not in schema: %s" % \
          set(columns).difference(set(features_in_schema)))

    # Helpful information
    print("\n\nFeatures in data and schema without transformation: %s" % \
          (features_common.difference(set(features_in_transformation))))

    # Return
    return corrected
"""

"""
class SchemaCorrectionTidy:

    def __init__(self, features=None, filepath=None):
        # Libraries
        import yaml

        # Load from filepath
        if filepath is not None:
            # Read yaml configuration
            features = yaml.load(open(filepath, 'r'),
                                 Loader=yaml.FullLoader)['features']

        # Set as dictionary for simplicity
        self.features = {r['name']: r for r in features}

    def get_feature_names(self):
        return [r['name'] for r in self.features
                if 'name' in r]

    def get_feature_records(self, columns):

        def skip(record, features):
            if 'name' not in record:
                return True
            if record['name'] not in features:
                return True
            if 'transformations' not in record:
                return True
            return False

        # Loop
        return [r for r in self.features
                if not skip(r, columns)]

    def transform(self, dataframe, columns=None, report_corrections=True):

        # Create corrections report
        corrections = {}

        # Copy DataFrame
        corrected = dataframe.copy(deep=True)

        # Features available
        if columns is None:
            columns = corrected.columns

        # Loop
        for name in columns:
            # Skip
            if name not in self.features:
                continue
            if 'transformations' not in self.features[name]:
                continue

            # Apply transformations
            for f, params in self.features[name]['transformations'].items():
                if f in TRANSFORMATIONS_TIDY:
                    # Logging information
                    print("Applying... %20s | %30s | %s" % \
                          (name, f, params))

                    if f in TRANSFORMATION_GROUPBY:
                        # Transformation by patient.
                        corrected[name] = \
                            corrected.groupby(by='StudyNo')[name] \
                                .transform(globals()[f], **params)
                    else:

                        corrected[name] = \
                            corrected[name].transform(globals()[f], **params)

            # Compare
            if report_corrections:
                comparison = dataframe[name].compare(corrected[name])
                comparison.columns = ['original', ' corrected']
                comparison = corrected[['StudyNo', 'date']].merge(comparison,
                                                                  left_index=True, right_index=True)
                corrections[name] = comparison

        # Return
        if report_corrections:
            return corrected, corrections
        return corrected
"""

"""
class SchemaCorrectionTidy2:

    def __init__(self, features=None, filepath=None):
        # Libraries
        import yaml

        # Load from filepath
        if filepath is not None:
            # Read yaml configuration
            configuration = yaml.load(open(filepath, 'r'),
                                      Loader=yaml.FullLoader)
            # Set groupby map
            self.groupby_ = \
                configuration['corrector']['groupby']
            # Override features
            features = configuration['features']

        # Set as dictionary for simplicity
        self.features_ = {r['name']: r for r in features}

    def get_transformations(self, name):

        # Skip
        if name not in self.features_:
            return []
        if 'transformations' in self.features_[name]:
            return self.features_[name]['transformations']
        return []

    def get_groupby(self, params):

        if not 'groupby' in params:
            return None
        return self.groupby_[params['groupby']]

    def get_feature_records(self, columns):

        def skip(record, features):
            if 'name' not in record:
                return True
            if record['name'] not in features:
                return True
            if 'transformations' not in record:
                return True
            return False

        # Loop
        return [r for r in self.features
                if not skip(r, columns)]

    def transform(self, dataframe, columns=None, report_corrections=True):

        invalid = {"groupby"}

        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        # Create corrections report
        corrections = {}

        # Copy DataFrame
        corrected = dataframe.copy(deep=True)

        # Features available
        if columns is None:
            columns = corrected.columns

        # Loop
        for name in columns:
            for tf_map in self.get_transformations(name):
                for f, params in tf_map.items():

                    # Logging information
                    print("Applying... %20s | %30s | %s" % \
                          (name, f, params))

                    # Get groupby and function parameters
                    gb_params = self.get_groupby(params)
                    fn_params = without_keys(params, invalid)

                    # Apply correction
                    if gb_params is not None:
                        # Transformation by group
                        corrected[name] = \
                            corrected.groupby(**gb_params)[name] \
                                .transform(globals()[f], **fn_params)
                    else:
                        # Transformation over all column
                        corrected[name] = \
                            corrected[name].transform(globals()[f], **fn_params)

            # Compare
            if report_corrections:
                #comparison = pd.DataFrame()
                
                #comparison = dataframe[name].compare(corrected[name])
                #comparison.columns = ['original', ' corrected']
                #comparison = corrected[[self.groupby_, 'date']].merge(comparison,
                #        left_index=True, right_index=True)
                #corrections[name] = comparison
                

        # Return
        if report_corrections:
            return corrected, corrections
        return corrected

"""
"""
def schema_correction_tidy(dataframe, schema_features, columns=None):
    This method applies all corrections from the schema.

    .. warning: The groupby value is hard coded.!

    Parameters
    ----------
    dataframe: pd.DataFrame
        The DataFrame in tidy format. Thus, it needs to have
        the following columns StudyNo, date, and then one
        column for each feture.

    schema_features: list
        List of dictionaries with all the information of the features
        including the following attributes (explained with a full example
        for simplicity). For more information see xxx

          {'name': 'age',
           'unit': 'year',
           'dtype': 'Int64',
           'transformations': [
              {'range_correction': {'range': [0, 120]},
              {'replace_correction': {'to_replace': {15: 88}},
              {'static_correction': {'method': 'max'},
              {'fillna_correction': {'method': 'ffill'}
            ]}

    columns: list
        List of column names to consider.

    Returns
    -------
    pd.DataFrame

    # Copy DataFrame
    corrected = dataframe.copy(deep=True)

    # Features available in the stacked dataset.
    corrected_features = corrected.columns

    # Include
    if columns is None:
        columns = corrected_features

    # Loop
    for record in schema_features:
        if 'name' not in record:
            continue
        if record['name'] not in columns:
            continue
        if record['name'] not in corrected_features:
            continue
        if 'transformations' not in record:
            continue

        name = record['name']

        # Apply transformations
        for f, params in record['transformations'].items():
            if f in TRANSFORMATIONS_TIDY:

                # Logging information
                print("Applying... %20s | %30s | %s" % \
                      (record['name'], f, params))

                if f in TRANSFORMATION_GROUPBY:
                    # Transformation by patient.
                    corrected[name] = \
                        corrected.groupby(by='StudyNo')[name] \
                            .transform(globals()[f], **params)
                else:

                    corrected[name] = \
                        corrected[name].transform(globals()[f], **params)

    # Return
    return corrected

def schema_json_correction(dataframe, schema_json, columns=None):

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
                    corrected.groupby(by=parameters['groupby'])[name] \
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

    # report = pd.DataFrame()
    # report['column'] = corrected.columns
    # print(report)

   
    #if 'default' in record:
    #    method = record['default']
    #    corrected[name] = corrected[name].fillna(method)

    # Return
    return corrected
"""


# -------------------------------------------------------------------
# Specific corrections for OUCRU conventions
# -------------------------------------------------------------------
def find_level_columns(columns):
    """This method finds level columns."""
    return [e for e in columns if 'level' in e]


def find_bool_columns(columns):
    """This method creates column frrom level column"""
    return [e.replace('_level', '')
            for e in columns if 'level' in e]


def find_bleeding_location_columns(columns):
    """This method find bleeding column sites.

    .. note: bleeding_severe is not a location
             and therefore should not be included.
             Also we should double check that
             they are all boolean variables.

    .. warning: Include other, severe, severity?

    """
    # Create locations
    locations = ['skin', 'mucosal', 'nose', 'gum',
        'urine', 'vaginal', 'vensite', 'gi']
    # Return variables
    return [e for e in columns
        if 'bleeding_' in e and
            e.split('_')[1] in locations]


def oucru_convert_dtypes(tidy, columns=[]):
    """Helper method to apply convert_dtypes.

    Helper method to apply convert_dtypes() to a specific
    set of columns which might or might not be included
    in the DataFrame.

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    columns: list
        The columns to apply convert_dtypes()

    Returns
    -------
    pd.DataFrame
        The DataFrame with columns converted.

    """
    # Find intersection
    intersection = \
        list(set(columns).intersection(tidy.columns))

    # The intersection is empty
    if not intersection:
        return tidy

    # Convert dtypes
    tidy[intersection] = \
        tidy[intersection].convert_dtypes()

    # Return
    return tidy


def oucru_parental_fluid_correction(tidy, verbose=10):
    """Corrects parental fluid related columns.

    It ensures that parental_fluid is True also when the
    parental_fluid_volume is specified but no specific
    parental_fluid column is found.

    .. note: Uses compound_feature_correction

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_parental_fluid.py`.

    Example
    -------
    tidy.parental_fluid = \
        tidy.parental_fluid | \
        (tidy.parental_fluid_volume > 0)
    """
    if verbose > 5:
        print("Applying... oucru_parental_fluid_correction.")

    # Correction
    if 'parental_fluid_volume' in tidy:
        if not 'parental_fluid' in tidy:
            tidy['parental_fluid'] = pd.NA

        # Correct compound feature.
        tidy.parental_fluid = \
            compound_feature_correction( \
                tidy.parental_fluid,
                tidy.parental_fluid_volume.to_frame())

    # Return
    return tidy


def oucru_shock_correction(tidy, verbose=10):
    """Corrects shock related columns.

    It ensures that the columns shock, multiple_shock and
    event_shock are consistent.

    - If >0 event_shock then shock=True
    - If >1 event_shock then shock_multiple=True
    - shock is True if shock or shock_multiple=True

    .. warning: For the boolean logic to work, the types need to
                be converted using the pandas primary dtypes.

    .. warning: Note that no event_shocks are created, so it
                might happen that multiple_shock is True but
                there is only one event_shock recorded.

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_shock.py`.
    """
    if verbose > 5:
        print("Applying... oucru_shock_correction.")

    # Convert dtypes
    tidy = oucru_convert_dtypes(tidy, \
        columns=['shock',
                 'shock_multiple',
                 'event_shock'])

    # Correction
    if 'event_shock' in tidy:

        if 'shock' not in tidy:
            tidy['shock'] = None
        if 'shock_multiple' not in tidy:
            tidy['shock_multiple'] = None

        # At least one shock event
        idxs = tidy \
            .groupby(by='study_no') \
                .event_shock.transform('sum') > 0
        tidy.loc[idxs, 'shock'] = True

        # Multiple shock events.
        idxs = tidy \
            .groupby(by='study_no') \
            .event_shock.transform('sum') > 1
        tidy.loc[idxs, 'shock_multiple'] = True

    if 'shock_multiple' in tidy:
        if 'shock' not in tidy:
            tidy['shock'] = None

        tidy.shock = \
            tidy.shock.convert_dtypes() | \
            tidy.shock_multiple.convert_dtypes()

    # Return
    return tidy


def oucru_pleural_effusion_correction(tidy, verbose=10):
    """Corrects pleural effusion related columns

    .. note: Applies compound_feature_correction to pleural effusion columns.

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_pleural_effusion.py`.

    Example
    -------
    tidy.pleural_effusion = \
        tidy.pleural_effusion | \
        tidy.pleural_effusion_left | \
        tidy.pleural_effusion_right

    """
    if verbose > 5:
        print("Applying... oucru_pleural_effusion_correction.")

    # Correction
    if 'pleural_effusion_left' in tidy or \
       'pleural_effusion_right' in tidy:
        # Ensure columns exist
        if 'pleural_effusion' not in tidy:
            tidy['pleural_effusion'] = pd.NA
        if 'pleural_effusion_left' not in tidy:
            tidy['pleural_effusion_left'] = pd.NA
        if 'pleural_effusion_right' not in tidy:
            tidy['pleural_effusion_right'] = pd.NA

        # Correct compound feature
        tidy.pleural_effusion = \
            compound_feature_correction(\
                tidy.pleural_effusion,
                tidy[['pleural_effusion_left',
                      'pleural_effusion_right']])

    # Return
    return tidy


def oucru_bleeding_correction(tidy, verbose=10):
    """Ensures bleeding and bleeding sites are consistent.

    .. note: Applies compound_feature_correction to bleeding related columns.

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_bleeding.py`.

    Examples
    --------
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
    if verbose > 5:
        print("Applying... oucru_bleeding_correction.")

    # Correction
    if 'bleeding' in tidy:
        # Find bleeding locations
        bleeding_locations = \
            find_bleeding_location_columns(tidy.columns)

        # Correct compound feature bleeding.
        tidy.bleeding = \
            compound_feature_correction(
                tidy.bleeding,
                tidy[bleeding_locations])

    # Return
    return tidy


def oucru_outcome_death_correction(tidy, verbose=10,
        outcome_category='Died'):
    """Corrects outcome when event_date is found.

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.
    outcome_category: str, default Died
        The outcome category to fill outcome

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_outcome_death.py`. ddd
    """
    if verbose > 5:
        print("Applying... oucru_outcome_death_correction.")

        # Convert dtypes
    tidy = oucru_convert_dtypes(tidy, \
        columns=['outcome',
                 'event_death'])

    # Correction
    if 'event_death' in tidy:

        if 'outcome' not in tidy:
            tidy['outcome'] = pd.NA

        # It has an event_death
        idxs_death = tidy \
            .groupby(by='study_no') \
            .event_death.transform('sum') > 0
        tidy.loc[idxs_death, 'outcome'] = outcome_category

        if 'event_discharge' not in tidy:
            tidy['event_discharge'] = None

        # It does not have an event_discharge
        idxs_discharge = tidy \
            .groupby(by='study_no') \
            .event_discharge.transform('sum') == 0
        idxs = idxs_death & idxs_discharge
        tidy.loc[idxs, 'event_discharge'] = \
            tidy.loc[idxs, 'event_death']

    # Return
    return tidy


def oucru_pcr_dengue_correction(tidy, verbose=10):
    """Ensures pcr related columns are consistent.

    .. warning: review!!

    Parameters
    ----------
    tidy: pd.DataFrame
        The DataFrame
    verbose: int
        The level of verbosity.

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame.

    See Also
    --------
    Examples: :ref:`sphx_glr__examples_correctors_oucru_plot_pcr_dengue.py`.
    """
    if verbose > 5:
        print("Applying... oucru_pcr_dengue_correction.")

    # Correction
    if 'pcr_dengue_load' in tidy and \
       'pcr_dengue_serotype' in  tidy:

        # Serotype cannot coincide with zero load.
        idxs_sero = ~(tidy.pcr_dengue_serotype.isin([None, '<LOD']))
        idxs_zero = (tidy.pcr_dengue_load == 0)

        tidy.loc[idxs_sero & idxs_zero, 'pcr_dengue_load'] = None

    if 'pcr_dengue_serotype' in tidy and \
        'pcr_dengue_interpretation' in tidy:

        idxs_sero = ~(tidy.pcr_dengue_serotype.isin([None, '<LOD']))
        tidy.loc[idxs_sero, 'pcr_dengue_interpretation'] = 'Lab-confirmed Dengue'

        idxs_sero = tidy.pcr_dengue_serotype.isin(['<LOD'])
        tidy.loc[idxs_sero, 'pcr_dengue_interpretation'] = 'Not Dengue'


    # Return
    return tidy


def oucru_gender_pregnant_correction(tidy, verbose=10):
    """Ensure that all pregnant patients have appropriate gender.

    Parameters
    ----------
    tidy: pd.DataFrame
        DataFrame with patients data
    verbose: int
        Verbosity level

    Returns
    -------
    pd.DataFrame
        The corrected DataFrame
    """
    if verbose > 5:
        print("Applying... gender_pregnant_correction.")

    if 'pregnant' in tidy:
        if not 'gender' in tidy:
            tidy['gender'] = None

        tidy.loc[tidy['pregnant'], 'gender'] = 'Female'

    return tidy


def day_from_first_true(x, event, tag):
    """Include day for the first True element in x.

    Parameters
    ----------
    x: pd.DataFrame
        DataFrame with patients data
    event: str
        Label for the column with the dessired event
    tag: str
        Tag to label new column (day_from_tag)

    Returns
    -------
    pd.DataFrame
        DataFrame with a column included indicating the
        days from the reference date indicated in event.
    """
    # Keep not nan
    notna = x.dropna(how='any', subset=[event])
    # Create column
    if notna.size:
        x['day_from_%s' % tag] = \
            (x.date - notna.date.values[0]).dt.days
        return x
    x['day_from_%s' % tag] = None
    # Return
    return x


def oucru_correction(tidy, yaml=None):
    """This method computes all OUCRU data corrections.

    - bool/level correction
    - bleeding correction
    - pleural effusion
    - parental fluid
    - shock
    - outcome death
    - pcr_dengue
    - day_from_onset, day_from_admission, day_from_enrolment
    - gender_pregnant_correction
    -
    -
    -
    -

    Parameters
    ----------
    tidy: pd.DataFrame
        The pandas DataFrame in tidy format.

    Returns
    -------
    pd.DatFrame
        The corrected DataFrame
    """

    # ------------------------
    # Corrections
    # ------------------------

    # Corrections bool/level
    # ----------------------
    # .. note: Important to do it before bleeding because it
    #          might convert some bleeding_level with a value
    #          greater than 0 into a positive bleeding.
    # Find tuples
    tuples = list(zip(
        find_level_columns(tidy.columns),
        find_bool_columns(tidy.columns)))

    # Perform corrections
    for slevel, sbool in tuples:
        if not sbool in tidy.columns:
            continue
        if not slevel in tidy.columns:
            continue
        tidy = bool_level_correction(tidy, sbool, slevel)

    # Correction bleeding
    # -------------------
    tidy = oucru_bleeding_correction(tidy)

    # Correction pleural_effusion
    # ---------------------------
    tidy = oucru_pleural_effusion_correction(tidy)

    # Correction parental_fluid
    # -------------------------
    tidy = oucru_parental_fluid_correction(tidy)

    # Correction fever
    # ----------------

    # Correction shock
    # ----------------
    tidy = oucru_shock_correction(tidy)

    # Correction outcome death correction
    # -----------------------------------
    tidy = oucru_outcome_death_correction(tidy)

    # Correction pcr_dengue
    # ---------------------
    tidy = oucru_pcr_dengue_correction(tidy)

    # Correction gender
    # -----------------
    #tidy = oucru_gender_pregnant_correction(tidy)

    # ---------------------------
    # Add new informative columns
    # ---------------------------
    # Days from enrolment
    if 'event_enrolment' in tidy:
        tidy = \
            tidy.groupby('study_no') \
                .apply(day_from_first_true,
                       event='event_enrolment',
                       tag='enrolment')

    # Days from admission
    if 'event_admission' in tidy:
        tidy = \
            tidy.groupby('study_no') \
                .apply(day_from_first_true,
                       event='event_admission',
                       tag='admission')

    # Days from onset
    if 'event_onset' in tidy:
        tidy = \
            tidy.groupby('study_no') \
                .apply(day_from_first_true,
                       event='event_onset',
                       tag='onset')

    """
    # Complications
    # -------------
    # Add complications
    tidy['complications'] = \
        tidy.bleeding_severe | \
        tidy.shock | tidy.shock_multiple | \
        tidy.pleural_effusion
    """

    # Automatic corrector
    # -------------------
    if yaml is not None:
        # Create corrector
        corrector = \
            SchemaCorrectionTidy(filepath=yaml)

        # Apply corrections
        tidy, corrections = \
            corrector.transform(tidy, report_corrections=True)

    # Return
    return tidy


def report_corrections(original, corrected, columns=None,
                       verbose=10, **kwargs):
    """This method...

    Parameters
    ----------
    original
    corrected

    Returns
    -------

    """
    # Set columns
    if columns is None:
        columns = corrected.columns

    # Initialise report
    report = {}

    # Loop
    for c in columns:
        # Newly created column (ignore)
        if c not in original:
            continue

        # Get series
        s1 = original[c]
        s2 = corrected[c]

        # Compare NaN
        idxs1 = s1.isnull() != s2.isnull()

        # Compare elements
        idxs2 = s1[~idxs1] != s2[~idxs1]

        # All
        idxs = idxs1 | idxs2

        # Comparison
        comparison = pd.DataFrame()
        comparison['original'] = original.loc[idxs, c]
        comparison['corrected'] = corrected.loc[idxs, c]

        # No comparison to store
        if not comparison.size:
            continue

        # Save in report
        report[c] = comparison

    # Return
    return report