"""
Toolbox
~~~~~~~

A few simple Python utils

:copyright: (c) 2021 xezzz
:license: MIT, see LICENSE for more details.
"""



# Classes
from .object import S
from .timer import Timer
from .db import Database, Collection
from .store import Store

# functions
from .asciify import asciify
from .flatten import flatten
from .similarity import similarity
from .silent import silent, async_silent
from .log import setup_logging
from .converters import to_json, to_string