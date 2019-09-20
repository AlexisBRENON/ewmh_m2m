======================================
EWMH Compliant Move To Monitor utility
======================================

Rationale
=========

I love XFCE. I use it on almost all my computers.
However, in a multi head setup, it lacks a "move window to monitor" feature.
Some posts link to the `move-to-next-monitor`_ script, which as many dependencies and is not very customizable
(move to bottom, to right, etc.)

Hence, here it is ewmh_m2m.

Install
=======

Just install the package with pip::

    pip install ewmh_m2m

You should now have a ``move-to-monitor`` command available.

Usage
=====

Call ``move-to-monitor`` to move the active window to the next monitor.
Next versions (starting at 1.0.0) will accept some arguments:

* to define in which direction to look for the "next" (up, bottom, left, right)
* to define if you want to wrap to the previous if on last screen
* to do more things if you have more ideas (features requests are welcome)


Note
====

This project has been set up using PyScaffold 3.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.

.. _move-to-next-monitor: https://github.com/jc00ke/move-to-next-monitor
