pymccusb
========

|Supported Python versions| |License|

``pymccus`` implements a Python interface for ``libmccusb``, the C library for Measurement Computing Corp (MCC) data acquisition devices. Currently implemented devices:

- USB-1208FS-Plus
- USB-1408FS-Plus

Supported Python versions: 2.7, 3.2+. Please report if you run into compatibility issues.

Prerequisites
-------------

On Debian/Ubuntu::

    sudo apt install build-essential autoconf libtool pkg-config libusb-1.0-0-dev libudev-dev

Building vendored components
----------------------------

::

    ./bootstrap

The shared libraries are installed to ``vendor/lib``. Remember to set ``LD_LIBRARY_PATH`` when using the shared libraries.

Usage
-----

No docs yet. You may check out ``examples`` in the meantime.

Issues
------

Please report issues to https://github.com/zmwangx/pymccusb/issues.


License
-------

The code base itself is licensed under MIT/Expat. See ``COPYING``.

Vendored components:

- ``Linux_Drivers/USB/mcc-libusb`` is licensed under LGPL. The rest of ``Linux_Drivers`` are licensed under GPL (version not specified), but they are not used by this project. See ``vendor/src/Linux_Drivers/README.md`` for details.

- ``hidapi`` is licensed under BSD 3-Clause. See ``vendor/src/hidapi/LICENSE-bsd.txt``.

.. |Supported Python versions| image:: https://img.shields.io/badge/python-2.7,%203.2,%203.3,%203.4,%203.5,%203.6-blue.svg?maxAge=86400
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg?maxAge=86400
