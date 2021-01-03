"""

.. note: The libraries are within the method so that they are only
         imported if the method is called. Note that this method is
         only used in some examples but it is not part of the main
         library.

         It still appears in many other scripts!

         If we don't do this, this library will be required by default.

"""


def load_logger(path):
    """This method loads the logger

    Parameters
    ----------
    path: str-like
        Path to the YAML configuration file.

    Returns
    -------
    Logge
    """
    # Import
    import yaml
    import logging
    import logging.config

    # Load logging configuration
    with open(path, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # Config logging from file.
    logging.config.dictConfig(config)

    # Create logger
    return logging.getLogger('dev')
