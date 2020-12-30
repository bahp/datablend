# Libraries
import yaml
import logging
import logging.config


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
    # Load logging configuration
    with open(path, 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # Config logging from file.
    logging.config.dictConfig(config)

    # Create logger
    return logging.getLogger('dev')
