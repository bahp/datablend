
.. _WIDGETS_PAGE:

Widgets
==========

This section explains the widgets implemented in ``DataBlend``. For full examples
of this widgets see the widget gallery. In addition, the table below summarises the
columns that must appear in the previously defined ``BlenderTemplate`` for each of
the implemented Widgets.

============= ====== ======= ============= ===== ================ =====
Column        Rename Replace DateTimeMerge Event DateFromStudyDay Stack
============= ====== ======= ============= ===== ================ =====
from_name      x
to_name        x        x       x           x        x
type
to_replace              x
datetime
datetime_date                    x
datetime_time                    x
event                                       x
study_day_col                                          x
study_day_ref                                          x
timestamp                                                          x
unit                                                               x
============= ====== ======= ============= ===== ================ =====


RenameWidget
------------

The ``RenameWidget`` renames columns.

.. note:: Requires:
    - ``from_name``
    - ``to_name``.


ReplaceWidget
-------------

The ``ReplaceWidget`` renames columns.

.. note:: Requires ``to_name`` and ``to_replace``.

MergeDateTimeWidget
-------------------

The ``MergeDateTimeWidget`` renames columns.

.. note:: Requires ``to_name``, ``datetime_date`` and ``datetime_time``.

EventWidget
-----------

The ``EventWidget`` renames columns.

.. note:: Requires ``to_name``, ``event``.

DateFromStudyDayWidget
----------------------

The ``DateFromStudyDayWidget`` renames columns.

.. note:: Requires ``to_name``, ``study_day_col`` and ``study_day_ref``.

Formatting to stacked data
--------------------------

The ``StackWidget`` renames columns.

.. note:: Requires ``to_name`` and ``timestamp``.

Formatting stacked data unit
----------------------------

The ``StackUnitWidget`` renames columns.

.. note:: Requires ``to_name``, ``unit``.