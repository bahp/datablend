# Libraries
import numpy as np
import logging
import warnings
import pandas as pd

# DataBlend library
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.base import BaseWidget
from datablend.utils.merge import merge_date_time
from datablend.utils.compute import add_days
from datablend.core.exceptions import ReplaceWidgetMapWarning

# Create logger
logger = logging.getLogger('dev')


class RenameWidget(BaseWidget):
    """This widget renames columns.

    .. warning: BlenderTemplate must have 'from_name' and 'to_name'

    .. note: The column 'to_name' from the BlenderTemplate will
             be used to find those data columns whose names will
             be replaced.
    """
    # Required columns
    subset = ['from_name', 'to_name']

    def get_map(self):
        """Creates the rename map.

        This method extracts from the template a dictionary where
        the keys and values indicate the current and target column
        names respectively.

        Example
        -------
        {StudyNo: study_no, BirthDate: dob, Sex: gender}

        Returns
        -------
        dictionary
            Dictionary with {from_name: to_name} keys and values.
        """
        # Parameters
        key, value = 'from_name', 'to_name'

        # Return
        return self.bt.df.set_index(key) \
            .dropna(subset=[value]) \
            .to_dict()[value]

    def transform(self, data):
        """Apply the transformation."""
        # Apply transformation
        return data.rename(columns=self.get_map())


class ReplaceWidget(BaseWidget):
    """This widget replaces values in a column.

      .. warning: BlenderTemplate must have 'from_name' and 'to_replace'.
      .. warning: BlenderTemplate must not have duplicated 'from_name' values.
      .. warning: BlenderTemplate column 'to_replace' must have dictionaries.
                  The transformation from str to dict (str2dict) is performed
                  when creating the BlenderTemplate. It could also be double
                  checked in this Widget.

    """
    # Required columns
    subset = ['from_name', 'to_replace']

    def get_map(self):
        """Creates the replace map.

        This method extracts from the template a dictionary where
        the key indicates the column name and the value is a
        dictionary with the renaming map convention.

        .. note: The default created maps (with keys starting with V_)
                 are not accounted for.

        Example
        -------
         {
            'code: {1:'Positive', 2:'Negative', 3: 'Equivocal'},
            'gender': {1: 'Male', 2: 'Female'},
            'diabetes': {1: True, 2: False}
          }

        Returns
        -------
            dictionary
        """

        def default_dict(d):
            return all([str(e).startswith('V_') for e in list(d.items())])

        # Create records
        aux = self.bt.map_kv(key='from_name', value='to_replace')

        # Remove default created maps
        delete = [k for k, v in aux.items() if default_dict(v)]
        for k in delete:
            del aux[k]

        return aux

    def show_warnings(self, data):
        """This method shows the warning information.

        The warnings are (i) whether there are data values
        that are not defined in the replace map or (ii) if
        there are keys defined in the replace map that do
        not appear in the data.

        Parameters
        ----------
        data: pd.DataFrame
            The data.

        Raises
        ------
            Displays warning on terminal
        """
        # Map Warnings
        for k, v in self.get_map().items():

            # Ignore
            if k.lower() in ['entry']:
                continue

            # Create warning
            w = ReplaceWidgetMapWarning(key=k,
                to_replace=v, data=data[k],
                max_size=10, verbose=5)

            # Raise warning
            if w.is_warning():
                warnings.warn(w)

    def transform(self, data):
        """Apply the transformation"""
        # Check warnings
        self.show_warnings(data)
        # Return
        return data.replace(to_replace=self.get_map())


class DateTimeMergeWidget(BaseWidget):
    """This widget merges date and time columns.

    .. todo: validate datetime_date strings have date format
    .. todo: validate datetime_time strings have time format
    .. todo: What happens when YYYY/MM/DD, YYYY/DD/MM or MM/DD/YY?
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
            data[name] = merge_date_time(data[date], data[time])

        # Return
        return data


class DateFromStudyDayWidget(BaseWidget):
    """This widget format study days to date.

    .. note: This should always go after the RenameWidget.

    .. todo: Check study_day_col is an integer.
    .. todo: Check study_day_ref string have date format.
    .. todo: The names specified do not exist???
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
        # Create date columns from study days
        for name, date, days in self.get_list():
            if days.startswith('-'):
                data[name] = add_days(data[date], -data[days[1:]])
            else:
                data[name] = add_days(data[date], data[days])

        # Return
        return data


class EventWidget(BaseWidget):
    """This widget creates events from date columns.

    .. todo: Ensure that 'from_name' column contains dates.
    """
    # Required columns
    subset = ['event', 'from_name']

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
        name, feature = 'event', 'from_name'

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


class FullTemplateWidget(BaseWidget):

    def transform(self, data):
        """This method performs all the transformations

        .. note: Use the ignore, coerce, raise approach.
        .. note: Order matters for DateFromStudy if it uses a date that
                 has been defined as the combination of separated columns
                 with date and time values.

        Parameters
        ----------

        Returns
        -------
        """
        # Transform
        wdt = DateTimeMergeWidget(errors='warn')
        wds = DateFromStudyDayWidget(errors='warn')
        wrp = ReplaceWidget(errors='warn')
        wev = EventWidget(errors='warn')
        wrn = RenameWidget() # do renaming in stack

        # Transformed data
        transformed = data.copy(deep=True)

        # Apply all widgets.
        for w in [wdt, wds, wrp, wev]:
            #print("FullTemplateWidget: Applying... %s" % w.__class__.__name__)
            if w.compatible_template(self.bt):
                transformed = w.fit_transform(self.bt, transformed)

        # Return
        return transformed


class DateTimeWidget(BaseWidget):
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