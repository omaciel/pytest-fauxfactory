# -*- encoding: utf-8 -*-
"""Setup file for the plugin."""
from setuptools import setup

setup(
    name='pytest-fauxfactory',
    version='1.0.1',
    author='Og Maciel',
    author_email='omaciel@ogmaciel.com',
    description='Integration of fauxfactory into pytest.',
    license='GPLv3',
    keywords='pytest',
    url='https://github.com/omaciel/pytest-fauxfactory',
    py_modules=['pytest_fauxfactory'],
    install_requires=['pytest>=3.2', 'fauxfactory'],
    extras_require={
        'dev': [
            'coveralls',
            'flake8',
            'pytest-cov',
            'pytest-xdist',
            'twine',
            'wheel',
        ]
    },
    entry_points={'pytest11': ['fauxfactory = pytest_fauxfactory']},
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Unix Shell'
    ]
)
