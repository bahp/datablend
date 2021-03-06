Development
=============================

Generating pytest coverage
-------------------------------

.. code: pytest --cov-report html -cov datablend -- verbose

Further reading...

https://www.robinandeer.com/blog/2016/06/22/how-i-test-my-code-part-3

Generating Sphinx documentation
-------------------------------

.. note:: The numpy doc style is used thorough the code (autodocs).

First you need to install sphinx, sphinx-gallery, sphinx-std-theme and matplotlib.


Let's install the required libraries.

.. code::

  py -m pip install sphinx            # Install sphinx
  py -m pip install sphinx-gallery    # Install sphinx-gallery for examples
  py -m pip install sphinx-std-theme  # Install sphinx-std-theme CSS
  py -m pip install matplotlib        # Install matplotlib for plot examples


Then go to the docs folder and run:

.. code::

  make github


Note that make github is defined within the Makefile and it is equivalent to:

.. code::

  sphinx-apidoc -o ./_apidoc ../datablend/
  make clean html
  cp -a _build/html/. ../../gh-pages/docs



Generating distribution files
-------------------------------

Lets generate the <a href="https://packaging.python.org/tutorials/packaging-projects/">
distribution package</a> which contains the archives that are uploaded to the public
Package Index (PyPI) and can be installed by anyone using pip.

First of all, make sure you have the latest versions of setuptools and wheel installed:

.. code::

  py -m pip install --upgrade setuptools wheel


Now run this command from the same directory where setup.py is located. Note that this
command should output a lot of text and once completed should generate two files in the
dist directory:

    - dist/
        - package-name-version-....whl
        - package-name-version-....tar.gz


.. code::

  py setup.py sdist bdist_wheel



