# -*- encoding: utf-8 -*-
"""Setup file for the plugin."""
import codecs
import os

from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    filename = os.path.join(*paths)
    with codecs.open(filename, mode='r', encoding='utf-8') as handle:
        return handle.read()


LONG_DESCRIPTION = (read('README.rst') + '\n\n' +
                    read('AUTHORS.rst') + '\n\n' +
                    read('HISTORY.rst'))


setup(
    name='pytest-fauxfactory',
    version='1.1.0',
    author='Og Maciel',
    author_email='omaciel@ogmaciel.com',
    description='Integration of fauxfactory into pytest.',
    long_description=LONG_DESCRIPTION,
    license='GPLv3',
    keywords='pytest',
    url='https://github.com/omaciel/pytest-fauxfactory',
    packages=['pytest_fauxfactory'],
    install_requires=['pytest>=3.2', 'fauxfactory'],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'pytest-xdist',
            'twine',
            'wheel',
        ]
    },
    entry_points={'pytest11': ['fauxfactory = pytest_fauxfactory.plugin']},
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
    ],
    test_suite='tests',
)
