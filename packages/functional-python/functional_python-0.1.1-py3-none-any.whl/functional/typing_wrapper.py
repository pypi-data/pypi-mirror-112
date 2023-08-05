from typing import *

try: from typing import Final
except ImportError:
    # noinspection PyTypeChecker
    Final = Generic

try: from typing import final
except ImportError:
    from .predef import identity as final
