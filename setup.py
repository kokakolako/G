#!/bin/env python3

import os
from setuptools import setup

from G.config import version

setup(
    name = "G",
    version = version(),
    author = "Niklas Köhler",
    author_email = "niklas.koehler@posteo.de",
    description = "An interactive shell for Git",
    license = "LICENSE.txt",
    packages = [ "G" ],
    include_package_data = True,
    scripts = [ "G.py" ]
)
