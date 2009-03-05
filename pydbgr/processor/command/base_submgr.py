# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.
import columnize, inspect, os, string, sys
from import_relative import *
base_cmd  = import_relative('base_cmd')
subcmd    = import_relative('subcmd', os.path.pardir)

class SubcommandMgr(base_cmd.DebuggerCommand):

    category      = 'status'
    min_args      = 0
    max_args      = None
    name_aliases  = None # ('???','?')  # Need to define this!
    need_stack    = False

    def __init__(self, proc, name=None):
        """Initialize show subcommands. Note: instance variable name
        has to be setcmds ('set' + 'cmds') for subcommand completion
        to work."""

        base_cmd.DebuggerCommand.__init__(self, proc)

        # Name is set in testing
        if name is None: name  = self.__module__.split('.')[-1]
        self.__class__.name = name

        self.cmds = subcmd.Subcmd(name, self)
        self.name = name
        self._populate_subcommands(name)
        self.proc = proc

        return

    def _populate_subcommands(self, name):
        """ Create an instance of each of the debugger
        subcommands. Commands are found by importing files in the
        directory 'name' + 'sub'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""

        # Iniitialization
        cmd_instances     = []
        module_dir        = name + 'sub'
        class_prefix      = string.capitalize(name) # e.g. Info, Set, or Show
        mod               = import_relative(module_dir)
        eval_cmd_template = 'command_mod.%s(self)'
        srcdir            = get_srcdir()
        sys.path.insert(0, srcdir)

        # Import, instantiate, and add classes for each of the
        # modules found in module_dir imported above.
        for module_name in mod.__modules__:
            import_name = module_dir + '.' + module_name

            try:
                command_mod = getattr(__import__(import_name), module_name)
            except ImportError:
                print("Error importing module %s: %s" % 
                      (module_name,sys.exc_info()[0]))
                

            # Even though we tend not to do this, it is possible to
            # put more than one class into a module/file.  So look for
            # all of them.
            classnames = [ classname for classname, classvalue in 
                           inspect.getmembers(command_mod, inspect.isclass)
                           if ('DebuggerCommand' != classname and 
                               classname.startswith(class_prefix)) ]

            for classname in classnames:
                eval_cmd = eval_cmd_template % classname
                try: 
                    instance = eval(eval_cmd)
                    self.cmds.add(instance)
                except:
                    print "Error eval'ing class %s" % classname
                    pass
                pass
            pass
        sys.path.remove(srcdir)
        return cmd_instances

    def help(self, args):
        """Give help for a command which has subcommands. This can be
        called in several ways:
            help cmd
            help cmd subcmd
            help cmd commands

        Our shtick is to give help for the overall command only if 
        subcommand or 'commands' is not given. If a subcommand is given and
        found, then specific help for that is given. If 'commands' is given
        we will list the all the subcommands.
        """
        if len(args) <= 2:
            # "help cmd". Give the general help for the command part.
            doc = self.__doc__ or self.run.__doc__
            if doc:
                self.proc.intf[-1].msg(doc)
            else:
                self.proc.intf[-1].errmsg('Sorry - author mess up. ' + 
                                          'No help registered for command' + 
                                          self.name)
                pass
            return

        subcmd_name = args[2]

        if '*' == subcmd_name:
            self.msg("List of subcommands of command '%s':" % self.name)
            self.msg(columnize.columnize(self.cmds.list(), lineprefix='    '))
            self.cmds.list()
            return

        # "help cmd subcmd". Give help specific for that subcommand.
        cmd = self.cmds.lookup(subcmd_name)
        if cmd:
            doc = cmd.__doc__ or cmd.run.__doc__
            if doc:
                self.proc.intf[-1].msg(doc)
            else:
                self.proc.intf[-1].errmsg('Sorry - author mess up. ' + 
                                          'No help registered for subcommand: ' + 
                                          subcmd_name + ', of command: ' + 
                                          self.name)
                pass
        else:
            self.undefined_subcmd(self.name, subcmd_name)
            pass
        return

    def run(self, args):
        """Ooops -- the debugger author didn't redefine this run docstring."""
        if len(args) < 2:
            # We were given cmd without a subcommand; cmd is something
            # like "show", "info" or "set". Generally this means list
            # all of the subcommands.
            self.msg("List of %s commands (with minimum abbreviation in "
                     "parenthesis):" % self.name_aliases[0])
            for subcmd_name in self.cmds.list():
                # Some commands have lots of output.
                # they are excluded here because 'in_list' is false.
                subcmd = self.cmds.subcmds[subcmd_name]
                self.summary_help(subcmd_name, subcmd)
                pass
            return False

        subcmd_prefix = args[1]
        # We were given: cmd subcmd ...
        # Run that.
        subcmd = self.cmds.lookup(subcmd_prefix)
        if subcmd:
            return subcmd.run(args[2:])
        else:
            return self.undefined_subcmd(self.name, subcmd_prefix)
        return # Not reached

    def summary_help(self, subcmd_name, subcmd):
        return self.msg('%s (%d) %-11s -- %s' %
                        (self.name_aliases[0], subcmd.min_abbrev,
                         subcmd_name, subcmd.short_help))
    pass

    def undefined_subcmd(self, cmd, subcmd):
        """Error message when subcommand asked for but doesn't exist"""
        self.proc.intf[-1].errmsg(('Undefined "%s" subcommand: "%s". ' + 
                                  'Try "help %s *".') % (cmd, subcmd, cmd))
        return
    pass

if __name__ == '__main__':
    pass