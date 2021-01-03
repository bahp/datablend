# Libraries
import numpy as np
import logging
import warnings
import pandas as pd

# DataBlend library
from datablend.core.widgets.base import BaseWidget
from datablend.utils.methods import extract_records_from_tuples

# Create logger
logger = logging.getLogger('dev')


class StackUnitWidget(BaseWidget):
    """This widget appends unit to stacked data.
    """
    # Required columns
    subset = ['to_name', 'unit']

    def get_dataframe(self):
        """Creates dataframe.

        This method extracts from the template a dataframe
        indicating the column indicating the feature name
        and the unit to be merged with.

        Returns
        -------
        pd.DataFrame
        """
        # Parameters
        name, unit = 'to_name', 'unit'

        # Extract unit dataframe
        aux = self.bt.df[[name, unit]] \
            .dropna(how='any')
        aux.columns = ['column', 'unit']

        # Return
        return aux

    def transform(self, data):
        """Performs the transformation."""
        # Return
        return data.merge(self.get_dataframe(), how='left', on='column')


class StackWidget(BaseWidget):
    """This widget stacks data.

    Original format:


    Stacked format:


    """
    # Required columns
    subset = ['to_name', 'timestamp']

    def __init__(self, index, with_unit=True,
                       as_datetime=True):
        self.index = index
        self.with_unit = with_unit
        self.as_datetime = as_datetime

        if with_unit:
            self.subset.append('unit')

    def get_timestamp_feature_tuples(self):
        """Creates tuples (timestamp, feature).

        This method extracts from the template tuples indicating
        the column that will be used as timestamp and the column
        that will be used as feature.

        Returns
        -------
         [('date_enrolment', 'age'),
          ('date_enrolment', 'gender'),
          ('date_collection', 'hct'),
          ('date_collection', 'wbc'),
          ('date_assessment', 'cough')]
        """
        # Parameters
        timestamp, feature = 'timestamp', 'to_name'

        # Get records
        aux = self.bt.df[[timestamp, feature]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[timestamp], d[feature]) for d in aux]

        # Return
        return tuples

    def get_timestamp_feature_events(self):
        """Creates tuples..."""
        if 'event' not in self.bt.df:
            return []
        # Parameters
        date, name = 'to_name', 'event'

        # Get records
        aux = self.bt.df[[date, name]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[date], d[name]) for d in aux]

        # Return
        return tuples

    def transform(self, data, index=None):
        """Performs the transformation.

        .. todo: Implement in extract_records_from_tuples the
                 functionality so that when tuples passed is
                 an empty list, the stacked data is just None
                 or raises an error.

        .. todo: extract_records_from_tuples fails when columns
                 in template are not in the data or viceversa.
        """
        # Get tuples
        tuples = self.get_timestamp_feature_tuples()
        tuples += self.get_timestamp_feature_events()

        # Logging
        if not tuples:
            logger.warning("{0} - There are not defined columns "
                           "to stack. Please review the columns 'timestamp' "
                           "end 'event' on the Template."
                           .format(self.__class__.__name__))
            return None

        # Extract events from tuples
        stacked = extract_records_from_tuples(dataframe=data,
                                              index=self.index,
                                              return_by_types=False,
                                              tuples=tuples, verbose=10)

        # Unit
        if self.with_unit:
            stacked = StackUnitWidget().fit_transform(self.bt, stacked)

        # Cast date to datetime
        if self.as_datetime:
            stacked.date = pd.to_datetime(stacked.date)

        # Return
        return stacked
