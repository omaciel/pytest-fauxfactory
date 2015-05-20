#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#   Author(s): Milan Falesnik   <milan@falesnik.net>
#                               <mfalesni@redhat.com>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from setuptools import setup

setup(
    name="pytest-fauxfactory",
    version="1.0",
    author="Milan Falešník",
    author_email="milan@falesnik.net",
    description="Integration of fauxfactory into pytest.",
    license="GPLv3",
    keywords="pytest",
    url="https://github.com/mfalesni/pytest-fauxfactory",
    py_modules=['pytest_fauxfactory'],
    install_requires=['pytest', 'fauxfactory'],
    entry_points={'pytest11': ['pytest_fauxfactory = pytest_fauxfactory']},
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Unix Shell"
    ]
)
