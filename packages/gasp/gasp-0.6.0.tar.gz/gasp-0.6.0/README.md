GASP (Graphics API for Students of Python)
==========================================

GASP is built on Tkinter and Pygame graphics. It was not written from scratch but was instead derived directly
from the Livewires library, and is thus released under the same free software
license covering the original source:

  https://github.com/livewires/python

GASP has been ported to Python 3.

GASP is designed to enable absolute beginners to write 1980's
style arcade games as an introduction to python.

Homepage: https://codeberg.org/GASP/GASP_Code 

There is an excellent coursebook <http://openbookproject.net/pybiblio/gasp/>
which goes over learning to use GASP in your own applications.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

INSTALLATION
------------

GASP should be available in PyPI. To install it:

    $ python3 -m pip install gasp
    
To also obtain the GASP games extension:

    $ python3 -m pip install gasp[games]

USAGE
-----

GASP for beginners is built on Tkinter and is meant to be imported using:

```python
from gasp import *
```

GASP games is built on Pygame and is meant to be imported using:

```python
from gasp import games
```

Because of this, to reference anything in beginners GASP, you can simply reference that object e.g. `begin_graphics()`.
However, to reference an object in GASP games, you must preface it with `games.` e.g. `games.Screen()`

TESTS
-----

The `tests` directory contains tests for GASP. For API level functional tests,
from inside the same directory where this README file is located, run:

GASP API test:

    $ python3 -m doctest tests/test_gasp_api.rst
    
GASP games API test:

    $ python3 -m doctest tests/test_games_api.rst
    
If your terminal is empty after running these commands, rest easy knowing GASP is perfect.

To visually inspect the graphics rendering, run:

    $ python3 tests/test_graphics.py


LICENSE
-------

This software is licensed under the [GPL License](LICENSE.txt) found in this
distribution.


#### REQUIREMENTS

GASP using Tkinter is designed to not require any further installations, so nothing beyond the Python Standard Library (<https://docs.python.org/3/library/index.html>) is needed.
However, GASP using Pygame requires the installation of Pygame. Please see the documentation for guidance on how to do that. 

