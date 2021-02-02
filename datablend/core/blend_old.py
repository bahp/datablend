# Libraries
import re
import ast
import yaml
import json
import copy
import logging
import numpy as np
import pandas as pd
import logging.config

# Specific
from pathlib import Path

# Own libraries
from datablend.utils.pandas import save_xlsx
from datablend.utils.transformations import convert_dtypes_categorical
from datablend.utils.transformations import convert_dtypes_datetime
from datablend.utils.transformations import format_var_names
from datablend.utils.transformations import str2eval

from datablend.core.exceptions import BTNullValueError
from datablend.core.exceptions import BTMissingRequiredColumnsError
from datablend.core.exceptions import BTDuplicateError

# Configure logger
logger = logging.getLogger('dev')


def date_time_maps(data):
    """This method...

    .. todo : Improve because date can be upper or lower case.
              This issue appears with 32dx Labtime from LAB sheet.
    """

    # Find column ending in date and time
    d = set([c[:-4] for c in data.columns if c.lower().endswith('date')])
    t = set([c[:-4] for c in data.columns if c.lower().endswith('time')])

    # Find the intersection
    dt = t.intersection(d)

    l = [
        {'to_name': 'date_%s' % format_var_names(e),
         'type': 'datetime64[ns]',
         'datetime': True,
         'datetime_date': '%sDate' % e,
         'datetime_time': '%sTime' % e} for e in dt
    ]

    return l


def category_maps(data, max_nunique=5):
    """This method infers the enumerated maps."""

    # CONSTANTS
    CAT = {True: 1, False: 2, None: None}
    SET = set([1, 2, None])

    # Get only categories
    aux = data.select_dtypes(include=['category'])

    # Fill  information
    d = {}
    for c in aux.columns:
        u = set(aux[c].unique())
        p = 100 - (aux[c].isnull().sum() * 100 / len(aux[c]))
        if u.issubset(SET) and p > 75:
            d[c] = CAT
        else:
            d[c] = {'V_%s' % i: v for i, v in enumerate(aux[c].unique())
                    if not pd.isnull(v)}

        # print(c, p,  d[c])

    # Return
    return d


