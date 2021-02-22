==================
06dx
==================



General notes
=============


1 - As a main convention, when using variable names to describe the data collected use the main word first and then further description of the variable. Note that it is very easy to sort this variable names alphabetically and they should appear together.

	Example with ascites:

	ascites                  - boolean
	ascites_level            - number or str
	ascites_description      - number or str
	ascites_interpretation   - interpretation by clinicians
	ascites_duration         - number

	Example with shock:

	shock              -
	shock_re           -
	shock_clinical     -
	shock_resucitation -


2 - Those laboratory results with unit expressed in percent (%) have such information appended in the variable name. This is to differentiate when the biochemical marker is measured in percent or in another concentration unit (e.g. mmol/L). Note that there are many different concentration units that could be used.

	Example with monocytes:

	monocytes            - U/mL
	monocytes_percent    - %


3 - The event variables have the 'event' element prepended in the name. Note that in the configuration files some events have not been specified (e.g. event_pcr) because such the sample collection date for the PCR has not been specified in the data. Thus, it has been fixed by using the date_enrolment.

	event_onset
	event_admission
	event_laboratory
	event_pcr
	event_serology
	event_discharge
	event_transfer

Questions....
  Should I use pleural_efussion or efussion_pleural?




Worksheets
==========

HIST
----

  - feeling_faint probably better rename as feeling_dizzy

EVO
----
  - MaxTemp renamed to body_temperature (warning of duplicates)
  - MaxPulse renamed to pulse (warning of duplicates)

SUM
---
  - Ignored but might have data.

FU
--
  - Ignored but might have data.

NS1
---
  - Ignored (empty sheet).


