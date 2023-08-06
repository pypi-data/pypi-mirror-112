"""sc-introspection utilities """

__version__ = '0.1.0'
__author__ = 'Snap Dep'
__all__ = []

import platform
import sys


def warning_message():
    package_name = "sc-introspection"
    sys.stderr.write('Note, your build has pulled the public version of: {}\n'.format(package_name))
    sys.exit(1)

if 'darwin' in platform.platform():
    warning_message()
