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

from setuptools import setup, find_packages


setup(
    name='python-draughts',
    version='0.1',
    license='GNU General Public License (GPL)',
    author="Yohaan Seth Nathan",
    author_email='yohaan.nathanjw@gmail.com',
    packages=find_packages('draughts'),
    package_dir={'': 'draughts'},
    url='https://github.com/TheYoBots/python-draughts',
    keywords='draughts pdn fen'
)