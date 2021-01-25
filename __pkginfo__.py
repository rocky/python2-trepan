# Copyright (C) 2008-2010, 2013-2018, 2021 Rocky Bernstein <rocky@gnu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Debugger packaging information"""

# To the extent possible we make this file look more like a
# configuration file rather than code like setup.py. I find putting
# configuration stuff in the middle of a function call in setup.py,
# which for example requires commas in between parameters, is a little
# less elegant than having it here with reduced code, albeit there
# still is some room for improvement.

# Things that change more often go here.
copyright = """
Copyright (C) 2008-2010, 2013-2018, 2020 Rocky Bernstein <rocky@gnu.org>.
"""

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
]

# Python-version | package | last-version |
# -----------------------------------------
# 2.5            | pip     |  1.1         |
# 2.6            | pip     |  1.5.6       |
# 2.7            | pip     | 19.2.3       |

# The rest in alphabetic order
author = "Rocky Bernstein"
author_email = "rocky@gnu.org"
ftp_url = None
install_requires = [
    "columnize >= 0.3.10",
    "nose>=1.0.0, <= 1.3.7",
    "pyficache >= 2.2.1",
    "pygments == 2.2.0",  # Later releases don't support Python 2.7
    "spark_parser >= 1.8.9, <1.9.0",
    "uncompyle6 >= 3.7.4",
    "tracer >= 0.3.2",
    "unittest2",
    "xdis >= 5.0.4",
]
license = "GPL3"
mailing_list = "python-debugger@googlegroups.com"
modname = "trepan2"
packages = [
    "trepan",
    "trepan.bwprocessor",
    "trepan.interfaces",
    "trepan.inout",
    "trepan.lib",
    "trepan.processor",
    "trepan.processor.command",
    #   'trepan.processor.command.ipython_magic',
    "trepan.processor.command.info_subcmd",
    "trepan.processor.command.set_subcmd",
    "trepan.processor.command.show_subcmd",
    "trepan.processor.parse",
]
py_modules = None
short_desc = "GDB-like Python Debugger in the Trepan family"

import os.path as osp


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


# trepan/version.py sets variable __version__.
ns = {}
exec(open(osp.join(get_srcdir(), "trepan", "version.py")).read(), ns)
version = ns["__version__"]
web = "http://github.com/rocky/python2-trepan/"

# tracebacks in zip files are funky and not debuggable
zip_safe = False


def read(*rnames):
    return open(osp.join(osp.dirname(__file__), *rnames)).read()


long_description = read("README.rst") + "\n"
