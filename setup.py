#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W6005,W6100
from __future__ import absolute_import, print_function

import os
import re
import sys

from setuptools import find_packages, setup


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

VERSION = get_version("theming", "__init__.py")

if sys.argv[-1] == "tag":
    print("Tagging the version on GitHub:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

base_path = os.path.dirname(__file__)

README = open(os.path.join(base_path, "README.rst")).read()
CHANGELOG = open(os.path.join(base_path, "CHANGELOG.rst")).read()
REQUIREMENTS = open(os.path.join(base_path, 'requirements', 'base.txt')).read().splitlines()

setup(
    name="djangotheming",
    version=VERSION,
    description="""Complete solution for theming your django site.""",
    long_description=README + "\n\n" + CHANGELOG,
    author="Saleem Latif",
    author_email="saleem_ee@hotmail.com",
    url="https://github.com/saleem-latif/djangotheming",
    packages=[
        "theming",
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="GPL 3.0",
    zip_safe=False,
    keywords="Django Theming",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
)
