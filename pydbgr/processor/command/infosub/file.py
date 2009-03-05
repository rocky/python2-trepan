# -*- coding: utf-8 -*-
#   Copyright (C) 2008, 2009 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import columnize, inspect, os, pyficache, sys

from import_relative import *
# Our local modules
Mbase_subcmd  = import_relative('base_subcmd', '..', 'pydbgr')
Mmisc         = import_relative('misc', '....', 'pydbgr')

try:
    import coverage
except:
    coverage = None
    pass

class InfoFile(Mbase_subcmd.DebuggerSubcommand):
    '''info file [filename [all | lines | sha1 | size]]

Show information about the current file. If no filename is given and
the program is running then the current file associated with the
current stack entry is used. Sub options which can be shown about a file are:

line -- Line numbers where there are statement boundaries. 
        These lines can be used in breakpoint commands.
sha1 -- A SHA1 hash of the source text. This may be useful in comparing
        source code.
size -- The number of lines in the file.

all  -- All of the above information.
'''

    min_abbrev = 2
    need_stack = False
    short_help = 'Show information about an imported or loaded Python file'

    def run(self, args):
        """Get file information"""
        if len(args) == 0:
            if not self.proc.curframe:
                self.errmsg("No frame - no default file.")
                return False
            filename = self.proc.curframe.f_code.co_filename
        else:
            filename = args[0]
            pass

        m = filename + ' is'
        filename_cache = self.core.filename_cache
        if filename in filename_cache:
            m += " cached in debugger"
            if filename_cache[filename] != filename:
                m += ' as:'
                m = Mmisc.wrapped_lines(m, filename_cache[filename] + '.',
                                        self.settings['width'])
            else:
                m += '.'
                pass
            self.msg(m)
        else:
            self.msg(m + ' not cached in debugger.')
            pass
        canonic_name = self.core.canonic(filename)
        self.msg(Mmisc.wrapped_lines('Canonic name:', canonic_name,
                                     self.settings['width']))
        for name in (canonic_name, filename):
            if name in sys.modules:
                for key in [k for k,v in sys.modules.items()
                            if name == v]:
                    self.msg("module: %s", key)
                    pass
                pass
            pass
        for arg in args[1:]:
            processed_arg = False
            if arg in ['all', 'size']:
                self.msg("File has %d lines." % pyficache.size(canonic_name))
                processed_arg = True
                pass
            if arg in ['all', 'sha1']:
                self.msg("SHA1 is %s." % pyficache.sha1(canonic_name))
                processed_arg = True
                pass
            if arg in ['all', 'lines']:
                lines = pyficache.trace_line_numbers(canonic_name)
                self.msg("Possible breakpoint line numbers:")
                fmt_lines = columnize.columnize(lines, ljust = False,
                                                arrange_vertical = False,
                                                lineprefix='  ')
                self.msg(fmt_lines)
                processed_arg = True
                pass
            if not processed_arg:
                self.errmsg("Don't understand sub-option %s." % arg)
                pass
            pass
        return
    pass

if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    d, cp = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoFile(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    sub.run(['file.py', 'foo'])
    for width in (200, 80):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])
        print sub.run([])
        pass
    sub.run(['file.py', 'all'])
    # sub.run(['file.py', 'lines', 'sha1'])
    pass