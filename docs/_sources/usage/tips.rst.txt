Useful Tips
===========

Naming conventions for variables
--------------------------------

 - **General**: Use variable names to describe the data collected using
   the most meaningful word first. Try to include further description of
   the variable if possible and avoid using acronyms (unless they are very
   well known). Words should be separated by ``_``.

   .. note::
      It is very easy to sort variable names alphabetically and using
      good naming conventions will make them appear together. This will
      facilitate further inspection and validation of results.

   Example with ascites:

   .. code::

        ascites                  # boolean (presence of ascites)
        ascites_level            # number or str ([1,2,3], [Low, Medium ,High)
        ascites_description      # free-text
        ascites_interpretation   # interpretation by clinicians
        ascites_duration         # number (seconds, minutes)

   Example with bleeding:

   .. code::

        bleeding          #
        bleeding_skin     #
        bleeding_gums     #
        bleeding_mucosal  #
        bleeding_other    #


   .. code::

        shock              #
        shock_re           #
        shock_clinical     #
        shock_resucitation #


 - **Percentages**: Those laboratory results with unit expressed in percentages
   (%) have such information appended in the variable name. This is to differentiate
   when the biochemical marker is measured in percent or in another concentration
   unit (e.g. mmol/L). Note that there are many different concentration units
   that could be used.

   .. code::

        monocytes            # concentration (U/mL)
        monocytes_percent    # percentage (%)


 - **Events**: The event variables have the 'event' element prepended in the name.


   .. note:: Ensure that laboratory dates (e.g. pcr, serology, cytokines, blood, ...)
      are referring to the sample collection date or the date the laboratory result
      was presented to the clinicians. In some scenarios this information is missing
      in the datasets and other standard dates (e.g. date of enrolment or date of
      admission) have been used. Thus collecting events in this scenarios might
      lead to confusion.

   .. code::

        event_onset       # onset of diseases
        event_admission   # admitted to hospital
        event_laboratory  # sample collected for laboratory test
        event_pcr         # sample collected for pcr test
        event_serology    # sample collected for serology
        event_discharge   # discharged from hospital (alive/death?)
        event_transfer    # transferred to other unit



Considerations for stacked data
-------------------------------

Considerations for tidy data
----------------------------

The conversation from the stacked data structure to the tidy data structure, there are
a few things to consider to improve the quality of the data.

 - Filling missing values

    - **Static**: There are variables that are static and they only need to be collected
      once and remain the same through the data collection period. Some examples of this
      type of variables are ``gender``, ``age``, ``pregnancy``, ``diabetes``, ``hiv``, ...

    - **Levels**: There are variables that indicate a level with a range that usually goes
      from 0 to N. However, they are only recorded when significant presence (e.g. of pain)
      appears. Thus, we can assume that empty values have no significant presence and fill
      them with 0. Some examples of this type of variables are ``abdominal_pain_level``,
      ``joint_pain_level`` or ``cough_level``

      .. note:: Sometimes two columns are collected, one column to indicate the
                presence of pain (usually a boolean) and another column indicating
                the level (usually a number). This is redundant since the level
                already encapsulates all the information.

    - **Onset**: Sometimes the condition is recorded only with the data of onset. For
      example, nausea started on te da 21/12/2020. Thus in the data there will be only
      a True for nause on that particular day and the rest will be missing. It is up to
      the user to decide whether this should remain this way or it should be forward
      filled and therefore nause was carried out more days. It could be 2 days, 3 days
      or until the next recorded value.

    - **Events**: dates: todo date_admission date_discharge ...

    - **Merging**: Sometimes the same biomarker is collected in different ways. For example,
      the hematocrit value can be collected and recorded at the very moment but sometimes
      clinicians just record the maximum and minimum values for the day. Thus it is possible
      to merge this information and have haematocrit, haematocrit_max and haematocrit_min all
      called the same. Note that this could result in duplicated rows if all values are recorded.

