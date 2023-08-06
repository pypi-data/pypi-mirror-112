# -*- coding: utf-8 -*-
#
# This file is part of the python-draughts library.
# Copyright (C) 2010-2018 ImparaAI https://impara.ai (MIT LICENSE)
# Copyright (C) 2021- TheYoBots (Yohaan Seth Nathan)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import io
import setuptools

def read_description():
  description = io.open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read()
  return description

setuptools.setup(
    name="python-draughts",
    version="0.3",
    author="Yohaan Seth Nathan",
    author_email="yohaan.nathanjw@gmail.com",
    description="A Python3 library that you can use to play a game of draughts.",
    long_description= read_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheYoBots/python-draughts",
    project_urls={
        "Bug Tracker": "https://github.com/TheYoBots/python-draughts/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "draughts"},
    packages=setuptools.find_packages(where="draughts"),
    python_requires=">=3",
)