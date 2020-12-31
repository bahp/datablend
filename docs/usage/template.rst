Template
==========Let's understand this configuration files by describing the columns?

from_name: str
    Refers to the name of the column in the original dataset.

to_name: str
    Refers to the name of the column in the formatted dataset.

type: str
    Indicates the type of the column (serves as guidance).

to_replace: dict-like
    These dictionaries indicate the values that need to be replaced from
    the original dataset into the formatted one. For instance, if the
    original dataset used the following coding system (1 is True, 2 False)
    the dictionary would be {True: 1, False: 2}. Note that strings should
    be quoted (e.g. {'Positive': 1, 'Negative': 2, 'Equivocal': 3). It
    is also possible to include None (e.g. {True: 1, False: 2, None: 3})

datetime: boolean
    Indicates whether the features is a datetime. It is redundant because
    type includes the datetime64[ns] type. The aim of the datetime information
    is to combine columns containing date and time information
    separately.

datetime_date
    Refers to the from_name of the column with the date information.

datetime_time
    Refers to the from_name of the column with the time information.



In order to transform the data, we use a DatasetDescriptor. This object
contains all the information describing the data and the transformations
that need to be applied. In order to configure the DatasetDescriptor we
need a configuration file. The datablend library has a method to ease
this process by automatically creating configuration files from raw datasets.

Let's create the configuration files.

```py
python create_ccfgs.py
```

This script creates a single configuration file for each of the books within
the excel spreadsheet. Note that all of them are stored within the tmp folder
because these configuration files will need further revision/editing.


#### Aut