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

import inspect
from import_relative import import_relative
# Our local modules
import_relative('processor', '....', 'pydbgr')
Mbase_subcmd  = import_relative('base_subcmd', '..', 'pydbgr')
Mcmdfns       = import_relative('cmdfns', '..', 'pydbgr')
Mcmdproc      = import_relative('cmdproc', '...', 'pydbgr')

class SetCmdDbgPydb(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """Set the ability to debug the debugger.
    
Setting this allows visibility and access to some of the debugger's
internals.
"""

    in_list    = True
    min_abbrev = 3    # Need at least "set dbg"
    short_help = "Set debugging the debugger"

    def run(self, args):
        Mcmdfns.run_set_bool(self, args)
        if self.debugger.settings[self.name]:
            # Put a stack frame in the list of frames so we have
            # something to inspect.
            frame = inspect.currentframe()
            self.proc.stack, self.proc.curindex = \
                Mcmdproc.get_stack(frame, None, self.proc)
            self.proc.curframe = self.proc.stack[self.proc.curindex][0]
            # Remove ignored debugger functions.
            self.core.ignore_filter = None
            pass
        return
    pass


