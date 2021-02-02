# Libraries
import logging
import pandas as pd
import logging.config

# Own libraries
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
    """This method infers the enumerated maps.

    .. note:

            # CONSTANTS
            CAT = {True: 1, False: 2, None: None}
            SET = set([1, 2, None])

            if u.issubset(SET) and p > 75:
                d[c] = CAT
            else:
                ...

                If only YES NO o TRUE FALSE strings then show boolean convertions?

    """
    # Get only categories
    aux = data.select_dtypes(include=['category'])

    # Create empty dictionary
    d = {}

    # Loop for each column
    for c in aux.columns:
        d[c] = {v: 'V_%s' % i \
            for i, v in enumerate(aux[c].unique())
                if not pd.isnull(v)}

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
            raise BTNullValueError(column='to_name')

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
        """Fits the template from a template dataframe.

        .. note: It converts the values within the column to_replace
                 to dictionaries. Note that they are loaded initially
                 as strings.

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