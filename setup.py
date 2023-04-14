# -*- coding: utf-8 -*-
"""
    Setup file for ewmh_m2m.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.2.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys

from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

from os import path

if __name__ == "__main__":
    links = "\n".join(
        (
            ".. _Authors: https://ewmh-m2m.readthedocs.io/en/latest/authors.html",
            ".. _Licence: https://ewmh-m2m.readthedocs.io/en/latest/license.html",
            ".. _Changelog: https://ewmh-m2m.readthedocs.io/en/latest/changelog.html",
            "",
            ".. |logo| image:: https://ewmh-m2m.readthedocs.io/en/latest/_images/ewmh_m2m.svg",
            "   :alt: Logo",
            "   :width: 500",
            "",
        )
    )

    with open(
        path.join(path.abspath(path.dirname(__file__)), "README.rst"), encoding="utf-8"
    ) as f:
        lines = f.readlines()
        start_index = lines.index(".. EndOfLinks\n")
        description_content = "".join(lines[start_index + 1 :])

    setup(
        long_description=links + description_content,
        long_description_content_type="text/x-rst; charset=UTF-8",
        use_pyscaffold=True,
    )
