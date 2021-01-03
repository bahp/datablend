# Libraries
from datablend.core.widgets.base import BaseWidget


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

    def get_list(self):
        """Creates tuples (name)

        This method extracts from the template template
        the name of the columns from the renamed dataset
        that have static value.

        Returns
        -------
        ['gender', 'age', 'diabetes']
        """
        # Parameters
        name, static = 'to_name', 'static'

        # Get list
        aux = self.bt.df[[name, static]] \
            .dropna(how='any')[name].tolist()

        # Return
        return aux

    def transform(self, data):
        """Apply the transformation.

        .. todo: check that there is only one value. If different values
                 found the column cannot be assumed static and a warning
                 should be raised.

        .. todo: merge list with default settings list?

        """
        # Copy
        data = data.copy(deep=True)

        # Complete
        for name in self.get_list():
            if name in data:
                data[name] = data.groupby(by='study_number')[name].ffill()
                data[name] = data.groupby(by='study_number')[name].bfill()

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


class TidyWidget(BaseWidget):
    """This widget creates data in tidy structured."""

    def transform(self, data):
        """This method..."""
        # Convert from stack to tidy structure

        # Fill
        trans = StaticTidyWidget().fit_transform(self.bt, data)
        trans = fillna_events(trans)
        trans = fillna_levels(trans)

        # Return
        return trans