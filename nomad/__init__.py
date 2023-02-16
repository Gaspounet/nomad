#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Docstring with information
"""

# Python Core Import
from pathlib import Path
import logging.config

# Third-party Imports

# Nomad Imports
path_file = Path(__file__).parent.joinpath('logger_config.conf')
print(path_file)
logging.config.fileConfig(fname=path_file)


if __name__ == '__main__':
    pass
