# Libraries
import re
import ast
import yaml
import json
import copy
import logging
import numpy as np
import pandas as pd
import logging.config

# Specific
from pathlib import Path

# Own libraries
from datablend.utils.pandas import save_xlsx
from datablend.utils.pandas import save_df_dict
from datablend.core.blend.config import BlenderConfig
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.tidy import TidyWidget
from datablend.core.repair.correctors import oucru_correction
from datablend.core.repair.schema import SchemaCorrectionStack
from datablend.core.repair.schema import SchemaCorrectionTidy

# Configure logger
logger = logging.getLogger('dev')


class Blender:
    """This method..."""
    templates = {}
    bc = None

    def __init__(self, widgets=[], filepath=None,
                                   curr_path=None,
                                   verbose=0):
        """Constructor"""
        self.widgets = widgets
        if filepath is not None:
            self.bc = BlenderConfig(filepath, curr_path)

    def _fit_from_config(self):
        """This method fits the blender.

        It gets the templates path from the blender configuration
        file (corrector.yaml) and fits the blender with all the
        templates.

        .. note: All the informations needs to be appropriately
                 defined in a yaml configuration file. See an
                 example at:
        """
        # Get filepath
        filepath = self.bc.filepath_temp()

        # Read templates
        templates = pd.read_excel(filepath,
            sheet_name=None)

        # Fit
        return self.fit(templates)

    def _stack_from_config(self, clean=True):
        """This methods stacks from config file.

        .. note: All the information needs to be appropriately
                 defined in a yaml configuration file. See an
                 example at:

        These are the steps:
            1. Read the raw data.
            2. Compute transformations.
            3. Stack the data.
            4. Save it in a flat .csv
            5. Save it in a xlsx with worksheets
            6. Return stacked data.
        """
        # Get filepath
        filepath = self.bc.filepath_data()

        # Read data
        data = pd.read_excel(filepath,
            sheet_name=None)

        # Transform data
        data = self.transform(data,
            include=self.bc.worksheets_included(),
            exclude=self.bc.worksheets_excluded())

        # Stack data
        stacked = self.stack(data,
            index=self.bc.stack_index(),
            include=self.bc.worksheets_included(),
            exclude=self.bc.worksheets_excluded())

        # Save all worksheets together in one csv file.
        save_df_dict(stacked,
            filepath=self.bc.filepath_datasets(),
            filename=self.bc.filename(mode='stacked', add='flat'),
            extension='csv', flat=True, index=False)

        # Save all worksheets separated in same xlsx file.
        save_df_dict(stacked,
            filepath=self.bc.filepath_datasets(),
            filename=self.bc.filename(mode='stacked'),
            extension='xlsx', index=False)

        # No need to clean the data
        if not clean:
            return stacked

        # Return
        return stacked

    def _tidy_from_config(self, verbose=10):
        """This method creates tidy data from config file.

         .. note: All the information needs to be appropriately
             defined in a yaml configuration file. See an
             example at:

         These are the steps:
             1. Read the raw data.
             2. Compute transformations.
             3. Stack the data.
             4. Save it in a flat .csv
             5. Save it in a xlsx with worksheets
             6. Return stacked data.
        """
        # Parameters
        filepath = self.bc.filepath_stack(corrected=True)

        # Read stacked data
        stack = pd.read_csv(filepath,
            parse_dates=['date'])

        if verbose > 1:
            print("\n\nConverting to tidy format!")

        # Create tidy data
        widget = TidyWidget(index=self.bc.tidy_index())

        # Set only the date and not the time.
        stack.date = stack.date.dt.date

        # Transform
        tidy, duplicated = \
            widget.transform(stack, report_duplicated=True)

        # Return
        return tidy, duplicated

    def fit(self, info=None):
        """Fits the blender.

        Parameters
        ----------
        info: pd.DataFrame or dict-like
            Template to fit in either pd.DataFrame format or a
            dictionary where key is the sheet name and the value
            is the pd.DataFrame.
        """
        # Ensure that it is a dictionary
        if not isinstance(info, dict):
            info = {'ROOT': info}

        # For each sheet create template
        for k, df in info.items():
            self.templates[k] = BlenderTemplate().fit(df)

        # Return
        return self

    def transform(self, data, include=None, exclude=None, verbose=10):
        """Transforms the data according to a template.

        .. note: The result is in the same format as the parameter data.
        .. note: If same column passed in include and exclude, by default
                 such column will be excluded. It would be possible to
                 show a warning.

        .. todo: Only process sheets with existing templates[k] and
                 raise/log warnings otherwise.

        Parameters
        ----------
        data: pd.DataFrame or dict-like
            Data to transform in either pd.DataFrame format or a
            dictionary where key is the sheet name and the value
            is the pd.DataFrame.

        include: list of str
            Name of sheets to be included.

        exclude: list of str
            Name of sheets to be excluded

        Returns
        -------
        """
        if verbose > 1:
            print("\n\nTransforming excel sheets!\n")

        # Copy data
        aux = data

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Transform
        for k, df in aux.items():
            # Exclude sheet
            if k not in include:
                continue

            # Show information
            print("{0:8} Transforming sheet <{1}>... COMPLETED.".format('', k))

            # Apply all widgets.
            for w in self.widgets:
                df = w.fit_transform(self.templates[k], df)

            # Assign df
            aux[k] = df

        if isinstance(data, pd.DataFrame):
            return aux['ROOT']

        return aux

    def fit_transform(self, data):
        pass

    def stack(self, data=None, index=None, include=None,
              exclude=None, verbose=10):
        """Stacks the data.

        .. todo: Warn skipped sheets?
        .. todo: This method could go within the StackWidget.
        .. todo: Stack widget by default unit=True. If unit
                 is true look for unit and if it exists in the
                 template then include StackUnitWidget. If no
                 unit then raise warning. If unit=False ignore
                 unit.
        """
        if verbose > 1:
            print("\n\nStacking excel sheets!\n")

        # Copy data
        aux = copy.deepcopy(data)

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Stacked data
        stacked = {}

        # Transform
        for k, df in aux.items():
            # Exclude current sheet
            if not k in include:
                continue

            # Show information
            print("{0:8} Stacking sheet <{1}>... COMPLETED.".format('', k))

            # Import (importing this library in other places crashes)
            from datablend.core.widgets.stack import StackWidget

            # It no unit then with unit equal False, or create empty or something

            # Stack
            stacked[k] = StackWidget(index=index).fit_transform(self.templates[k], df)

        # Return DataFrame
        if isinstance(data, pd.DataFrame):
            return stacked['ROOT']

        # Return dict of DataFrames
        return stacked

    def tidy(self, data, index, include=None, exclude=None):

        # Copy data
        aux = copy.deepcopy(data)

        # Create dictionary
        if isinstance(data, pd.DataFrame):
            aux = {'ROOT': data}

        # Check include and exclude
        if include is None:
            include = aux.keys()
        if exclude is not None:
            include = set(include) - set(exclude)

        # Stacked data
        tidied= {}

        # Transform
        for k, df in aux.items():
            # Exclude current sheet
            if not k in include:
                continue

            # Logging information
            logger.info("Tidying sheet <{0}>... COMPLETED.".format(k))

            from datablend.core.widgets.tidy import TidyWidget

            # Create widget
            #tidied[k] = TidyWidget(index=index).fit_transform(self.templates[k], df)
            tidied[k] = TidyWidget(index=index).transform(df)

        # Return DataFrame
        if isinstance(data, pd.DataFrame):
            return tidied['ROOT']

        # Return dict of DataFrames
        return tidied

    def fit_stack(self):
        pass

    def fit_stack_tidy(self):
        pass

    def save(self, filepath):
        """

        .. todo: bad name and not very intuitive...

        :param filepath:
        :return:
        """
        # Save resources_artificial
        path = Path(filepath)
        path.mkdir(parents=True, exist_ok=True)

        aux = {k:v.df for k,v in self.templates.items()}

        save_xlsx(aux, filepath+'/ccfg.xlsx')

    def load(self):
        pass