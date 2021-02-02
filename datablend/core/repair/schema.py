"""


"""
# Libraries
import yaml
import numpy as np
import pandas as pd

# Import correctors (for globals()[] to work).
from datablend.core.repair.correctors import dtype_correction
from datablend.core.repair.correctors import range_correction
from datablend.core.repair.correctors import order_magnitude_correction
from datablend.core.repair.correctors import replace_correction
from datablend.core.repair.correctors import static_correction
from datablend.core.repair.correctors import fillna_correction
from datablend.core.repair.correctors import unique_true_value_correction
from datablend.core.repair.correctors import date_outliers_correction


# ----------------------------------------------
# Helper methods
# ----------------------------------------------
def _finditem(obj, key):
    """Finds an item in a dictionary recursively.

    Parameters
    ----------
    obj: dict-like
        The dictionary to investigate.
    key: str-like
        The key to find

    Returns
    -------
    object
    """
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item


# ----------------------------------------------
# Main classes
# ----------------------------------------------
class SchemaCorrectorBase:
    """Class to apply corrections.

    List of dictionaries with all the information of the features
    including the following attributes (explained with a full example
    for simplicity).

    For more information see corrector.yaml.

    """

    def __init__(self, features=None, filepath=None):
        """Constructor"""
        # Load from filepath
        if filepath is not None:
            # Read yaml configuration
            configuration = yaml.load(open(filepath, 'r'),
                                      Loader=yaml.FullLoader)

            # Set groupby map
            self.groupby_ = \
                configuration['corrector']['groupby']

            # Override features
            features = configuration['features']

        # Set as dictionary for simplicity
        self.features_ = {r['name']: r for r in features}

    def get_transformations(self, name):
        """"""
        # Skip
        if name not in self.features_:
            return []
        if 'transformations' in self.features_[name]:
            return self.features_[name]['transformations']
        return []

    def get_groupby(self, params):
        """Retrieve defined groupby map

        Parameters
        ----------
        key: str
        params: dict

        Returns
        -------
        """
        if not 'groupby' in params:
            return None
        return self.groupby_[params['groupby']]

    def get_feature_records(self, columns):
        """Get columns in features."""

        def skip(record, features):
            if 'name' not in record:
                return True
            if record['name'] not in features:
                return True
            if 'transformations' not in record:
                return True
            return False

        # Loop
        return [r for r in self.features
                if not skip(r, columns)]

    def transform(self, **kwargs):
        pass

    def features_summary(self, dataframe=None, columns=None):
        """Create summary of features.

        If DataFrame is not None, all the columns will appear
        in the summary.

        .. todo: A bit messy, could be improved!

        Parameters
        ----------
        columns: list
            The features to consider.

        Returns
        -------
            pd.DataFrame
        """
        # Libraries
        import copy

        # Columns to include
        if dataframe is not None:
            columns = dataframe.columns

        # Filter columns
        if columns is None:
            columns = self.features_.keys()

        # Create report
        report = []

        # Loop to fill record
        for name in columns:
            # Create dictionary
            d = {'name': name}

            # Skip
            if name not in self.features_:
                report.append(d)
                continue

            # Include more information
            record = copy.deepcopy(self.features_[name])
            d.update(record)
            d['included'] = 'Yes'
            # Get transformations
            transformations = self.get_transformations(name)
            # Loop adding transformations
            for record in transformations:
                d.update(record)
            # Add transformations info
            if len(transformations) > 1:
                d['transform'] = 'Yes'
                del d['transformations']

            # Append
            report.append(d)

        # Create report
        report = pd.DataFrame(report)
        drop = ['categories', 'range', 'code']
        report = report.drop(columns=report.columns.intersection(set(drop)))

        # Return
        return report


