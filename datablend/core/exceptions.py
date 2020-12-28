# Libraries.


class IncompatibleBlenderTemplateError(Exception):
    pass


class InvalidBlenderTemplateError(Exception):
    pass


class MissingRequiredColumns(IncompatibleBlenderTemplateError):
    def __init__(self):
        pass


class WrongColumnType(IncompatibleBlenderTemplateError):
    pass
