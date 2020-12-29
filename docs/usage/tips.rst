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
