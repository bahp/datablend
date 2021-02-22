# Library
import numpy as np
import pandas as pd

# Libraries DataBlend
from datablend.core.consistency import range_correction
from datablend.core.consistency import order_magnitude_correction

class Corrector(object):
    pass


class InRangeCorrector(Corrector):
    """This method...
    """
    def __init__(self, low, high, value=np.nan):
        self.low = low
        self.high = high
        self.value = value

    def report(self, verbose=10):
        """"""
        msg = "   -<{0}> has {1} inconsistent values" \
            .format(self.column_, len(self.rows_))
        msg += "\n\n\tThe complete report:"
        msg += "\n\t\t{0}\n".format( \
            self.report_.to_string().replace('\n', '\n\t\t'))
        return msg

    def transform(self, series):
        """This method..."""
        # Return corrected series
        transform, idxs = range_correction(series,
            range=(self.low, self.high),
            value=self.value, return_idxs=True)

        # Save information
        self.column_ = series.name
        self.rows_ = idxs

        # Save report
        report = pd.DataFrame()
        report['original'] = series[self.rows_]
        report['corrected'] = transform[self.rows_]
        report['feature'] = self.column_
        self.report_ = report

        # Return corrected series
        return transform


class OrderMagnitudeCorrector(Corrector):

    def __init__(self, low, high, orders=[10, 100]):
        self.low = low
        self.high = high
        self.orders = orders

    def transform(self, series):
        order_magnitude_correction(series)
        import sys
        sys.exit()
        pass
        """
        # Loop
        for i in self.orders:
            aux = (series / i)
            idx = aux.between(low, high)
            transform[idx] = aux[idx]
        # Return
        return transform
        """
