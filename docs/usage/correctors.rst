Correctors
==========

Explanation...



List of correctors
------------------

The following generic correctors are available:

 ======================================================================== ==================
 :meth:`~datablend.core.repair.correctors.dtype_correction`               ``OK``
 :meth:`~datablend.core.repair.correctors.range_correction`               ``OK``
 :meth:`~datablend.core.repair.correctors.order_magnitude_correction`     ``OK``
 :meth:`~datablend.core.repair.correctors.replace_correction`             ``OK``
 :meth:`~datablend.core.repair.correctors.categorical_correction`         ``OK``
 :meth:`~datablend.core.repair.correctors.fillna_correction`              ``OK``
 :meth:`~datablend.core.repair.correctors.static_correction`              ``OK``
 :meth:`~datablend.core.repair.correctors.unique_true_value_correction`   ``OK``
 :meth:`~datablend.core.repair.correctors.causal_correction`              Not implemented
 :meth:`~datablend.core.repair.correctors.date_outliers_correction`       Needs testing
 :meth:`~datablend.core.repair.correctors.compound_feature_correction`    ``OK (not .yaml)``
 :meth:`~datablend.core.repair.correctors.bool_level_correction`          ``OK (not .yaml)``
 ======================================================================== ==================


How to use this correctors?
---------------------------

Well, using this correctors is quite simple!

 - :ref:`sphx_glr__examples_correctors_plot_correction_stack.py`.
 - :ref:`sphx_glr__examples_correctors_plot_correction_tidy.py`.

Anyways, lets follow this small tutorial.

Lets assume we have the following dataset in tidy structured format.

.. code::

             id        date   age     bt  gender  pregnant
    0  32dx-001  2020/12/05    32   7.20    Male     False
    1  32dx-002  2020/12/05     4  38.95  Female      True
    2  32dx-002  2020/12/06  <NA>   <NA>    <NA>      <NA>
    3  32dx-002  2020/12/07  <NA>   <NA>    <NA>      <NA>
    4  32dx-003  2020/12/05  <NA>   <NA>    <NA>      <NA>
    5  32dx-004  2020/12/04  <NA>   <NA>    <NA>      <NA>
    6  32dx-004  2020/12/05  <NA>  36.50    <NA>      <NA>
    7  32dx-004  2020/12/06  <NA>   <NA>    <NA>      <NA>
    8  32dx-004  2020/12/08  <NA>   3950    <NA>      <NA>

Now, lets create a ``corrector.yaml`` file with the transformations. The
file should look as the one shown below were transformations is a list
with the name of the transformation and the parameters to pass to the
function.

.. note:: The ``groupby`` allows us to apply the correction functions to
          sub-groups of data. As an example, we can apply the transformations
          for each ``patient`` independently by grouping the data using the
          patient id.

.. code::

    corrector:
      groupby:
        patient:
          by: [id]

    features:

      - name: age
        transformations:
          - dtype_correction: {dtype: Float64}
          - range_correction: {range: [0, 120]}
          - replace_correction: {to_replace: {}}
          - static_correction: {method: max, groupby: patient}

      - name: gender
        categories:
          - Male
          - Female
        transformations:
          - static_correction: {method: mode, groupby: patient}

      - name: pregnant
        transformations:
          - dtype_correction: {dtype: boolean}
          - static_correction: {method: max, groupby: patient}
          - fillna_correction: {value: False}

      - name: bt
        transformations:
          - dtype_correction: {dtype: Float64}
          - order_magnitude_correction:
              range: [35, 43]
              orders: [10, 100]
          - range_correction: {range: [35, 43]}

Lets instantiate ``SchemaCorrectionTidy`` passing ``corrector.yaml`` as argument.

.. code::

     # Create schema corrector
     schema_corrector = \
         SchemaCorrectionTidy(filepath=filepath)

     # Correct schema
     corrected, report = \
         schema_corrector.transform(transform)

And voila, your data has been corrected.

What if we have stack structured data format? Well... pretty much the same.

.. code::

     # Create schema corrector
     schema_corrector = \
         SchemaCorrectionStack(filepath=filepath)

     # Correct schema
     corrected, report = \
         schema_corrector.transform(transform)


And the specific for OUCRU?
---------------------------

The following correctors have implemented for OUCRU specific purposes:

 - :meth:`~datablend.core.repair.correctors.oucru_bleeding_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_outcome_death_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_parental_fluid_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_pcr_dengue_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_pleural_effusion_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_shock_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_gender_pregnant_correction`
 - :meth:`~datablend.core.repair.correctors.oucru_correction`: Applies all.

These cannot be included in the .yaml because they are specific to OUCRU. In fact,
they assume that certain columns are present in the dataset passed. For this reason, at
the moment are quite experimental. Once we identify similar patterns between
different correctors, we will implement more generic correctors.

.. warning:: These methods only work for ``tidy`` structure data at the moment.

The :meth:`~datablend.core.repair.correctors.oucru_correction` method applies
all the OUCRU correctors to the data.

.. code::

    corrected = oucru_correction(dataset)