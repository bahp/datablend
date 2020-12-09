# Libraries
import ast
import textwrap
import pandas as pd

from collections import ChainMap

from datablend.utils.methods import merge_date_time


# -----------------------------------
# Methods
# -----------------------------------
def str2eval(x):
    if not pd.isnull(x):
        return ast.literal_eval(x)


def display_descriptor_status(data, config, verbose=0):
    print("\n")
    print("=" * 50)
    print(*textwrap.wrap(('The following columns which '
        'appear on the data have not been specified in the '
        'descriptor configuration file:\n'), width=50), sep='\n')
    print(set(data.columns) - set(config.name))
    print('\n' + "=" * 50)


def display_column_types(df):
    print("\n")
    print("=" * 50)
    print("Columns dtypes:\n")
    print(df.dtypes.sort_index())
    print("=" * 50)


class ColumnsDescriptor:

    def __init__(self, dataframe):
        """The constructor method"""
        # Set DataFrame
        df = dataframe.copy(deep=True)

        # Format
        df.to_rename = df.to_rename.fillna(df.name)
        df.to_rename = df.to_rename.str.lower()
        # df.code = df.code.fillna(df.to_rename)
        # df.code = df.code.str.upper()
        df.to_replace = df.to_replace.apply(str2eval)
        df.to_datetime = df.to_datetime.apply(str2eval)

        # Set DataFrame
        self.df = df

    def get_dict(self, k, v, dropna=True):
        """This method...

        Parameters
        ----------

        Returns
        --------
        """
        # Create dictionary
        d = dict(zip(self.df[k], self.df[v]))

        # Return
        if not dropna:
            return d

        # Return
        return {k: v for k, v in d.items() if not pd.isnull(v)}

    def get_rename_dict(self):
        return self.get_dict(k='name', v='to_rename')

    def get_replace_dict(self):
        return self.get_dict(k='to_rename', v='to_replace')

    def get_datetime_dict(self):
        datetime = self.df.to_datetime.values
        datetime = [e for e in datetime if not pd.isnull(e)]
        datetime = dict(ChainMap(*datetime))
        return datetime

    def get_datetime_column_tuples(self):
        aux = self.df[['to_rename', 'date_column']]
        aux = aux[aux.date_column.notna()]
        tuples = list(zip(aux.date_column, aux.to_rename))
        return tuples

    def format(self, data, verbose=0):
        """This method....

        Returns
        -------
        """
        # Show information
        if verbose > 1:
            display_descriptor_status(data, self.df)

        # Main formatting
        data = self.format_rename_columns(data)
        data = self.format_replace(data)
        data = self.format_date_time_columns(data, verbose=verbose)

        # Format specific columns
        data.study_number = data.study_number.str.replace(" ", "")

        # Convert dtypes.
        #data = data.drop(labels='entry', axis=1)
        data = data.convert_dtypes()

        # Show
        if verbose > 3:
            display_column_types(data)

        # Return
        return data

    def format_rename_columns(self, data):
        return data.rename(columns=self.get_rename_dict())

    def format_replace(self, data):
        return data.replace(self.get_replace_dict())

    def format_date_time_columns(self, data, verbose=0, drop=True):
        # Format
        for k, v in self.get_datetime_dict().items():
            if v[0] in data and v[1] in data:
                if verbose>2:
                    print("Merging <%s, %s> into <%s>." % (v[0], v[1], k))
                data[k] = merge_date_time(data, v[0], v[1])
                if drop:
                    data = data.drop(labels=v, axis=1)
        # Return
        return data


class FeaturesDescriptor:
    pass
