# Libraries
import logging
import pandas as pd

# Own
from datablend.utils.merge import merge_date_time
from datablend.utils.compute import add_days
from datablend.utils.methods import extract_records_from_tuples

from datablend.core.blend import BlenderTemplate
from datablend.core.exceptions import MissingRequiredColumns

# Create logger
logger = logging.getLogger('dev')


class BaseWidget:
    """Base widget class

    .. todo: Create generic get_tuples method?
    .. todo: Create generic get_map method?
    .. todo: Create generic get_list method?
    .. todo: errors={'ignore', 'raise', 'coerce'} # warn
        If ‘raise’, then invalid parsing will raise an exception.
        If ‘coerce’, then invalid parsing will be set as NaT.
        If ‘ignore’, then invalid parsing will return the input.
    """

    def __init__(self):
        """Constructor"""
        self.bt = None

    def check_required_columns(self, bt):
        """Verify required columns.

        .. todo: Improve the logging of warnings.
        .. todo: Include class RenameWidget.
        .. todo: Include description.
        .. todo: Raise error might be to strict, just display warning?

        Returns
        -------
        boolean: whether all columns are in template"""
        # Get the required columns
        subset = set(getattr(self, 'subset', []))
        # Does not have the required columns
        if not bt.has_columns(subset):
            missing = bt.missing_columns(subset)
            print("Missing columns: %s" % str(missing))
            raise MissingRequiredColumns()
        # Return
        return True

    def compatible_template(self, bt):
        """Verify that widget can be applied.

        Parameters
        ----------
        bt: BlenderTemplate
            The blender template fitted.

        Returns
        -------
        """
        if not isinstance(bt, BlenderTemplate):
            raise TypeError
        # Do all basic checks
        check1 = self.check_required_columns(bt)
        # Return
        return check1

    def fit(self, bt):
        """Fits widget."""
        # Create blender template
        if not isinstance(bt, BlenderTemplate):
            bt = BlenderTemplate().fit(bt)

        # Check whether template is compatible
        if self.compatible_template(bt):
            self.bt = bt

        # Return
        return self

    def transform(self, data):
        """Transform function needs to be overridden."""
        return data

    def fit_transform(self, template, data):
        """Fit widget and transform data."""
        self.fit(template)
        return self.transform(data)


class RenameWidget(BaseWidget):
    """This widget renames columns.

    .. note: The column 'to_name' from the BlenderTemplate will
             be used to find those data columns whose values
             will be replace.
    """
    # Required columns
    subset = ['from_name', 'to_name']

    def get_map(self):
        """Creates the rename map.

        This method extracts from the template a dictionary where
        the key indicates the current column name and the value
        the target column name.

        Returns
        -------
        {StudyNo: study_no, BirthDate: dob, Sex: gender}
        """
        # Parameters
        key, value = 'from_name', 'to_name'

        # Return
        return self.bt.df.set_index(key) \
            .dropna(subset=[value]) \
            .to_dict()[value]

    def transform(self, data):
        """Performs the transformation.
        """
        # Apply transformation
        return data.rename(columns=self.get_map())


class ReplaceWidget(BaseWidget):
    """This widget replaces values in a column.
    """
    # Required columns
    subset = ['to_name', 'to_replace']

    def get_map(self):
        """Creates the replace map.

        This method extracts from the template a dictionary where
        the key indicates the column name and the value is a
        dictionary with the renaming map convention.

        .. note: the column to_replace contains dictionaries. The
                 transformation from str to dict (str2dict) is
                 performed when creating the BlenderTemplate.

        .. todo: This invert might be caused by the way we have
                 created the resources_artificial. Think carefully
                 to avoid this extra coding. Keep the invert
                 function and or option in parameters.

        Returns
        -------
        {'code: {'Positive': 1, 'Negative': 2, 'Equivocal': 3},
         'gender': {'Male': 1, 'Female': 2},
         'diabetes': {True: 1, False: 2}}

        """

        def invert(d):
            return {v: k for k, v in d.items()}

        # Parameters
        key, value = 'to_name', 'to_replace'

        # Create records
        aux = self.bt.df.dropna(subset=[key, value]) \
                  .set_index(key).to_dict()[value]

        # Return inverted
        return {k: invert(v) for k, v in aux.items()}

    def transform(self, data):
        """Performs the transformation"""
        return data.replace(to_replace=self.get_map())


