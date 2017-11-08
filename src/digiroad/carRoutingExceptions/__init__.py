class IncorrectGeometryTypeException(Exception):
    """
    The input json file must be a multipoint geometry type, in case the file do not accomplish with the geometry type
    then the application throw this exception.
    """

    def __init__(self, message):
        super(IncorrectGeometryTypeException, self).__init__(message)


class NotURLDefinedException(Exception):
    """
    In case the arguments do not have an URL defined,
    the application throw this exception
    """
    pass


class NotWFSDefinedException(Exception):
    """
    The exception is thrown if there is not any WFS service defined to retrieve the features.
    """
    pass
