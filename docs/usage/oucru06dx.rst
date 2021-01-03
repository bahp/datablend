
The OUCRU-06dx case
-------------------

The folder structure for this example is as follows:

::

  oucru-06dx
      |- resources
          |- datasets
              |- 19-5-2020-CTU06DX_Data.xls (required)
              |- CTU06DX_DataDictionary.xls (optional)
          |- outputs
              |- datasets
                  |- 06dx_data_fixed.xlsx
                  |- 06dx_data_stacked.xlsx
                  |- 06dx_data_stacked_<worksheet>.csv
                  |- 06dx_data_tidy.csv
              |- templates
                  |- ccfgs_06dx_data_fixed.xlsx
                  |- tmp
                      |- ccfgs_06dx_data_fixed.xlsx
      |- automated_run.sh
      |- create_data_ccfgs.py
      |- create_data_fixed.py
      |- create_data_stacked.py
      |- create_data_tidy.py

.. warning:: The original data ``19-5-2020-CTU06DX_Data.xls`` must be located in
   the corresponding folder.

Quick run
=========

To run the example execute ``automated_run.sh``.

.. code-block::

    ./automated_run.sh

This bash script just runs the following python scripts:

.. literalinclude:: ../../examples/oucru/oucru-06dx/automated_run.sh
  :language: BASH
  :emphasize-lines: 0


Fixing the data
===============

The ``create_data_fixed.py`` script corrects some of the issues that are
found on the raw dataset for the oucru-06dx example. These are some of
the issues that have been fixed for the various OUCRU examples (06dx,
13dx, 32dx and 42dx).

 - **Missing date** column: Note that many worksheets have information but
   no date associated with it. This is a problem if one of our goals is to
   stack the data. Thus, one of the corrections is to include a datetime
   column from another worksheet (e.g. date_admission) when there is no
   datetime column present.

 - **Inconsistent Age/DoB** recording.

 - **Erroneous Time** format (24:00).

.. note:: This script creates ``06dx_data_fixed.xls``.

Creating configuration files
============================

The original data ``19-5-2020-CTU06DX_Data.xls`` contains a total of 22 worksheets
which makes the process of manually creating template configuration files quite
tedious. Luckily, ``BlenderTemplate`` has a method to auto-generate template
configuration files from data.

.. literalinclude:: ../../examples/oucru/oucru-06dx/create_data_ccfgs.py
  :language: PYTHON
  :lines: 26-37

The ``create_data_ccfgs.py`` script auto-generates a template configuration file
(see `template_raw`_) describing ``06dx_data_fixed.xls`` and saves it in a temporary
folder (``tmp``). The user needs to copy this configuration file into the main
templates folder for further revision and editing. For simplicity, a revised version
of the auto-generated template configuration file has been also included in the
example (see `template_rev`_).

.. note:: This script creates ``ccfgs_06dx_data_fixed.xls`` in the temporary ``tmp`` folder.

.. _template_raw: https://github.com/bahp/datablend/raw/main/examples/oucru/oucru-06dx/resources/outputs/templates/tmp/ccfgs_06dx_data_fixed.xlsx
.. _template_rev: https://github.com/bahp/datablend/raw/main/examples/oucru/oucru-06dx/resources/outputs/templates/ccfgs_06dx_data_fixed.xlsx

Data in stacked format
======================

The ``create_data_stacked.py`` script creates the stacked data.

.. note:: This script creates ``06dx_data_stacked.xls`` and ``06dx_data_stacked_<worksheet>.csv``.

Data in tidy format
===================

The ``create_data_tidy.py`` script creates the tidy data.

.. note:: This script creates ``06dx_data_tidy.csv``.

Further considerations
======================

The full process is logged both in the console and the ``output.log`` file. As
such, this file might contain useful information to revise and improve the
data blending process. Note that during the creation of ``06dx_data_tidy.csv``
the different variables collected for a patient (e.g. skin_rash, ascites, dbp, ...)
are grouped for each patient daily.

In the log file the duplicate values are presented (see below).

 - There are some duplications that could be justified in scenarios where various
   samples where collected for the same day (e.g. various dbp samples). Thus, it is
   up to the user to decide how to address this issue (e.g. mean) if needed.

 - However, there are other scenarios in which duplicates are not justified. This
   might be caused by mistakes made during the manual collection and or manipulation
   of data using Microsoft Excel. For instance, the skin_rash column with both
   True and False values on the same day.


    - Inconsistent **values**: Opposite values recorded on the same day. This
      are a problem since we need to identify why they are contradictory and
      decide the strategy to solve this inconsistency.
       - e.g. ascites can't True and False

    - Inconsistent **formats**: Equal values are considered duplicated due to the
      format in which they have been collected. These are not a real problem as
      it can be easily solved by just keeping the last appearance (note that all
      values are the same).
        - e.g. sbp of 120.0 (float) and 120 (int)
        - e.g. skin_rash of 0.0 (float), 0 (int) and False (boolean).


.. code-block::
   :emphasize-lines: 8-9, 12-13, 20-21

    ================================================================================
    The data size: (83313, 4)
    The following duplicates were found:

        study_no date       column
        06DXA001 2009-08-03 skin_rash                 0.0
                            skin_rash               False
        06DXA002 2009-08-07 ascites                 False
                            ascites                  True
        06DXA005 2009-08-05 body_temperature         39.0
                            body_temperature         40.0
                            dbp                      70.0
                            dbp                        80
                            petechiae                 0.0
                            petechiae                True
                            pulse                   120.0
                            pulse                     120
                            respiratory_rate         20.0
                            respiratory_rate         28.0
                            sbp                     120.0
                            sbp                       120
                            skin_rash                 1.0
                            skin_rash               False
                 2009-08-11 pcr_dengue_load      1.69E+04
                            pcr_dengue_load      6.33E+03
        ...
    ================================================================================


In addition, it is extremely useful to revise the columns created in ``06dx_data_tidy.csv``
to see whether there are features representing the same parameters with different names
(e.g. alb and albumin or abdo_pain and abdominal_pain). Note that this issue could be easily
solved by renaming them on the template configuration files.

.. code-block::
   :emphasize-lines: 8-9

    ================================================================================
    Data Source: None (2178, 115)
    Data Types:
        abdominal_pain              string
        abdominal_pain_level         Int64
        abdominal_tenderness       boolean
        age                          Int64
        alb                        Float64
        albumin                    Float64
        alt                          Int64
        aptt                       Float64
        ascites                    boolean
        ascites_level                Int64
        ast                          Int64
        bilirubin_direct           Float64
        bilirubin_total            Float64
        bladder_thickening          string
        bleeding                   boolean
        bleeding_gum                string
        ...
    ================================================================================
