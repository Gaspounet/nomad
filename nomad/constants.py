#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Docstring with information
"""

# Python Core Import
from enum import Enum
from enum import unique
from types import DynamicClassAttribute

# Third-party Imports

# nomad Imports
from .pkg_info import __version__ as _v


class VersionEnum(Enum):
    """
    Current framework version.
    """
    VERSION = _v
    MAJOR = int(_v.split('.')[0])
    MINOR = int(_v.split('.')[1])
    PATCH = int(_v.split('.')[2])


class ColorEnum(Enum):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.color = (red, green, blue)

    @DynamicClassAttribute
    def value(self) -> tuple:
        return super().value


class NodeStatus(ColorEnum):
    """
    Different statuses and colors
    """
    IDLE = (150, 150, 150)
    WORKING = (127, 127, 0)
    COMPLETE = (0, 127, 0)
    ERROR = (200, 0, 0)
    DISABLED = (50, 0, 0)


class PortType(ColorEnum):
    """
    Type to Color association
    """
    EXEC = (127, 127, 127)
    INT = (255, 0, 0)
    FLOAT = (127, 127, 0)
    STRING = (0, 255, 0)
