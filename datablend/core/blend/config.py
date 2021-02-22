# Libraries
import yaml
import pandas as pd


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


class BlenderConfig:
    """Class to handle access to the .yaml file"""

    def __init__(self, filepath, curr_path=None):
        """Constructor"""
        # Read yaml configuration
        self.config = yaml.load(open(filepath, 'r'),
            Loader=yaml.FullLoader)

        # Current path
        self.curr_path = curr_path

    def add_curr_path(self, path):
        """This method returns fullpath.

        Parameters
        ----------

        Returns
        -------
        str
        """
        if self.curr_path is not None:
            return "{0}/{1}".format(self.curr_path, path)
        else:
            return path

    def filename(self, mode='stacked', add=None):
        """Creates filename from config"""
        prefix = _finditem(self.config, 'filename_prefix')
        dttype = _finditem(self.config, 'filename_%s' % mode)
        if add is None:
            return "%s_%s" % (prefix, dttype)
        return "%s_%s_%s" % (prefix, dttype, add)

    def filepath_data(self):
        return self.add_curr_path(
            self.config['datablend']
                       ['blender']
                       ['filepath_data'])

    def filepath_temp(self):
        return self.add_curr_path(
            self.config['datablend']
                       ['blender']
                       ['filepath_template'])

    def filepath_logger_config(self):
        return self.add_curr_path(
            self.config['datablend']
                       ['blender']
                       ['logger_config'])

    def filepath_datasets(self):
        """"""
        return self.add_curr_path(
            self.config['datablend']
                       ['blender']
                       ['folder_structure']
                       ['outputs']
                       ['datasets'])

    def filepath_reports(self):
        return self.add_curr_path(
            self.config['datablend']
                       ['blender']
                       ['folder_structure']
                       ['outputs']
                       ['reports'])

    def filepath_stack(self, corrected=False):
        """"""
        prefix_corr = '_corrected' if corrected else ''
        return "%s/%s_%s%s.csv" % \
               (self.filepath_datasets(),
                self.prefix('filename_prefix'),
                self.prefix('filename_stacked'),
                prefix_corr)

    def filepath_tidy(self, corrected=False):
        """"""
        prefix_corr = '_corrected' if corrected else ''
        return "%s/%s_%s%s.csv" % \
               (self.filepath_datasets(),
                self.prefix('filename_prefix'),
                self.prefix('filename_tidy'),
                prefix_corr)

    def prefix(self, name):
        return self.config['datablend'] \
                          ['blender'] \
                          ['folder_structure'] \
                          ['tags'] \
                          [name]

    def worksheets_included(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['worksheets'] \
                          ['include']

    def worksheets_excluded(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['worksheets'] \
                          ['exclude']

    def stack_index(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['stack'] \
                          ['index']

    def tidy_index(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['tidy'] \
                          ['index']

    def tidy_params(self):
        return self.config['datablend'] \
                          ['blender'] \
                          ['tidy']

    def features(self):
        return self.config['features']

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
            columns = [r['name'] for r in self.features()]

        # Create features dictionary
        features = {r['name']: r for r in self.features()}

        # Create report
        report = []

        # Loop to fill record
        for name in columns:
            # Create dictionary
            d = {'name': name}
            # Skip
            if name in features:
                record = copy.deepcopy(features[name])
                d.update(record)
                d['included'] = 'Yes'
                if 'transformations' in d:
                    d['transform'] = 'Yes'
                # Add transformations
                if 'transformations' in d:
                    t = {f: params for f, params in d['transformations'].items()}
                    d.update(t)
                    del d['transformations']

            # Append
            report.append(d)

        # Create report
        report = pd.DataFrame(report)
        report = report.drop(columns=['categories', 'range', 'code'])

        # Return
        return report