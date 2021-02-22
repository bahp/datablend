# Libraries
import copy
import numpy as np
import pandas as pd

# DataBlend Library
from datablend.core.widgets.base import BaseWidget
from datablend.core.consistency import report_unique_value
from datablend.utils.pandas import str2func

# --------------------------------------------
# Methods
# --------------------------------------------

def fillna_levels(data):
    """Fill nan for levels.

    .. note: Fill with 0?
    .. note: Fill interpolated if values found?
    """
    # Columns containing level
    columns = [c for c in data.columns if 'level' in c]
    # Format
    data[columns] = data[columns].fillna(0)
    # Return
    return data


def fillna_events(data):
    """Fill nan for events.

    .. note: Fill with 0?
    .. note: Fill interpolated if values found?
    """
    # Columns containing level
    columns = [c for c in data.columns if 'event' in c]
    # Format
    data[columns] = data[columns].fillna(0)
    # Return
    return data


class StaticTidyWidget(BaseWidget):
    """

    raise:
        More than one value found!

    """
    subset = ['to_name', 'static']

    def __init__(self, by, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)
        self.by = [by] if isinstance(by, str) else by

    def report(self, data, trans, report, columns, verbose=10):
        """This method constructs the report.

        .. note: Use textwrap at some point?
        """

        # Show
        if verbose > 0:
            print('\n' + '=' * 80)

        if verbose > 0:
            msg = report_unique_value(data=data[self.by + columns],
                                      groupby=self.by,
                                      verbose=verbose)
            print(msg)

        if verbose > 1:
            print('The STATIC transformations report:\n\n')
            print('\t\t%s\n' % report.sort_index().to_string().replace('\n', '\n\t\t'))

        if verbose > 0:
            print("=" * 80)

    def transform(self, data, l=None):
        """Apply the transformation.

        .. note: checks that there is only one value. If different values
                 found the column cannot be assumed static and a warning
                 should be raised.

        .. todo: What if not name in data?
        .. todo: Use raise, warn, coerce?
        .. todo: merge list with default settings list?
        .. todo: Check if no template or list then warning!.

        .. note: filter(lambda g: (g.nunique() > 1).any())

        """
        # Copy
        trans = data.copy(deep=True)

        # Get static transformations
        map = self.bt.map_kv(key='to_name', value='static')

        # Keep only existing columns (not needed)
        map = {k: v for k, v in map.items() if k in trans}

        # Apply transformations
        status = {}
        for name, tf in str2func(map).items():
            try:
                trans[name] = trans.groupby(by=self.by)[name].transform(tf)
                status[name] = 'completed'
            except Exception as e:
                status[name] = e

        # -------------
        # Create report
        # -------------
        # Report
        report = {
            'name': map.keys(),
            'transform': map.values(),
            'dtypes.1': trans[map.keys()].dtypes,
            'dtypes.2': trans[map.keys()].convert_dtypes().dtypes,
            'status': status.values()
        }
        report = pd.DataFrame.from_dict(report).set_index('name')

        # Show report
        self.report(data, trans, report, list(map.keys()), verbose=self.verbose)

        # Return
        return data


