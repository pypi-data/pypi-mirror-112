#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) EXPE. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

"""
    setup
    =====

    A Python API for interacting with GoogleSheet

    :copyright: © 2020 by the EXPE.
    :license: MIT License
"""

import codecs
import os
import platform

from setuptools import (
    find_packages,
    setup,
)

py_version = platform.python_version()

f = codecs.open('version', 'r', 'utf-8-sig')
line = f.readline()
f.close()
PACKAGE_VERSION = str(line)

EXTRAS_REQUIRE = {
    'tester': [
        'coverage',
        'pep8',
        'pyflakes',
        'pylint',
        'pytest-cov'
    ],

    'docs': [
        "mock",
        "sphinx-better-theme>=0.1.4",
        "click>=5.1",
        "configparser==3.5.0",
        "contextlib2>=0.5.4",
        "py-solc>=0.4.0",
        "pytest>=2.7.2",
        "sphinx",
        "pdoc3",
        "sphinx_rtd_theme>=0.1.9",
        "toposort>=1.4",
        "urllib3",
        "wheel >= 0.31.0"
    ],

    'dev': [
        "bumpversion",
        "flaky>=3.3.0",
        "hypothesis>=3.31.2",
        "pytest>=3.5.0,<4",
        "pytest-mock==1.*",
        "pytest-pythonpath>=0.3",
        "pytest-watch==4.*",
        "pytest-xdist==1.*",
        "setuptools>=38.6.0",
        "tox>=1.8.0",
        "twine >= 1.11.0",
        "tqdm",
        "when-changed"
    ]

}

EXTRAS_REQUIRE['dev'] = (
        EXTRAS_REQUIRE['tester'] +
        EXTRAS_REQUIRE['docs'] +
        EXTRAS_REQUIRE['dev']
)

install_requires = [
    "bs4",
    "requests>=2.16.0,<3.0.0",
    "base58",
    'attrdict',
]

this_dir = os.path.dirname(__file__)
readme_filename = os.path.join(this_dir, 'README.md')

with open(readme_filename) as f:
    PACKAGE_LONG_DESCRIPTION = f.read()

setup(
    name='googlesheettranslate',
    version=PACKAGE_VERSION,
    description='Non credential proved url scrapper for google sheet',
    long_description=PACKAGE_LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords='google sheet cli sdk',
    url='https://gitee.com/jjhoc/sheet-localization-py',
    author='Shodan Vault & Heskemo',
    author_email='steein.shamsudin@gmail.com',
    license='MIT License',
    zip_safe=False,
    python_requires='>=3.5,<=4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['examples', 'private']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=EXTRAS_REQUIRE['tester'],
    extras_require=EXTRAS_REQUIRE,
)
