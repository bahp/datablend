# Libraries
import re
import ast
import yaml
import json
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

from datablend.core.widgets import RenameWidget
from datablend.core.widgets import ReplaceWidget
from datablend.core.widgets import DateTimeMergeWidget
from datablend.core.widgets import TemplateTransformWidget

from datablend.utils.compute import datetime

"""
# ------------------------------------------
# Constants
# ------------------------------------------
# Load logging configuration
with open('./logging.yaml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

# Config logging from file.
logging.config.dictConfig(config)

# Create logger
logger = logging.getLogger('dev')
"""


def create_descriptor_list(l):
    """This method...

    .. note: Checks"""
    # return [i for i in l]
    return [ColumnDescriptor(**i) if isinstance(i, dict) else i for i in l]


class ColumnDescriptor:
    """This class describes the column transformations.
    """

    def __init__(self, **kwargs):
        """The constructor.

        .. note: default to_name is from_name
        .. note: to_replace is a dict-like

        """
        # Set kwargs as properties
        self.__dict__.update(kwargs)

        # Ensure existence of configured attributes.
        self.from_name = getattr(self, 'from_name', None)
        self.to_name = getattr(self, 'to_name', None)
        self.to_replace = getattr(self, 'to_replace', None)
        self.datetime = getattr(self, 'datetime', False)
        self.datetime_date = getattr(self, 'datetime_date', None)
        self.datetime_time = getattr(self, 'datetime_time', None)  # automatizar esto!
        self.unit = getattr(self, 'unit', None)

        # Format to_name
        if self.to_name is None:
            self.to_name = self.from_name

        # Format to_replace
        if isinstance(self.to_replace, str):
            self.to_replace = str2eval(self.to_replace)

    def transform(self, series):
        """This method transforms the series"""
        if getattr(self, 'datetime', False):
            series = pd.to_datetime(series)
        return series

    def show(self):
        for k, v in self.__dict__.items():
            print("{0}: {1}".format(k, v), end=' | ')
        print("")


def date_time_maps(data):
    """This method...

    .. note: Improve because date can be upper or lower case.
    .. note:
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


class Template:
    """Description...


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

    def has_timestamp(self):
        return not ~self.df.timestamp.isnull().all()

    def check(self):
        pass

    def fit_from_template(self, template):
        """Fits the resources_artificial.

        Parameters
        ----------
        template: pd.DataFrame
            The dataframe with the resources_artificial information.

        Returns
        -------
        Template object
        """
        # Check the resources_artificial is valid.

        # Convert to_replace to dict
        template.to_replace = template.to_replace.apply(str2eval)

        # Set resources_artificial
        self.df = template
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

    def transform(self, data):
        """This method...

        .. todo: raise warnings columns in data are not in resources_artificial
        .. todo: raise warnings columns in temp are not in data
        .. todo: convert merge_date_time as widget?
        """
        # Copy data
        df = data.copy(deep=True)

        # Merge date/time columns.
        df = DateTimeMergeWidget(self.df).transform(df)

        # Rename column names.
        df = RenameWidget(self.df).transform(df)

        # Replace column values.
        df = ReplaceWidget(self.df).transform(df)

        # Template transform
        df = TemplateTransformWidget(self.df).transform(df)

        # Return
        return df

    def __str__(self):
        return str(self.df)


def Blender():
    """This method..."""


class DataBlender:
    """This class helps with the descriptor templates.

    Explanation in detail.

    """
    templates = {}

    def fit(self, data):
        """Creates a configuration file for the data file.

        The result produced is just a resources_artificial and needs further inspection
        by the user to ensure that all the transformations and parameters
        are correct.

        Parameters
        ----------
        filepath: str-like
            The full data filepath (supported .csv, .xls, .xlsx and .json)

        **kwargs:
            The parameters needed to read files using pandas.

        Returns
        --------
        """
        # Create dictionary
        if not isinstance(data, dict):
            data = {'ROOT': data}

        # For each sheet create resources_artificial
        for k, df in data.items():
            self.templates[k] = Template().fit_from_dataframe(df)

        # Return
        return self.templates




