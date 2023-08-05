from collections import namedtuple

__title__ = 'functional-python'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2019 Peter Zaitcev'
__version__ = '0.1.1'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(*__version__.split('.'), releaselevel='alpha', serial=0)

from .containers import *
from .final import *
from .monads import *
from .predef import *

from .anyval import *
from .option import *

__all__ = \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
    *containers.__all__,
    *final.__all__,
    *monads.__all__,
    *predef.__all__,
    *anyval.__all__,
    *option.__all__,
]
