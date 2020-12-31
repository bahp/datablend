# datablend README

<!-- ----------------------- -->
<!--     PROJECT SHIELDS     -->
<!-- ----------------------- -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
***
*** For more badges: http://badges.github.io/badgerbadgerbadger/
*** For more badges: https://github.com/Naereen/badges
***  Basic use: 
*** https://img.shields.io/badge/<subject>-<status>-<color?.svg
*** https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
***
-->
<!--[![Build][build-shield]][none-url]-->
<!--[![Coverage][coverage-shield]][none-url]-->
<!--[![Documentation][documentation-shield]][none-url]-->
<!--[![Website][website-shield]][none-url]-->
[![Actions Status](https://github.com/bahp/datablend/workflows/Python%20package/badge.svg)](https://github.com/bahp/datablend/actions)
[![Python][python-shield]][none-url]
[![Issues][issues-shield]][none-url]
[![MIT License][license-shield]][none-url]
[![Contributors][contributors-shield]][none-url]

<!--
[![Forks][forks-shield]][none-url]
[![Stargazers][stars-shield]][none-url]
[![MIT License][license-shield]][none-url]
-->

Community | Documentation | Resources | Contributors | Release Notes

The Datablend library aims to facilitate the formatting of manually collected data into
(i) stacked data format which is commonly used to store data in a database table and 
(ii) tidy format which is commonly used in ML libraries.

<!-- > Subtitle or Short Description Goes Here -->

<!-- > ideally one sentence -->

<!-- > include terms/tags that can be searched -->


<!-- PROJECT LOGO -->
<!--
<br />
<p align="center">
  <a href="">
    <img src="" alt="Logo" width="150" height="80">
  </a>
</p>
-->


<!-- ----------------------- -->
<!--    TABLE OF CONTENTS    -->
<!-- ----------------------- -->
## Table of Contents

* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Tests](#tests)
* [Roadmap](#roadmap)
* [License](#license)
* [Contact](#contact)
* [Utils](#utils)

<!--* [Contributing](#contributing)-->
<!--* [Versioning](#versioning)-->
<!--* [Sponsors](#sponsors)-->
<!--* [Authors](#authors)-->
<!--* [Acknowledgements](#acknowledgements)-->

<!-- ----------------------- -->
<!--    ABOUT THE PROJECT    -->
<!-- ----------------------- -->
## About the project

<!-- Add image if it is a graphical user interface -->
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

The Datablend library facilitates formatting data into stacked and/or tidy format.

<!--
### Built With

This project heavily relies on other major framework which have build most of the
algorithms and functionality. It just sits on top of them to facilitate the
evaluation and reporting of to wider audiences.

* [![Django](https://img.shields.io/badge/Django-3.0.7-blue.svg)](https://www.djangoproject.com/) 
* [![DjangoRF](https://img.shields.io/badge/djangorestframework-3.11.0-blue.svg)](https://www.django-rest-framework.org/) 
* [![DjangoIE](https://img.shields.io/badge/django_import_export-2.2.0-blue.svg)](https://django-import-export.readthedocs.io/en/latest/) 
* Others
-->

<!--
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Laravel](https://laravel.com)
-->


<!-- ----------------------- -->
<!--     GETTING STARTED     -->
<!-- ----------------------- -->
## Getting Started

### Prerequisites

### Installation

#### Creating the virtual environment

A <a href="#">virtual environment</a> is a tool that helps to keep dependencies required by different projects 
separate by creating isolated python virtual environments for them. This is one of the most 
important tools that Python developers use.

In recent versions of python we can use venv

```
  py -m pip install venv           # Install venv
  py -m venv <environment-name>    # Create environment
```

Otherwise, using standard virtualenv (linux-based systems)

```sh
  which python                                    # where is python
  pip install virtualenv                          # Install virtualenv
  virtualenv -p <python-path> <environment-name>  # create virtualenv
  source virtualenv-name/bin/activate             # activate environment
  deactivate                                      # deactivate environment
```

#### Installing in editable (develop) mode

It is recommended that you install this package in 
<a href="https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html">
develop mode</a>. It puts a "link (actually *.pth files) into the python installation
to your code, so that your package is installed, but any changes will immediately 
take effect. This way all your test code, and client code, etc, can all import your 
package the usual way.

First, lets clone the repo

```sh
  git clone https://github.com/<your-username>/datablend.git
```

Install the requirements. In the scenario of missing libraries, just install them using pip.

```sh
  py -m pip install -r requirements.txt   # Install al the requirements
```

Go to the directory where the setup.py is. Please not that although setup.py is a python
script, it is not recommended to install it executing that file with python directly. Instead
lets use the package manager pip.

```sh
  py -m pip install --editable  .         # Install in editable mode
```


<!-- ----------------------- -->
<!--     USAGE EXAMPLES      -->
<!-- ----------------------- -->
### Usage (the oucru-32dx example)

See the [documentation]() for a list of examples.

The oucru-32dx directory tree is as follows.

* oucru-32dx
    - resources
        - configuration
            - tmp
            - ccfg-EVO.csv
            - ccfg-LAB.csv
            - ccfg-PCR.csv
        - datasets
            - data.csv
        - outputs
            - 32dx-combined-books.csv
            - stacked_data_EVO.csv
            - stacked_data_EXAM.csv
            - stacked_data_PCR.csv

#### Configuring the dataset descriptor

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

Let's understand this configuration files by describing the columns?

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

#### Data transformation using the DatasetDescriptor

This script loads a spreadsheet (dataset) and all the associated
configuration files and formats the data. The output is stored in
a stacked format.

```py
python create_data_stacked.py 
```

The stacked format has the following columns.

data: str

patient: str

result: str

#### From stacked data to tidy data

This script is used to transform stacked data into tidy. In addition,
it can be used to fill missing data based on assumptions:

- static:
    There are variables that are static and they only need to be
    collected once and remain the same through the data collection
    period. Clear examples of this are gender or conditions such
    as diabetes, hiv, ... Other examples are not that clear and
    might vary depending on the length of the study (e.g. age,
    pregnancy, ...)
    
- levels:
    There are variables that indicate level. For example, the 
    level of abdominal pain. This levels tend to go between 0 and 
    a number but usually only recorded when pain appears. Thus,
    we can use this assumption to fill all missing values as 0
    (e.g. no pain). Note that sometimes two columns are collected,
    a boolean saying whether there is pain, and another column 
    indicating the level of that pain. This is redundant and only
    can be used.

- onset:
    Sometimes the condition is recorded only with the data of onset.
    For example, nausea started on te da 21/12/2020. Thus in the
    data there will be only a True for nause on that particular day
    and the rest will be missing. It is up to the user to decide
    whether this should remain this way or it should be forward 
    filled and therefore nause was carried out more days. It could
    be 2 days, 3 days or until the next recorded value.

- dates: todo
    date_admission
    date_discharge
    ...

- merging: 
    Sometimes the same biomarker is collected in different ways. For 
    example, the hematocrit value can be collected and recorded at the 
    very moment but sometimes clinicians just record the maximum and
    minimum values for the day. Thus it is possible to merge this
    information and have haematocrit, haematocrit_max and haematocrit_min
    all called the same. Note that this could result in duplicated 
    rows if all values are recorded.

#### Automated run

In order to run all the conversions easily a bash script has been
create. This script just loops through different folders and executes
the previously explained python scripts.

As summary it shows the final columns to review that all the names 
are consistent. For instance, there might be spelling errors resulting
in two columns referring to the same data with different names.



<!-- ----------------------- -->
<!--          TESTS          -->
<!-- ----------------------- -->
### Tests

This section is empty.


<!-- ----------------------- -->
<!--        ROADMAP          -->
<!-- ----------------------- -->
## Roadmap

See the [open issues]() for a list of proposed features (and known issues).


<!-- ----------------------- -->
<!--      CONTRIBUTING       -->
<!-- ----------------------- -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For more information read <a href="#">CONTRIBUTING.md</a> for details on our code of conduct and the process
for submitting pull requests to us.


<!-- ----------------------- -->
<!--         LICENSE         -->
<!-- ----------------------- -->
## License

Distributed under the GNU v3.0 License. See `LICENSE` for more information.

<!-- ----------------------- -->
<!--         CONTACT         -->
<!-- ----------------------- -->
## Contact

Bernard Hernandez - 
   - add twitter
   - add email
   - add linkedin
   - add anything

[Project Link](https://github.com/bahp/python-epicimpoc-inference)


<!-- ----------------------- -->
<!--     ACKNOWLEDGEMENTS    -->
<!-- ----------------------- -->
## Acknowledgements

<!-- ----------------------- -->
<!-- MARKDOWN LINKS & IMAGES -->
<!-- ----------------------- -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-1-yellow.svg
[forks-shield]: https://img.shields.io/badge/forks-0-blue.svg
[stars-shield]: https://img.shields.io/badge/stars-0-blue.svg
[issues-shield]: https://img.shields.io/badge/issues-3_open-yellow.svg
[license-shield]: https://img.shields.io/badge/license-GNUv0.3-orange.svg
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[product-screenshot]: images/screenshot.png

[build-shield]: https://img.shields.io/badge/build-none-yellow.svg
[coverage-shield]: https://img.shields.io/badge/coverage-none-yellow.svg
[documentation-shield]: https://img.shields.io/badge/docs-none-yellow.svg
[website-shield]: https://img.shields.io/badge/website-none-yellow.svg
[python-shield]: https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg
[pypi-package]: https://img.shields.io/badge/pypi_package-0.0.1-yellow.svg

[dependency-shield]: http://img.shields.io/gemnasium/badges/badgerbadgerbadger.svg?style=flat-square
[coverage-shield]: http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square
[codeclimate-shield]: http://img.shields.io/codeclimate/github/badges/badgerbadgerbadger.svg?style=flat-square
[githubissues-shield]: http://githubbadges.herokuapp.com/badges/badgerbadgerbadger/issues.svg?style=flat-square
[pullrequests-shield]: http://githubbadges.herokuapp.com/badges/badgerbadgerbadger/pulls.svg?style=flat-square
[gemversion-shield]: http://img.shields.io/gem/v/badgerbadgerbadger.svg?style=flat-square
[license-shield]: http://img.shields.io/:license-mit-blue.svg?style=flat-square
[badges-shield]: http://img.shields.io/:badges-9/9-ff6799.svg?

[none-url]: https://www.imperial.ac.uk/bio-inspired-technology/research/infection-technology/epic-impoc/


## Utils

### Generating distribution archives (not required)

Lets generate the <a href="https://packaging.python.org/tutorials/packaging-projects/">
distribution package</a> which contains the archives that are uploaded to the public 
Package Index (PyPI) and can be installed by anyone using pip.

First of all, make sure you have the latest versions of setuptools and wheel installed:

```shell
  py -m pip install --upgrade setuptools wheel
```

Now run this command from the same directory where setup.py is located. Note that this 
command should output a lot of text and once completed should generate two files in the 
dist directory:

    - dist/
        - package-name-version-....whl
        - package-name-version-....tar.gz


```shell
  py setup.py sdist bdist_wheel
```

### Generating the documentation with sphinx (not required)

Description of sphinx and link

First you need to install sphinx and possibly sphinx-gallery.

Go to the docs folder and run:

```shell
  make html 
```

#### Contributors (optional)
#### Support (optional)
#### FAQ (optional)