class DBDescriptor:
    """This class describes the dataset transformations.

    The aim of this class is to"""



    descriptors = []

    def __init__(self, verbose=10):
        """The constructor."""
        pass

    def fit_dataframe(self, ccfg):
        """Fits from dataframe"""
        ccfg = ccfg.to_json(orient='records')
        ccfg = json.loads(ccfg)
        self.descriptors = create_descriptor_list(ccfg)
        return self

    def fit_csv(self, filepath):
        """Fit DatasetDescriptor from csv file.

        Parameters
        ----------
        filepath: str-like
            Path to the csv file.

        Returns
        --------
        dataset descriptor
        """
        # Load pandas dataframe
        ccfg = pd.read_csv(filepath)
        ccfg = ccfg.to_json(orient='records')
        ccfg = json.loads(ccfg)
        self.descriptors = create_descriptor_list(ccfg)
        return self

    def fit_json(self, filepath):
        """Fit DatasetDescriptor from json file.

        Parameters
        ----------
        filepath: str-like
            Path to the json file.

        Returns
        --------
        dataset descriptor
        """
        # Load list of columns configuration
        with open(filepath) as f:
            ccfg = json.load(f)
            # Format elements
        self.descriptors = create_descriptor_list(ccfg)
        return self

    def fit(self, descriptors=None, filepath=None):
        """Fit the DatasetDescriptor.

        Parameters
        ---------
        descriptors: array-like
            List of dictionaries or ColumnDescriptor objects.

        filepath: string
            Filepath (json) with the ColumnDescriptor informaton
        """
        if filepath is not None:
            if filepath.endswith('.csv'):
                return self.fit_csv(filepath)
            if filepath.endswith('.json'):
                return self.fit_json(filepath)
        elif descriptors is not None:
            # Format elements
            self.descriptors = create_descriptor_list(descriptors)

        # Return
        return self

    def transform(self, dataframe):
        """This method applies the transformations

        .. note: cdf = pd.DataFrame(self.descriptors)
        .. note: cdf = cdf[['from_name', 'to_name']].dropna(how='any')

        Parameters
        ----------
        dataframe: pandas DataFrame object
            The DataFrame in which the transformations will be applied.

        Returns
        -------
        """
        # Copy data
        df = dataframe.copy(deep=True)

        # Warn non-valid descriptors
        for c in self.descriptors:
            if c.from_name not in df.columns:
                print('Warning: <%s> not in DataFrame!' % c.from_name)

        # Merge date and time columns.
        for c in self.descriptors:
            if c.to_name not in df.columns:
                if (c.datetime is not None) and \
                        (c.datetime_date is not None) and \
                        (c.datetime_time is not None):
                    # df[c.to_name] = df.apply(lambda x: datetime(x[c.datetime_date],
                    #                                            x[c.datetime_time]), axis=1)
                    df[c.to_name] = merge_date_time(df, c.datetime_date, c.datetime_time)
                    # df = df.drop(labels=[c.datetime_date,
                    #                     c.datetime_time], axis=1)

        # Rename column names.
        df = df.rename(columns=
                       {c.from_name: c.to_name for c in self.descriptors})

        # Replace column values. Note that the values in the
        # config file contain first the string value and then the
        # number used in the data thus it needs to be reversed.
        #
        # Example: {"Female": 2, "Male": 1}
        df = df.replace({c.to_name:
                             {v: k for k, v in c.to_replace.items()}
                         for c in self.descriptors
                         if c.to_replace is not None})

        # Format columns using descriptors
        for c in self.descriptors:
            if c.to_name in df.columns:
                df[c.to_name] = c.transform(df[c.to_name])

        # Set date as an event.
        for c in self.descriptors:
            if c.to_name == c.timestamp:
                df['%s' % c.to_name.split('_')[-1]] = ~pd.isnull(df[c.to_name])

        # Return
        return df

    def get_timestamp_feature_tuples(self):
        """This method..."""
        l = []
        for c in self.descriptors:
            if c.timestamp is not None:
                if c.to_name == c.timestamp:
                    l.append((c.timestamp, '%s' % c.to_name.split('_')[-1]))
                else:
                    l.append((c.timestamp, c.to_name))
        return l

    def get_units(self):
        return [[c.to_name, c.unit] for c in self.descriptors
                if c.unit is not None]