class BlenderTemplate:
    """Description...

    .. todo: raise warnings columns in data are not in temp
    .. todo: raise warnings columns in temp are not in data
    .. todo: function parameter with widgets to compute
    .. todo: check if widgets parameter is valid.

    from_name:

    to_name:

    type:

    to_replace:

    datetime:

    datetime_date:

    datetime_time:

    unit:

    """
    # Dataframe
    df = None

    def __init__(self):
        pass

    def has_columns(self, columns):
        return not self.missing_columns(columns)

    def missing_columns(self, columns):
        return set(columns) - set(self.df.columns)

    def has_timestamp(self):
        return not ~self.df.timestamp.isnull().all()

    def check(self):
        pass

    def valid_blender_template_dataframe(self, df):
        """Whether the template is valid.

        Raises
        ------
        BTMissingRequiredColumnsError
            The required columns ['from_name', 'to_name'] are missing.

        BTDuplicateError
            The column has duplicated values.

        BTRenameError
            Not all the columns in the template have been renamed.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError

        # Missing required columns
        for c in ['from_name', 'to_name']:
            if c not in df.columns.tolist():
                raise BTMissingRequiredColumnsError(missing=c)

        # Duplicate values found
        if any(df.from_name.duplicated()):
            values = df.from_name[df.from_name.duplicated()]
            raise BTDuplicateError(column='from_name',
                                   values=values)

        # Null values found
        if any(pd.isnull(df.to_name)):
            values = df.to_name[df.to_name.duplicated()]
            raise BTNullValueError(column='to_name',
                                   values=values)

        return True

    def map_kv(self, key, value, include_keys=None):
        """This method.....

        Parameters
        ----------
        key: string
            The column to use as keys.
        value: string
            The column to use as values.

        Returns
        -------
        dictionary
        """
        # Return empty map
        if key not in self.df or value not in self.df:
            return {}
        # Return map
        d = self.df.set_index(key) \
            .dropna(subset=[value]) \
            .to_dict()[value]
        # Keep
        return d

    def fit(self, template):
        """Fits the template.

        .. note: all([isinstance(e, dict) for e in template)

        Parameters
        ----------
        template: pd.DataFrame or array of dicts
            The information of the template (see class description).

        Returns
        -------
        BlenderTemplate
        """
        if isinstance(template, pd.DataFrame):
            return self.fit_from_bt_df(template)
        if isinstance(template, list):
            return self.fit_from_bt_df(pd.DataFrame(template))

        raise TypeError

    def fit_from_bt_df(self, df):
        """Fits the template.

        Parameters
        ----------
        df: pd.DataFrame
            The template information as DataFrame

        Returns
        -------
        BlenderTemplate
        """
        # Raises error if not valid.
        self.valid_blender_template_dataframe(df)

        # Convert to_replace to dict
        if 'to_replace' in df:
            df.to_replace = df.to_replace.apply(
                lambda x: x if isinstance(x, dict) else str2eval(x))

        # Set DataFrame
        self.df = df
        # Return
        return self

    def fit_from_data(self, data):
        """Creates a configuration file for the descriptor.

        .. todo: Review the way the category maps are created.
                 For instance rename categories when they have
                 been encoded as numbers, but if they are
                 strings leave them and don't create automatically
                 a to_replace?

        The result produced is just a preliminary template and needs
        further inspection by the user to ensure that all the
        transformations and parameters are correct.

        Parameters
        ----------
        data: pd.DataFrame
            The data from which a preliminary template will be inferred.

        Returns
        --------
        BlenderTemplate
        """
        # Convert data types
        data = data.convert_dtypes()
        data = convert_dtypes_datetime(data)
        data = convert_dtypes_categorical(data)

        # Create empty configuration DataFrame
        ccfg = pd.DataFrame(columns=['from_name',
                                     'to_name',
                                     'type',
                                     'to_replace',
                                     'timestamp',
                                     'datetime',
                                     'datetime_date',
                                     'datetime_time',
                                     'event',
                                     'unit'])

        # Fill basic configuration DataFrame
        ccfg.from_name = data.columns
        ccfg.to_name = ccfg.from_name.apply(format_var_names)
        ccfg.type = data.dtypes.tolist()
        ccfg.type = ccfg.type.astype(str)
        ccfg.datetime = ccfg.type == 'datetime64[ns]'

        # Fill category maps to replace
        ccfg.set_index('from_name', inplace=True)
        ccfg.to_replace = pd.Series(category_maps(data))

        # Fill datetime_date and date_time
        ccfg = ccfg.append(date_time_maps(data))

        # Reset index and keep name in column
        ccfg = ccfg.rename_axis('from_name').reset_index()

        # Set
        self.df = ccfg

        # Return
        return self

    def __str__(self):
        return '\nBlenderTemplate:\n{0}\n'.format(self.df)


class Blender:
    """This method..."""
    templates = {}
    bc = None

    def __init__(self, widgets=[], filepath=None,
                                   curr_path=None,
                                   verbose=0):
        """Constructor"""
        self.widgets = widgets
        if filepath is not None:
            self.bc = BlenderConfig(filepath, curr_path)

    def _fit_from_config(self):
        """This method..."""
        templates = pd.read_excel(self.bc.filepath_temp(), sheet_name=None)
        return self.fit(templates)

    def _stack_from_config(self):
        """This methods stacks from config file"""
        # Get filepath
        filepath = self.bc.filepath_data()

        # Read data
        data = pd.read_excel(filepath,
            sheet_name=None)

        # Transform data
        data = self.transform(data,
            include=self.bc.worksheets_included(),
            exclude=self.bc.worksheets_excluded())

        # Stack data
        return self.stack(data,
            index=self.bc.stack_index(),
            include=self.bc.worksheets_included(),
            exclude=self.bc.worksheets_excluded())

    def _tidy_from_config(self):
        pass

    def fit(self, info=None):
        """Fits the blender.

        Parameters
        ----------
        info: pd.DataFrame or dict-like
            Template to fit in either pd.DataFrame format or a
            dictionary where key is the sheet name and the value
            is the pd.DataFrame.
        """
        # Fit from config
        if info is None:
            return self._fit_from_config()

        # Ensure that it is a dictionary
        if not isinstance(info, dict):
            info = {'ROOT': info}

        # For each sheet create template
        for k, df in info.items():
            self.templates[k] = BlenderTemplate().fit(df)

        # Return
        return self

    def transform(self, data, include=None, exclude=None):
        """Transforms the data according to a template.

        .. note: The result is in the same format as the parameter data.
        .. note: If same column passed in include and exclude, by default
                 such column will be excluded. It would be possible to
                 show a warning.

        .. todo: Only process sheets with existing templates[k] and
                 raise/log warnings otherwise.

        Parameters
        ----------
        data: pd.DataFrame or dict-like
            Data to transform in either pd.DataFrame format or a
            dictionary where key is the sheet name and the value
            is the pd.DataFrame.

        include: list of str
            Name of sheets to be included.

        exclude: list of str
            Name of sheets to be excluded

        Returns
        -------
        """
        # Copy data
        aux = data

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Transform
        for k, df in aux.items():
            # Exclude sheet
            if k not in include:
                continue

            # Logging information
            logger.info("Transforming sheet <{0}>... COMPLETED.".format(k))

            # Apply all widgets.
            for w in self.widgets:
                df = w.fit_transform(self.templates[k], df)

            # Assign df
            aux[k] = df

        if isinstance(data, pd.DataFrame):
            return aux['ROOT']

        return aux

    def fit_transform(self, data):
        pass

    def stack(self, data=None, index=None, include=None, exclude=None):
        """Stacks the data.

        .. todo: Warn skipped sheets?
        .. todo: This method could go within the StackWidget.
        .. todo: Stack widget by default unit=True. If unit
                 is true look for unit and if it exists in the
                 template then include StackUnitWidget. If no
                 unit then raise warning. If unit=False ignore
                 unit.
        """
        if data is None:
            return self._stack_from_config()

        # Copy data
        aux = copy.deepcopy(data)

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Stacked data
        stacked = {}

        # Transform
        for k, df in aux.items():
            # Exclude current sheet
            if not k in include:
                continue

            # Logging information
            logger.info("Stacking sheet <{0}>... COMPLETED.".format(k))

            # Import (importing this library in other places crashes)
            from datablend.core.widgets.stack import StackWidget

            # It no unit then with unit equal False, or create empty or something

            # Stack
            stacked[k] = StackWidget(index=index).fit_transform(self.templates[k], df)

        # Return DataFrame
        if isinstance(data, pd.DataFrame):
            return stacked['ROOT']

        # Return dict of DataFrames
        return stacked

    def tidy(self, data, index, include=None, exclude=None):

        # Copy data
        aux = copy.deepcopy(data)

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Stacked data
        tidied= {}

        # Transform
        for k, df in aux.items():
            # Exclude current sheet
            if not k in include:
                continue

            # Logging information
            logger.info("Tidying sheet <{0}>... COMPLETED.".format(k))

            from datablend.core.widgets.tidy import TidyWidget

            # Create widget
            tidied[k] = TidyWidget(index=index).fit_transform(self.templates[k], df)

        # Return DataFrame
        if isinstance(data, pd.DataFrame):
            return tidied['ROOT']

        # Return dict of DataFrames
        return tidied

    def fit_stack(self):
        pass

    def fit_stack_tidy(self):
        pass

    def save(self, filepath):
        """

        .. todo: bad name and not very intuitive...

        :param filepath:
        :return:
        """
        # Save resources_artificial
        path = Path(filepath)
        path.mkdir(parents=True, exist_ok=True)

        aux = {k:v.df for k,v in self.templates.items()}

        save_xlsx(aux, filepath+'/ccfg.xlsx')

    def load(self):
        pass


import yaml


class BlenderConfig():

    def __init__(self, filepath, curr_path=None):
        """Constructor"""
        # Read yaml configuration
        self.config = yaml.load(open(filepath, 'r'),
            Loader=yaml.FullLoader)

        # Current path
        self.curr_path = curr_path

    def _fullpath(self, path):
        """This method returns fullpath.

        Parameters
        ----------

        Returns
        -------
        str
        """
        if self.curr_path is not None:
            return "{0}/{1}".format(self.curr_path, path)
        else:
            return path

    def filepath_data(self):
        return self._fullpath( \
            self.config['datablend']
                       ['blender']
                       ['filepath_data'])

    def filepath_temp(self):
        return self._fullpath(
            self.config['datablend']
                       ['blender']
                       ['filepath_template'])

    def filepath_logger_config(self):
        return self._fullpath(
            self.config['datablend']
                       ['blender']
                       ['logger_config'])

    def worksheets_included(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['worksheets'] \
                          ['include']

    def worksheets_excluded(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['worksheets'] \
                          ['exclude']

    def stack_index(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['stack'] \
                          ['index']

    def features(self):
        return self.config['features']
