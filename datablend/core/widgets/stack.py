# Libraries
import numpy as np
import logging
import warnings
import pandas as pd

# DataBlend library
from datablend.core.widgets.base import BaseWidget
from datablend.core.widgets.format import RenameWidget
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


# ---------------------------------------------
# StackWidget
# ---------------------------------------------
class StackWidget(BaseWidget):
    """This widget stacks data.

    Original format:


    Stacked format:


    """
    # Required columns
    subset = ['to_name', 'timestamp']

    def __init__(self, index, with_unit=True,
                              rename=True,
                              as_datetime=True,
                              errors='raise'):
        """Constructor"""
        super().__init__(errors)
        self.index = index
        self.with_unit = with_unit
        self.as_datetime = as_datetime
        self.rename = rename

        #if self.with_unit:
        #   self.subset.append('unit')

        #print(self.subset)

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
        timestamp, feature = 'timestamp', 'from_name'

        # The timestamps are given using the newly defined to_name
        # feature. However, the data has only original column names
        # (from_name). Thus we cast the column timestamp from
        # to_names to from_names.
        rn = {'timestamp': self.bt.map_kv('to_name', 'from_name')}

        # Get combos timestamp feature
        aux = self.bt.df.replace(rn) \
            [[timestamp, feature]] \
            .dropna(how='any')

        # Return
        return list(zip(aux[timestamp], aux[feature]))

    def get_timestamp_feature_events(self):
        """Creates tuples..."""
        if 'event' not in self.bt.df:
            return []
        # Parameters
        date, name = 'from_name', 'event'
        #date, name = 'to_name', 'event'

        # Get records
        aux = self.bt.df[[date, name]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[date], d[name]) for d in aux]

        # Return
        return tuples

    def transform(self, data, date_feature_tuples=None):
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
            logger.warning("{0} - There are not defined columns to "
                           "stack. Please review the columns 'timestamp' "
                           "end 'event' on the Template."
                           .format(self.__class__.__name__))
            return pd.DataFrame()

        for timestamp, column in tuples:
            if column not in data:
                print("\nThe BlenderTemplate contains the value '%s' in either \n"
                      "the timestamp/event columns. However, such column does not exist \n"
                      "in the data and will be ignored!" % column)

        # Clean tuples
        tuples = [(t, c) for t, c in tuples if c in data]

        # Get renaming map
        rn = self.bt.map_kv(key='from_name',
                            value='to_name')

        # Rename exclusively the index. This is done because when
        # we configure the corrector.yaml only one common index
        # can be passed but the original data might have different
        # names from it (e.g. StudyNo, StudyCode, ...) thus we just
        # set the to_name in the templates and rename all of them
        # in the first instance here.
        rn_index = {k: v
            for k, v in rn.items()
                if v in self.index}
        data = data.rename(columns=rn_index)

        # Extract events from tuples
        stacked = extract_records_from_tuples(dataframe=data,
            index=self.index, return_by_types=False,
            tuples=tuples, verbose=10)

        # Rename column names
        if self.rename:
            stacked = stacked.replace({'column': rn})

        # Include unit
        #if self.with_unit:
        stacked = StackUnitWidget(errors='warn') \
            .fit_transform(self.bt, stacked)

        # Cast date to datetime
        if self.as_datetime:
            stacked.date = pd.to_datetime(stacked.date)

        # Drop duplicates
        stacked = stacked.drop_duplicates()

        # Return
        return stacked
