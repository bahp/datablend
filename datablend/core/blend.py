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
from datablend.utils.merge import merge_date_time
from datablend.utils.transformations import convert_dtypes_categorical
from datablend.utils.transformations import convert_dtypes_datetime
from datablend.utils.transformations import format_var_names
from datablend.utils.transformations import str2eval

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

        .. todo: Minimum required columns
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError
        return True

    def fit(self, template):
        """Fits the template.

        .. note: all([isinstance(e, dict) for e in template)

        Parameters
        ----------
        """
        if isinstance(template, pd.DataFrame):
            return self.fit_from_bt_df(template)
        if isinstance(template, list):
            return self.fit_from_bt_df(pd.DataFrame(template))

        raise TypeError
        print("Fit from data")
            #return self.fit_from_data(df)

    def fit_from_bt_df(self, df):
        """Fits the resources_artificial.

        Parameters
        ----------
        template: pd.DataFrame
            The dataframe with the resources_artificial information.

        Returns
        -------
        Template object
        """
        # Raises error if not valid.
        self.valid_blender_template_dataframe(df)

        # Convert to_replace to dict
        if 'to_replace' in df:
            df.to_replace = df.to_replace.apply(str2eval)

        # Set resources_artificial
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

        The result produced is just a resources_artificial and needs further inspection
        by the user to ensure that all the transformations and parameters
        are correct.

        Parameters
        ----------
        data: pd.DataFrame
            A pandas DataFrame with the data.

        Returns
        --------
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

    def transform(self, data, widgets=[]):
        """"""
        pass

    def stack(self, data, index):
        """"""
        pass

    def __str__(self):
        return '\nBlenderTemplate:\n{0}\n'.format(self.df)


class Blender:
    """This method..."""
    templates = {}

    def __init__(self, widgets=[], verbose=0):
        """Constructor"""
        self.widgets = widgets

    def fit(self, info):
        """Fits the blender.

        Parameters
        ----------
        info:

        """
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

        .. todo: include parameter (include sheets).
        .. todo: exclude parameters (exclude sheets).
        .. todo: only process sheets with existing templates[k].
                 raise/log warnings otherwise.

        .. note: If same column passed in include and exclude, by default
                 such column will be excluded. It would be possible to
                 show a warning.

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
            if not k in include:
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

    def stack(self, data, index, include=None, exclude=None):
        """Stacks the data.

        .. todo: This method could go within the StackWidget.
        .. todo: Stack widget by default unit=True. If unit
                 is true look for unit and if it exists in the
                 template then include StackUnitWidget. If no
                 unit then raise warning. If unit=False ignore
                 unit.
        """
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

            # Note importing this library in other places crashes
            from datablend.core.widgets import StackWidget


            stacked[k] = StackWidget(index=['study_no']).fit_transform(self.templates[k], df)

        # Return DataFrame
        if isinstance(data, pd.DataFrame):
            return stacked['ROOT']

        # Return dict of DataFrames
        return stacked

    def tidy(self):
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
