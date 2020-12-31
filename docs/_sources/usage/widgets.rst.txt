
.. _WIDGETS_PAGE:

Widgets
==========

This section explains the widgets implemented in ``DataBlend``. For full examples
of this widgets see the widget gallery.

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