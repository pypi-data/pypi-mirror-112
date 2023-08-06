The development of **wxPython** has stalled [#]_. Assuming there will be no more
binary extension packages for future minor versions of Python, **wxPython-zombie**
will provide the 64-bit binary extension package (build with Visual Studio 2019)
for MS Windows 10 and the source package to build for Linux. **wxPython-zombie**
has a ton of issues, but no more development and issue solving will be done. You
must not install **wxPython** and **wxPython-zombie** in the same environment,
both packages use the package directory ``wx``.

The build and installation on Linux was tested on Arch Linux, with just the
minimal explicit installed packages or groups linux, base, base-devel, python,
python-pip, webkit2gtk, glu and sdl2. Use the verbose and user option in pip.

The demo package of **wxPython-zombie** is included in the distribution.


Installation on MS Windows 10
-----------------------------
Using pip::

    > pip install wxpython-zombie


Build and installation on Arch Linux
------------------------------------
Using pip::

    > pip install -v --user wxpython-zombie


Start the demo
--------------
From the console::

    > wxpython-demo

..	[#] Time will tell whether or not this stall is recoverable.