class DefaultTidyWidget(BaseWidget):
    """Class to set default values from BlenderTemplate.

    raise:
        More than one value found!

    """
    # Required columns
    subset = ['to_name', 'default']

    def get_map(self):
        """
        .. todo: return empty map if they

        Returns
        -------

        """
        # Create empty map
        d = {}
        # Update with to_name defaults
        d.update(self.bt.map_kv(key='to_name', value='default'))
        # Update with event defaults
        d.update(self.bt.map_kv(key='event', value='default'))
        # Return
        return d

    def report(self, data, trans, report, columns, verbose=10):
        """This method constructs the report.

        .. note: Use textwrap at some point?
        """
        # Create message
        msg = ""

        if verbose > 0:
            msg += '\n{0}\n'.format('=' * 80)

        if verbose > 0:
            msg += report_unique_value(data=data[['StudyNo'] + columns],
                                       groupby='StudyNo',
                                       verbose=verbose)
        if verbose > 1:
            msg += 'The {0} report:\n\n'.format(self.__class__.__name__)
            msg += '\t\t%s\n' % report.sort_index() \
                .to_string() \
                .replace('\n', '\n\t\t')

        if verbose > 0:
            msg += '\n{0}\n'.format('=' * 80)

        # Return
        return msg

    def transform(self, data, map=None):
        """Apply the transformation.

        .. note: Check default value has same type as column?
        .. note: Missing percentage tidy[c].notna().mean()*100
        .. todo: What if people want to fill with medians.
        .. todo: Reporting including verbose?

                name     dtype   default status
                anorexia boolean False   completed
                vomiting boolean False   completed
                bleeding boolean False   ignored (no column found)
                ascites  boolean False   ignored (missing>80%)
        """
        # Copy
        trans = data.copy(deep=True)

        # Get map
        map = self.get_map() if map is None else map

        # Keep only existing columns (not needed)
        map = {k: v for k, v in map.items() if k in data}

        # Fill nan
        trans = data.fillna(str2func(map))

        # -------------
        # Create report
        # -------------
        # Report
        report = {
            'name': map.keys(),
            'transform': map.values(),
            'dtypes.1': trans[map.keys()].dtypes,
            'dtypes.2': trans[map.keys()].convert_dtypes().dtypes,
        }
        report['status'] = 'completed'
        report = pd.DataFrame.from_dict(report).set_index('name')

        # Show report
        r = self.report(data, trans, report, list(map.keys()), verbose=self.verbose)

        print(r)

        # Return
        return trans


class DTypesTidyWidget(BaseWidget):
    """This widget...

    .. note: When reading with csv it infers types properly
             but with xls it infers types based on the first
             value and this gives a lots of issues.

    .. check that bools are just True, False, Nan
    """
    # Required columns
    subset = ['to_name', 'dtype']

    def transform(self, data):
        """"""
        # Copy
        data = data.copy(deep=True)

        # Get dtypes
        dtypes = self.bt.map_kv('to_name', 'dtype')

        # Keep only existing columns (not needed)
        dtypes = {k: v for k, v in dtypes.items() if k in data}

        # For those columns that will be boolean.
        rp_bool = {1.0: True, 0.0: False, 1: True, 0: False}
        for k, v in dtypes.items():
            if v != 'boolean':
                continue
            data[k] = data[k].replace(rp_bool)

        # Convert dtypes
        data = data.astype(dtypes)

        # -------------
        # Create report
        # -------------
        # Unique values
        # unique = {k:data[k].unique() for k,v in dtypes.items() if v=='boolean'}

        # current dtype
        # target dtype

        # Create report
        report = pd.DataFrame()
        report['name'] = dtypes.keys()
        report['type'] = dtypes.values()
        report = report.set_index('name')
        report['unique'] = data.nunique()
        report['status'] = 'completed'

        # miss = data.columns.difference(set(dtypes.keys()))
        # missing = pd.DataFrame()
        # missing['name'] = miss
        # missing['status'] = 'missing'

        # report = report.append(missing)
        report = report.sort_index()

        # Show
        print("\n" + "=" * 80)
        print('Setting DTYPES ... \n\n\t%s\n' %
              report.to_string().replace('\n', '\n\t\t'))
        print("=" * 80)

        # Return
        return data


class LevelTidyWidget(BaseWidget):
    """

    raise:
        More than one value found!

    """

    def transform(self, data):
        """Apply the transformation.

        .. note: Check that column has ints.
        .. note: If strings as levels (low, medium, high)?
        """
        # Copy
        data = data.copy(deep=True)

        # Get levels
        levels = [c for c in data.columns if 'level' in c]

        # Format
        data[levels] = data[levels].fillna(0)

        # Return
        return data


# ---------------------------------------------------------
# TidyWidget
# ---------------------------------------------------------
# Libraries
from pandas.api.types import is_bool_dtype


# Helper methods.
def duplicated_combine_set(x):
    """This method combines rows.

    .. note: __repr__ of set orders values.

    The elements in x can be of any type, we cast
    them to the best possible type and we compute
    the mean if they are numeric, the max if they
    are boolean (hence keeping True) or the set of
    values otherwise (string).
    """
    try:
        # Convert dtypes
        x = x.convert_dtypes()
        # Boolean raise exception
        if is_bool_dtype(x.dtype):
            return x.max()
        # Return mean
        return pd.to_numeric(x).mean()
    except Exception as e:
        return ','.join(sorted(x))
        return set(x)


