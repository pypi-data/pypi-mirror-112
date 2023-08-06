==========
GSAToolKit
==========

|PyPI| |Python| |Downloads|

.. |PyPI| image:: https://img.shields.io/pypi/v/GSAToolKit
    :target: https://pypi.org/project/GSAToolKit
    :alt: PyPI

.. |Python| image:: https://img.shields.io/pypi/pyversions/GSAToolKit
    :target: https://pypi.org/project/GSAToolKit
    :alt: PyPI - Python Version

.. |Downloads| image:: https://img.shields.io/pypi/dm/GSAToolKit
    :target: https://pypi.org/project/GSAToolKit
    :alt: PyPI - Downloads

This is a package to mess with and get around systems.

Usage
=====

Modules on this package::

	diskInfo()
		- Default disk is the c drive. If you want to change the disk, type in the disk letter followed by a ":" e.g. diskInfo("d:")

	installPythonModule()
		- This is a function to install any python module on the local machine. e.g. installPythonModule("GSAToolKit")

	internetInfo()
		- Lists all the information about adapters and gateways attatched to the system. It is the same output as the command "ipconfig" on command prompt.

	killChrome()
		- Force kills all google chrome windows that are currently open.
	listDrives()
	listUsers()
	killNetSupport()
	performanceMonitor()
	systemInfo()
	taskManager()
	treeDrives()
