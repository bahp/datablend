

### Generating the documentation with sphinx (not required)

First you need to install sphinx, sphinx-gallery, sphinx-std-theme and matplotlib.
Then go to the docs folder and run:

```shell
  make html
  make github
```


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

