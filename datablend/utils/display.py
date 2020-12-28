# Libraries
import pandas


def str_data_types(data):
    """This method..."""
    s = "=" * 80 + "\n"
    s += "Date Types:\n\n"
    s += str(data.convert_dtypes().sort_index().dtypes)
    s += "\n\n"
    s += "=" * 80 + "\n"
    return s


def str_dtypes(data, label=None):
    """Returns str with the dtypes"""
    # Create string
    s = "=" * 80
    s += "\nData Source: {0} {1}".format(label, data.shape)
    s += "\nData Types:"
    s += "\n\t{0}\n".format(data.convert_dtypes()
                           .dtypes.sort_index()
                           .to_string().replace('\n', '\n\t'))
    s += "=" * 80
    # Return
    return s
