.. figure:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/pysabertooth/master/docs/pics/Sabertooth2x32Big.jpg
	:target: https://www.dimensionengineering.com/products/sabertooth2x32


PySabertooth
==============


.. image:: https://img.shields.io/pypi/l/pysabertooth.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth
.. image:: https://img.shields.io/pypi/pyversions/pysabertooth.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth
.. image:: https://img.shields.io/pypi/wheel/pysabertooth.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth
.. image:: https://img.shields.io/pypi/v/pysabertooth.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth


Install
----------

::

	pip install pysabertooth

Usage
--------

.. code-block:: python

	from pysabertooth import Sabertooth

	saber = Sabertooth('/dev/tty.usbserial', baudrate=115200, address=128, timeout=0.1)

	# drive(number, speed)
	# number: 1-2
	# speed: -100 - 100
	saber.drive(1, 50)
	saber.drive(2, -75)
	saber.stop()


MIT License
-------------

**Copyright (c) 2017 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
