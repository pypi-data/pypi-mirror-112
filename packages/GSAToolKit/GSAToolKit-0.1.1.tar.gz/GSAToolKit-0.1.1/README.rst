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

    adminDetails()
        - Lists information about
          all admin accounts.

    commandPrompt()
        - Runs any command that can be
          ran on a normal command prompt
          e.g. commandPrompt("ipconfig").

    diskInfo()
        - Default disk is the c drive.
          If you want to change the disk,
          type in the disk letter followed
          by a ":" e.g. diskInfo("d:").

    forkBomb()
        - Opens internet explorer to lag
          out a system. Default value is
          100 but can be changed
          by inputting a integer
          e.g. forkBomb(8943)

    folderBomb()
        - Creates random empty folders to
          fill up a directory. Default
          value is 100 but can be changed
          by inputting a integer
          e.g. folderBomb(87925)

    installPythonModule()
        - This is a function to install
          any python module on the local
          machine. e.g.
          installPythonModule("GSAToolKit")

    internetInfo()
        - Lists all the information about
          adapters and gateways attached
          to the system. It is the same
          output as the command "ipconfig"
          on command prompt.

    killChrome()
        - Force kills all google chrome
          windows that are currently open.

    listDrives()
        - Lists all shown and hidden
          drive letters that are attached
          to the machine.

    listUsers()
        - Lists all users that have ever
          logged on to the machine and
          the date/time that they last
          logged on.

    killNetSupport()
        - Checks if NetSupport is running
          and kills it if it is. If you
          want to continually kill it and
          prevent it from starting, use
          the code:

          while True:
            killNetSupport()

    performanceMonitor()
        - Opens windows performance
          monitor if it is blocked on
          your system.

    systemInfo()
        - Lists all information that
          is provided using the "systeminfo"
          command in command prompt.

    taskManager()
        - Displays all process names and
          ID's for every process currently
          running on the system.

    treeDrives()
        - Lists all directories and files
          on any drive. Default is the c
          drive but can be changed to any
          drive e.g. treeDrives("d:").

