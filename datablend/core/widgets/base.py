# Libraries
import logging

# DataBlend
from datablend.core.blend import BlenderTemplate
from datablend.core.exceptions import MissingRequiredColumns

# Create logger
logger = logging.getLogger('dev')


class BaseWidget:
    """Base widget class

    Attributes
    ----------
    bt: BlenderTemplate
        The blender template.

    subset: array-like
        List with the required columns that must be present in the
        template to successfully apply the widget transformation.

    Methods
    -------

    .. todo: Create generic get_tuples method?
    .. todo: Create generic get_map method?
    .. todo: Create generic get_list method?
    .. todo: errors={'ignore', 'raise', 'coerce'} # warn
        If ‘raise’, then invalid parsing will raise an exception.
        If ‘coerce’, then invalid parsing will be set as NaT. (NA)
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

        Raises
        ------
        MissingRequiredColumns
            Required columns are missing

        Parameters
        ----------
        bt: BlenderTemplate
            The template with the columns

        Returns
        -------
        boolean
            Whether all required columns are in the template
        """
        # Get the required columns
        subset = set(getattr(self, 'subset', []))
        # Does not have the required columns
        if not bt.has_columns(subset):
            missing = bt.missing_columns(subset)
            raise MissingRequiredColumns(missing=missing)
        # Return
        return True

    def compatible_template(self, bt):
        """Verify that the widget can be applied.

        Raises
        ------
        TypeError
            Invalid BlenderTemplate instance.
        MissingRequiredColumns
            Required columns are missing.
        DuplicateValues
            Duplicate values found in from_name.
        EmptyBlenderTemplate
            The BlenderTemplate has not been fitted.

        Parameters
        ----------
        bt: BlenderTemplate
            The blender template fitted.

        Returns
        -------
        boolean
            Whether the template is compatible with the widget.
        """
        if not isinstance(bt, BlenderTemplate):
            raise TypeError
        # Do all basic checks
        check1 = self.check_required_columns(bt)
        # Return
        return check1

    def fit(self, bt):
        """Fit widget.

        Parameters
        ----------
        bt: BlenderTemplate
            The blender template fitted.

        Returns
        -------
        Widget
            The fitted Widget instance.
        """
        # Create blender template
        if not isinstance(bt, BlenderTemplate):
            bt = BlenderTemplate().fit(bt)

        # Check whether template is compatible
        if self.compatible_template(bt):
            self.bt = bt

        # Return
        return self

    def transform(self, data):
        """Transform function needs to be overridden.

        Parameters
        ----------
        data: pd.DataFrame
            DatFrame with the data.

        Returns
        -------
        pd.DataFrame
            Transformed DataFrame
        """
        return data

    def fit_transform(self, template, data):
        """Fit widget and transform data.

        Parameters
        ----------
        template: pd.DataFrame or array of dicts
            The information needed to fit the template.

        data: pd.DataFrame
            DatFrame with the data.

        Returns
        -------
        pd.DataFrame
            Transformed DataFrame
        """
        self.fit(template)
        return self.transform(data)