class TidyWidget:
    """This widget creates data in tidy structured.

    It receives data in the so-called stack structure and returns
    the data transformed in tidy structure.

    .. note: When combining duplicates it computes the mean
             for numeric dtypes and creates a set for other
             dtypes such as string or boolean.

    .. todo: Check units before transformation.

    Examples
    --------
    # Create widget
    widget = TidyWidget(index=index, value=value)

    # Transform (keep all)
    transform, duplicated = \
        widget.transform(data, report_duplicated=True)

    # Transform (keep first)
    transform_first = \
        widget.transform(data, keep='first')

    Parameters
    ----------
    index: str or list, default ['id', 'date', 'column']
        The column names with the index. It will be used to
        identify duplicates within the data,.
    value: str, default, result
        The column name with the values
    convert_dtypes: boolean, default True
        Whether convert dtypes.
    reset_index: boolean, default True
        Whether reset index

    Returns
    -------
    """
    errors = {
        'True': True,
        'False': False
    }

    def __init__(self, index=['id', 'date', 'column'],
                 value='result', convert_dtypes=True,
                 reset_index=True, replace_errors=True):
        """Constructor"""
        # Add attributes
        self.index = index
        self.value = value
        self.convert_dtypes = convert_dtypes
        self.reset_index = reset_index

    def fit(self):
        """Does nothing."""
        return self

    def transform(self, data, report_duplicated=False, keep=False):
        """Transform stack data to tidy data.

        .. note: data = data.sort_values(by=['StudyNo', 'date', 'column'])

        .. todo: Review whether pd.pivot_table could be used?

        Old code
        --------
        # Basic formatting
        #replace = {'result': {'False': False, 'True': True}}
        #tidy.date = pd.to_datetime(tidy.date)
        #tidy.date = tidy.date.dt.date
        #tidy = tidy.replace(replace)            # Quick fix str to bool
        #tidy = tidy.drop_duplicates()           # Drop duplicates
        #tidy = tidy.set_index(self.index)

        Parameters
        ----------
        data: pd.DataFrame
            The data in stacked format. It usually has the
            columns ['patient_id', 'date', 'column', 'result'].
            The first three are usually the index and the
            results used as values.

        report_duplicated: boolean, default False
            Whether to return a DataFrame with the duplicates.

        keep: str, default False
            Strategy to remove duplicates. The possible values are
            to keep 'first' appearance, to keep 'last' or to keep
            all appearances combining them in a set using 'False'

        Returns
        -------
        tidy: pd.DataFrame
            The tidy DataFrame

        report: pd.DataFrame
            The report with the duplicate rows.
        """
        # Copy data
        aux = data.copy(deep=True)

        # Remove columns that are not in index
        subset = self.index + [self.value]

        # Keep only interesting
        aux = aux[subset]
        aux = aux.drop_duplicates()
        aux = aux.set_index(self.index)

        # Replace errors
        aux.result = aux.result.replace(self.errors)

        # Look for index duplicates
        duplicated = \
            aux.index.duplicated(keep=keep)

        # Create duplicates
        combination = pd.DataFrame()

        if not keep:
            # Combine duplicates
            combination = aux[duplicated] \
                .groupby(self.index) \
                .result.apply(duplicated_combine_set) \
                .to_frame()

        # Create stack without duplicates
        tidy = pd.concat([aux[~duplicated], combination])
        tidy = tidy.sort_values(by=self.index)

        # Create tidy (pivot)
        tidy = tidy.unstack() \
            .droplevel(level=0, axis=1)

        if self.reset_index:
            tidy = tidy.reset_index()

        if self.convert_dtypes:
            tidy = tidy.convert_dtypes()

        # Return
        if report_duplicated:
            return tidy, aux[duplicated]
        return tidy

    def fit_transform(self, **kwargs):
        """Fit transform (just calls transform)"""
        self.fit()
        self.transform(**kwargs)