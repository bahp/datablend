Installation
============

Prerequisites
-------------

Note that this library will need the following libraries. Most of the
libraries are included in the requirements.txt file and will be installed
by following this tutorial. Yet a few libraries are only required to
create the documentation, coverage or package testing and therefore might
not be required by default.

- ``pandas``
- ``pytest`` (testing)
- ``pytest-cov`` (testing)
- ``pyyaml`` (logging purposes)
- ``xlrd`` (working with excel files)
- ``xlsxwriter`` (working with excel files)
- ``openpyxl`` (working with excel files)
- ``sphinx`` (documentation)
- ``sphinx-gallery`` (documentation)
- ``sphinx-rtd-theme`` (documentation)
- ``matplotlib`` (plotting and documentation)


Creating the virtual environment
--------------------------------

A virtual environment is a tool that helps to keep dependencies required by
different projects separate by creating isolated python virtual environments
for them. This is one of the most important tools that Python developers use.

In recent versions of python we can use venv

.. code::

  py -m pip install venv           # Install venv
  py -m venv <environment-name>    # Create environment

Otherwise, using standard virtualenv (linux-based systems)

.. code::

  which python                                    # where is python
  pip install virtualenv                          # Install virtualenv
  virtualenv -p <python-path> <environment-name>  # create virtualenv
  source virtualenv-name/bin/activate             # activate environment
  deactivate                                      # deactivate environment

Installation in editable mode
-------------------------------

It is recommended that you install this package in editable (develop) mode. It
puts a link (actually \*.pth files) into the python installation to your code,
so that your package is installed, but any changes will immediately take effect.
This way all your test code, and client code, etc, can all import your package
the usual way.

First, lets clone the repo

.. code::

  git clone https://github.com/<your-username>/datablend.git

Install the requirements. In the scenario of missing libraries, just install
them using pip.

.. code::

  py -m pip install -r requirements.txt   # Install al the requirements

Go to the directory where the setup.py is. Please not that although setup.py
is a python script, it is not recommended to install it executing that file
with python directly. Instead lets use the package manager pip.

.. code::

  py -m pip install --editable  .         # Install in editable mode