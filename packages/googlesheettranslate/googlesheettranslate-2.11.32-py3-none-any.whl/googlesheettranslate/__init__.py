#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

import pkg_resources
import sys


if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")

__version__ = pkg_resources.get_distribution("googlesheettranslate").version

__all__ = [
    '__version__',
]