class DateTimeMergeWidget(BaseWidget):
    """This widget merges date and time columns.

    .. todo: validate datetime_date strings have date format
    .. todo: validate datetune_time strings have time format
    .. todo: should the columns datetime_date and datetime_time
             contain original names (from_name) or renamed values
             (to_name) for consistency?
    .. todo: What happens when YYYY/MM/DD or YYYY/DD/MM?
    .. todo: What happens when bad time (e.g. 24:00!!!)
    """
    # Required columns
    subset = ['to_name', 'datetime_date', 'datetime_time']

    def get_list(self):
        """Creates tuples (name, date, time)

        This method extracts from the template tuples indicating
        the column that will be used as name, the column that will
        be used as date and the column that will be used as time.

        Returns
        -------
        [('date_enrolment', 'enDate', 'enTime'),
         ('date_assessment', 'aDate', 'astime')]
        """
        # Parameters
        name = 'to_name'
        date = 'datetime_date'
        time = 'datetime_time'

        # Extract records
        aux = self.bt.df[[name, date, time]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[name], d[date], d[time]) for d in aux]

        # Return
        return tuples

    def transform(self, data):
        """Performs the transformation."""
        # Merge date/time columns.
        for name, date, time in self.get_list():
            data[name] = merge_date_time(data, date, time)

        # Return
        return data


class DateFromStudyDayWidget(BaseWidget):
    """This widget format study days to date.

    .. todo: Check study_day_col is an integer.
    .. todo: Check study_day_ref string have date format.
    .. todo: Since the study_day_ref must be a date, should I
             convert this column in the data? Or should I create
             a new widget DateTimeWidget to do so? Including also
             the conversion of those columns containing 'date'.
    """
    # Required columns
    subset = ['to_name', 'study_day_col', 'study_day_ref']

    def get_list(self):
        """Creates tuples (name, date, days)

        This method extracts from the template tuples indicating
        the column that will be used as name, the column that will
        be used as date and the column with the days to add.

        Returns
        -------
        [('date_laboratory', 'date_enrolment', 'study_day')]
        """
        # Parameters
        name = 'to_name'
        days = 'study_day_col'
        date = 'study_day_ref'

        # Extract records
        aux = self.bt.df[[name, date, days]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[name], d[date], d[days]) for d in aux]

        # Return
        return tuples

    def transform(self, data):
        """Performs the transformation."""
        # Create date columns from stuy days
        for name, date, days in self.get_list():
            data[name] = add_days(data[date], data[days])

        # Return
        return data


class EventWidget(BaseWidget):
    """This widget creates events from date columns.

    .. todo: Ensure that 'to_name' column is a date.
    """
    # Required columns
    subset = ['event', 'to_name']

    def get_list(self):
        """Creates tuples (name, date, days)

        This method extracts from the template tuples indicating
        the column that will be used as name and the column that
        will be used as date.

        Returns
        -------
        [('admission', 'date_admission')]
        """
        # Parameters
        name, feature = 'event', 'to_name'

        # Get records
        aux = self.bt.df[[name, feature]] \
            .dropna(how='any') \
            .to_dict(orient='records')

        # Format as tuples
        tuples = [(d[name], d[feature]) for d in aux]

        # Return
        return tuples

    def transform(self, data):
        """Performs the transformation"""
        # Create event columns
        for name, feature in self.get_list():
            data[name] = ~pd.isnull(data[feature])

        # Return
        return data


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

    def __init__(self, index, with_unit=True):
        self.index = index
        self.with_unit = with_unit

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
                                              index=self.index, return_by_types=False,
                                              tuples=tuples, verbose=10)

        # Unit
        if self.with_unit:
            stacked = StackUnitWidget().fit_transform(self.bt, stacked)

        # Return
        return stacked


class FullTemplateWidget(BaseWidget):
    pass

class TemplateTransformWidget(BaseWidget):
    """This widget performs basic data formatting from the template.
    """
    # Required columns
    subset = ['to_name', 'timestamp']

    def get_datetimes_list(self):
        """"""
        date = 'datetime'
        name = 'to_name'
        return self.bt.df[[name, date]] \
            .dropna(how='any')[self.bt.df[date] == True][name] \
            .tolist()

    def transform(self, data):
        """Performs the transformation.

        .. todo: to_replace str2dict
        .. todo: cast to datetime all datetimes.
        .. todo: cast to datetime if date in name.
        """
        # Format dates
        for d in self.get_datetimes_list():
            data[d] = pd.to_datetime(data[d])

        # Return
        return data
