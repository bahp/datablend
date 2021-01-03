Quickstart
==========

Data structure types
--------------------

There are numerous ways in which the data can be structured...

 - **Stacked data**: Data stacking involves splitting a data set up into smaller data
   files, and stacking the values for each of the variables into a single column.
   It is a type of data wrangling, which is used when preparing data for further
   analysis.

   ============ =================== ====== ====== ======
   patient_id   date                column result unit
   ============ =================== ====== ====== ======
   patient_01   2020-11-04 10:05:00 age    45     year
   patient_01   2020-11-04 13:00:00 gender Female
   patient_01   2020-11-04 14:00:00 sbp    80     mmHg
   patient_01   2020-11-04 14:00:00 wbc    5.2    k/uL
   patient_01   2020-11-04 14:00:00 hct    1.3    %
   patient_01   2020-11-05 14:00:00 wbc    5.4    k/uL
   patient_01   2020-11-05 14:00:00 hct    1.5    %
   patient_02   2020-11-15 10:05:00 age    32     year
   patient_02   2020-11-15 14:00:00 gender Male
   patient_02   2020-11-15 14:00:00 sbp    91     mmHg
   patient_02   2020-11-15 14:00:00 wbc    3.3    K/UL
   patient_02   2020-11-15 14:00:00 hct    0.5    %
   patient_03   2020-11-08 14:00:00 cre    1.1    umol/L
   ============ =================== ====== ====== ======

   .. note:: This data structure is often used in databases.

 - **Tidy data**: It is a standard way of mapping the meaning of a dataset to
   its structure. A dataset is messy or tidy depending on how rows, columns and
   tables are matched up with the observations, variables and types. In tidy data:
   Each variable forms a column. Each observation forms a row. In the example
   below the observations are the daily profiles for the patients.

   ============ ========== ====== ====== === === === ===
   patient_id   date       age    gender sbp wbc hct cre
   ============ ========== ====== ====== === === === ===
   patient_01   2020-11-04 45     Female 80  5.2 1.3
   patient_01   2020-11-05 45     Female     5.4 1.5
   patient_02   2020-11-15 32     Male   91  3.3 0.5
   patient_03   2020-11-08                           1.1
   ============ ========== ====== ====== === === === ===

   .. note:: This data structure is often required in AI/ML libraries.


Transformations
---------------

The ``BlenderTemplate`` contains the information to transform and stack
the data. These transformations are computed through the use and/or concatenation
of :ref:`WIDGETS_PAGE`. As such, the columns required to create the ``BlenderTemplate``
instance vary depending on the widgets used. An overall overview of the columns
is specified below.

 - ``from_name``: name of the column in the original data.
 - ``to_name``: name of the column in the transformed data (see).
 - ``type``: type of data (just for guidance).
 - ``timestamp``: name of the column (date) assigned to generate the stacked data.
 - ``to_replace``: transformation dictionary (see).
 - ``datetime``: whether it is a date variable.
 - ``datetime_date``: name of the column (original data) with the date part.
 - ``datetime_time``: name of the column (original data) with the time part.
 - ``study_day_col``: name of the column (transformed data) with the study day (see).
 - ``study_day_ref``: name of the column (transformed data) with the reference date.
 - ``unit``: the unit of measurement

.. note:: Different widgets require different columns.

The available widgets are:

 - ``RenameWidget``
 - ``ReplaceWidget``
 - ``DateTimeMergeWidget``
 - ``EventWidget``
 - ``DateFromStudyDayWidget``
 - ``StackWidget``
 - ``StackUnitWidget``

Examples
--------

 - Using :ref:`sphx_glr__examples_blender_plot_blender_01.py`.
 - Using :ref:`sphx_glr__examples_blender_plot_blender_02.py`.