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
# Constants
# ---------------------------------------------------
TRANSFORMATIONS_STACK = [
    'range_correction',
    'order_magnitude_correction',
    'replace_correction',
    'static_correction',
    'fillna_correction',
    'unique_true_value_correction'
]

TRANSFORMATIONS_TIDY = [
    'range_correction',
    'order_magnitude_correction',
    'replace_correction',
    'static_correction',
    'fillna_correction',
    #'compound_feature_correction',
    'unique_true_value_correction'
]

TRANSFORMATION_GROUPBY = [
    'static_correction',
    'fillna_correction',
    'unique_true_value_correction'
]


# ---------------------------------------------------
# Helper methods
# ---------------------------------------------------
# Transformation functions
def mode(series):
    """"""
    print(type(series))
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
        return x.replace(year=x.year+year,
                         month=x.month+month,
                         day=x.day+day)
    except:
        return x


# --------------------------------------------------------------------
# Corrections
# --------------------------------------------------------------------
def fillna_correction(series, **kwargs):
    """Corrects filling nan with a strategy

    .. note: Generalise to get function and pass arguments!

    Examples
    --------
    # Fill nan
    tidy.abdominal_pain =
        tidy.groupby(by=['StudyNo']) \
            .abdominal_pain.fillna(False)

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
             same frequency and only the first will be considered.

    Example
    -------
    tidy.shock = \
        tidy.groupby(by='StudyNo').shock \
            .transform(static_correction, method='max')

    Parameters
    ----------
    method: string
        The method which can be a function or a string supported
        by the pandas apply function such as [max, min, median,
        mean, mode]
    """
    # The series is static already
    if series.nunique(dropna=False) == 1:
        return series

    # Get value to fill with.
    value = series.apply(method)

    # For mode a series is returned
    if isinstance(value, pd.Series):
        value = value[0]

    # Transform
    transform = series.copy(deep=True)
    transform.update(np.repeat(value, len(series)))

    # Return
    return transform


def replace_correction(series, **kwargs):
    """Corrects replacing values"""
    return series.replace(**kwargs)


def order_magnitude_correction(series, range, orders=[10, 100]):
    """Corrects issues with order of magnitudes.

    Data manually collected often has one/two degrees of magnitude
    higher because one or two digits are pressed accidentally. It
    also happens if the comma was no pressed properly.

    Examples
    --------
    tidy.body_temperature = tidy.body_temperature \
        .transform(order_magnitude_correction range=(20, 50))

    Parameters
    ----------
    series: pd.Series
        The series to correct.
    orders: list
        The orders of magnitude to try.
    range:
        The desired range to accept the correction.

    Returns
    -------
        pd.Series
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

    .. todo: Warn if replace value is outside range.
    .. todo: Include several options for value:
                value=np.nan
                value=number
                value=(low, high)
                value='edges'

    .. todo: If transformation to numeric fails show error!

    Example
    -------
    tidy.dbp = \
        tidy.dbp.transform(range_correction, range=(40, 100))

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
    transform = pd.to_numeric(series.copy(deep=True))
    # Range
    low, high = range
    # Correction
    transform[~transform.between(low, high)] = value
    # Return
    return transform


def category_correction(series, **kwargs):
    """Corrects weird categories!

    .. note: Can be done using the replace_correction?
    """
    pass


def causal_correction(x, y):
    #if x is one then y must be one.
    pass


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

    Parameters
    ----------
    series: pd.Series
        The series to correct
    compound: pd.DataFrame
        The elements to consider

    Returns
    -------
        pd.Series


    Examples
    --------
    # Correct compound feature bleeding (careful use pd.NA)
    tidy.bleeding = \
        compound_feature_correction(tidy.bleeding,
            tidy[['bleeding_skin',
                  'bleeding_mucosal',
                  'bleeding_nose',
                  'bleeding_skin',
                  'bleeding_urine',
                  'bleeding_vaginal',
                  'bleeding_vensite']])

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


def unique_true_value_correction(series, value=np.nan, **kwargs):
    """Corrects more than one True appearance.

    For example, for variable representing events such as
    event_admission where only one value should be True
    during the data collection period.

    .. note: If len(series) <=1 return series
    .. note: Set to value=np.nan or value=False
    .. note: What if there is no true value?
    .. note: Rename to one_true_value_correction

    Examples
    --------
    tidy.event_admission = \
        tidy.groupby(by=['StudyNo']) \
            .event_admission \
            .transform(unique_true_value_correction)

    Parameters
    ----------
    series: pd.Series
    **kwargs:
        Argument keep to pass to duplicated function. The possible
        values are ['first', 'last', 'false'].

    Returns
    -------
    """
    # Check series is of type bool

    # No need to convert to boolean
    # transform = series.apply(bool)
    transform = series.copy(deep=True)

    # There is no true value!
    if transform.sum() == 0:
        print("No value found!")
        return series

    # It is already unique
    if transform.sum() == 1:
        return series

    # More than one
    transform[transform.duplicated(**kwargs)] = value

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
        corrections += [x.replace(year=y) for y in years]
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
    years = series[~outliers].dt.year.unique()

    # Compute various corrections
    r = series[outliers].apply(\
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
        print(series)
        print(r[idx].squeeze())
        # When two outliers it breaks!
        # Replace
        series[outliers] = r[idx].squeeze()
        print("U")
        # Return
        return series

    # Return
    return series


def schema_correction_stack(dataframe, schema_features, columns=None):
    """This method applies all corrections from the schema.

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

    """
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


class SchemaCorrectionTidy:
    """Class to apply corrections.

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
    """

    def __init__(self, features=None, filepath=None):
        """Constructor"""
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
        """Get columns in features."""

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
        """This method applies all corrections from the schema.

        .. warning: The groupby value is hard coded.!

        Parameters
        ----------
        dataframe: pd.DataFrame
            The DataFrame in tidy format.
        columns: list
            List of column names to consider.

        Returns
        -------
        pd.DataFrame
        """
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


class SchemaCorrectionTidy2:
    """Class to apply corrections.

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
    """

    def __init__(self, features=None, filepath=None):
        """Constructor"""
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
        """"""
        # Skip
        if name not in self.features_:
            return []
        if 'transformations' in self.features_[name]:
            return self.features_[name]['transformations']
        return []


    def get_groupby(self, params):
        """Retrieve defined groupby map

        Parameters
        ----------
        key: str
        params: dict

        Returns
        -------
        """
        if not 'groupby' in params:
            return None
        return self.groupby_[params['groupby']]

    def get_feature_records(self, columns):
        """Get columns in features."""

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
        """This method applies all corrections from the schema.

        .. warning: The groupby value is hard coded.!

        Parameters
        ----------
        dataframe: pd.DataFrame
            The DataFrame in tidy format.
        columns: list
            List of column names to consider.

        Returns
        -------
        pd.DataFrame
        """
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
                comparison = pd.DataFrame()
                """
                comparison = dataframe[name].compare(corrected[name])
                comparison.columns = ['original', ' corrected']
                comparison = corrected[[self.groupby_, 'date']].merge(comparison,
                        left_index=True, right_index=True)
                corrections[name] = comparison
                """

        # Return
        if report_corrections:
            return corrected, corrections
        return corrected







def schema_correction_tidy(dataframe, schema_features, columns=None):
    """This method applies all corrections from the schema.

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

    """
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
