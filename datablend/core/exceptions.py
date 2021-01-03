# Libraries.

class IncompatibleBlenderTemplateError(Exception):
    pass


class InvalidBlenderTemplateError(Exception):
    pass


class BTNullValueError(InvalidBlenderTemplateError):
    """Error used in the BlenderTemplate.

    Not all the columns in the template have been renamed.

    Example
    -------
    ========= ============
    from_name to_name
    ========= ============
    StudyNo   study_number
    Age       age
    Gender
    Sex       sex
    ========= ============
    """
    def __init__(self, column):
        self.column = column

    def __str__(self):
        msg = "\n{0}: The BlenderTemplate column <{1}> has NULL values. "
        return msg.format(self.__class__.__name__, str(self.column))


class BTDuplicateError(InvalidBlenderTemplateError):
    """Error used in the BlenderTemplate.

    The column has duplicated values.

    .. code:
        =========
        from_name
        =========
        StudyNo
        Age
        Age
        Sex
        =========
    """
    def __init__(self, column):
        self.column = column

    def __str__(self):
        msg = "\n{0}: The BlenderTemplate column <{1}> has duplicated values."
        return msg.format(self.__class__.__name__, str(self.column))


class BTMissingRequiredColumnsError(InvalidBlenderTemplateError):
    """Error used in the BlenderTemplate.

    The required columns ['from_name', 'to_name'] are missing.
    """
    def __init__(self, missing):
        self.missing = missing

    def __str__(self):
        msg = "\n{0}: The BlenderTemplate is missing the following required columns: {1}.\n"
        return msg.format(self.__class__.__name__, str(self.missing))


class MissingRequiredColumns(IncompatibleBlenderTemplateError):
    """Error used for errors in the BlenderTemplate.

    Attributes:

    """

    def __init__(self, missing):
        self.missing = missing

    def __str__(self):
        msg = "\n{0}: The BlenderTemplate is missing the following required columns: {1}.\n"
        return msg.format(self.__class__.__name__, str(self.missing))


class WrongColumnType(IncompatibleBlenderTemplateError):
    pass


class ReplaceWidgetMapWarning(Warning):
    """Warning used for errors in the ReplaceWidget map.

    It warns if the map does not contain all the elements in the data.
    It warns if the map contains elements that do not appear in the data.


    """
    diff1_ = set()
    diff2_ = set()

    def __init__(self, key, dict_values, data_values, max_size=10):
        """Constructor.

        .. note:
            diff1_: elements of data not appearing in replace map.
            diff2_: elements of replace map not appearing in data.

        Parameters
        ----------
        key: string
            Name of the column
        dict_values: list
            List of keys in the replace map.
        data_values: list
            List of unique elements in the data.
        max_size: int
            Max number of elements over which warning should not
            be raised.

        Returns
        -------
        """
        # Attributes
        self.key = key
        self.dict_values = set(dict_values)
        self.data_values = set(data_values)
        self.max_size = max_size

        # Set information
        self.diff1_ = self.data_values - self.dict_values
        self.diff2_ = self.dict_values - self.data_values

    def _is_warning_diff1(self):
        return bool(self.diff1_) and len(self.diff1_) < self.max_size

    def _is_warning_diff2(self):
        return bool(self.diff2_) and len(self.diff2_) < self.max_size

    def is_warning(self):
        return self._is_warning_diff1() #or self._is_warning_diff2()

    def __str__(self):
        """Returns warning string."""
        msg = "\n{0}: Issue with 'to_replace' map for <{1}>.\n"

        if self.diff1_:
            msg += "\tThe map does not contain all values appearing in\n"
            msg += "\tthe data. Please ensure that this is correct. The\n"
            msg += "\tvalues are: {2}\n\n"

        if self.diff2_:
            msg += "\tThe map contains values that do not appear in the\n"
            msg += "\tdata. Please ensure that this is correct. The\n"
            msg += "\tvalues are: {3}\n"

        return msg.format(self.__class__.__name__,
                          self.key.upper(),
                          str(self.diff1_),
                          str(self.diff2_))
