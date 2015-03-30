#!/bin/env python3

import os
from setuptools import setup

setup(
    name = "G",
    version = "0.0.1",
    author = "Niklas Köhler",
    author_email = "niklas.koehler@posteo.de",
    description = "An interactive shell for Git",
    license = "GNU General Public License Version 2",
    package_dir = { "": "src" },
    py_modules = [ "G" ]
)
