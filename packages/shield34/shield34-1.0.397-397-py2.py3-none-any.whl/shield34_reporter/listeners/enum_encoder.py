from enum import Enum
from json import JSONEncoder


_saved_default = JSONEncoder().default  # Save default method.


def _new_default(obj):
    if isinstance(obj, Enum):
        return obj.name  # Could also be obj.value
    else:
        return _saved_default


JSONEncoder.default = _new_default
# Set new default method.
