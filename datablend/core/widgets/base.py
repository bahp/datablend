# Libraries
import logging

# DataBlend
from datablend.core.blend.template import BlenderTemplate
from datablend.core.exceptions import MissingRequiredColumns

# Create logger
logger = logging.getLogger('dev')


def check_parameter_value(name, value, allowed):
    """This method check possible values of a parameter.

    Parameters
    ----------
    name:
    value:
    allowed:

    Returns
    -------
    object
        The value if it is valid.
    """
    msg = "The parameter <{0}> accepts {2} but '{1}' was found."
    if value not in allowed:
        raise ValueError(msg.format(name, value, allowed))
    return value


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

    def __init__(self, errors='raise', verbose=10):
        """Constructor"""
        self.bt = None
        self.verbose = verbose
        self.errors = check_parameter_value('errors', errors, ['raise', 'warn', 'coerce'])

    def report(data, trans):
        pass

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
            error = MissingRequiredColumns(
                widget=self.__class__.__name__,
                missing=missing)

            if self.errors == 'raise':
                raise error
            if self.errors == 'warn':
                print(error)

            return False
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
        NotDateTime

        Parameters
        ----------
        bt: BlenderTemplate
            The blender template fitted.

        Returns
        -------
        boolean
            Whether the template is compatible with the widget.
        """
        # Basic check
        if not isinstance(bt, BlenderTemplate):
            raise TypeError
        # Do other simple checks
        check1 = self.check_required_columns(bt)
        check2 = True
        check3 = True
        check4 = True
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

        .. note: If the template is compatible with the widget,
                 then the attribute self.bt will have BlenderTemplate
                 otherwise it will remain as None.

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
        # Fit template
        self.fit(template)
        # Template is compatible
        if self.bt is not None:
            return self.transform(data)
        # Return data
        return data