class SchemaCorrectionTidy(SchemaCorrectorBase):
    """Class to apply corrections for tidy datasets.
    """
    def transform(self, dataframe, columns=None,
                  report_corrections=True, verbose=10):
        """Corrects dataset in tidy format.

        .. warning: Ensure DataFrame is properly sorted (e.g.
                    by patient_id and date) and sampled so that
                    methods such as ffill work as expected.

        Parameters
        ----------
        DataFrame:
            The DataFrame to correct.
        columns:
            The selected columns
        report_corrections
            Whether to report the corrections.

        Returns
        -------
        """
        if verbose > 1:
            print("\n\nApplying SchemaCorrectionTidy!\n")


        invalid = {"groupby"}

        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        # Create corrections report
        corrections = {}

        # Copy DataFrame
        corrected = dataframe.copy(deep=True)

        # Features available
        if columns is None:
            columns = corrected.columns

        # Loop
        for name in columns:
            for tf_map in self.get_transformations(name):
                for f, params in tf_map.items():

                    # Logging information
                    if verbose > 5:
                        print("%30s: Applying... %25s | %30s | %s" %
                              (self.__class__.__name__, name, f, params))

                    # Get groupby and function parameters
                    gb_params = self.get_groupby(params)
                    fn_params = without_keys(params, invalid)

                    # Apply correction
                    if gb_params is not None:
                        # Transformation by group
                        corrected[name] = \
                            corrected.groupby(**gb_params)[name] \
                                .transform(globals()[f], **fn_params)
                    else:
                        # Transformation over all column
                        #corrected[name] = \
                        #    corrected[name].transform(globals()[f], **fn_params)

                        # Faster
                        corrected[name] = globals()[f](corrected[name], **fn_params)

            # Compare
            if report_corrections:
                comparison = pd.DataFrame()
                """
                comparison = dataframe[name].compare(corrected[name])
                comparison.columns = ['original', ' corrected']
                comparison = corrected[[self.groupby_, 'date']].merge(comparison,
                        left_index=True, right_index=True)
                corrections[name] = comparison
                """

        # Return
        if report_corrections:
            return corrected, corrections
        return corrected


class SchemaCorrectionStack(SchemaCorrectorBase):

    def transform(self, dataframe, columns=None,
                  report_corrections=True, verbose=10):
        """Corrects dataset in stack format.

        .. warning: Ensure dataframe is properly sorted (e.g.
                    by patient_id and date) and sampled so that
                    methods such as ffill work as expected.

        Parameters
        ----------
        DataFrame:
            The DataFrame to correct.
        columns:
            The selected columns
        report_corrections
            Whether to report the corrections.

        Returns
        -------

        """
        if verbose > 1:
            print("\n\nApplying SchemaCorrectionStack!\n")


        invalid = {"groupby"}

        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        # Create corrections report
        corrections = {}

        # Copy DataFrame
        corrected = dataframe.copy(deep=True)

        # Ensure data is sorted! otherwise ffill might fail!

        # Features available
        if columns is None:
            columns = corrected.column.unique()

        # Loop
        for name in columns:

            # Get indexes
            idxs = corrected.column == name

            for tf_map in self.get_transformations(name):
                for f, params in tf_map.items():

                    # Logging information
                    if verbose > 5:
                        print("{0:8} {1}: Applying... {2:25} | {3:30} | {4}" \
                            .format('', self.__class__.__name__, name, f, params))

                    # Get groupby and function parameters
                    gb_params = self.get_groupby(params)
                    fn_params = without_keys(params, invalid)

                    # Apply correction
                    if gb_params is not None:
                        # Transformation by group
                        corrected.loc[idxs, 'result'] = \
                            corrected[idxs] \
                                .groupby(**gb_params).result \
                                    .transform(globals()[f], **fn_params)
                    else:
                        # Transformation whole column.
                        #corrected.loc[idxs, 'result'] = \
                        #    corrected[idxs].result \
                        #        .transform(globals()[f], **fn_params)

                        # Faster transformation
                        corrected.loc[idxs, 'result'] = \
                            globals()[f](corrected[idxs].result, **fn_params)

        # Return
        if report_corrections:
            return corrected, corrections
        return corrected