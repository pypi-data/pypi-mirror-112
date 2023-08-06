# This file was ported from GStreamer cebero project
# url:  https://gitlab.freedesktop.org/gstreamer/cerbero/commands/__init__.py
#  
# ---------------------------------------------------------
#
# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


__all__ = ['Command', 'register_command', 'run', 'ArgparseArgument']
import os
import argparse
from conanx.errors import FatalException, UsageException
from conanx.utils import _

class SmartFormatter(argparse.HelpFormatter):

    def _fill_text(self, text, width, indent):
        import textwrap
        text = textwrap.dedent(text)
        return ''.join(indent + line for line in text.splitlines(True))


class Command:
    """Base class for Command objects"""
    name = None
    epilog = None
    prog = None
    help = None

    def __init__(self, arguments=[]):
        self.arguments = arguments

    def run(self, conan, args):
        """The body of the command"""
        raise NotImplementedError

    def add_parser(self, subparsers):
        self.parser = subparsers.add_parser(self.name, prog=self.prog,
                                            description=self.__doc__,
                                            help=self.help, epilog=self.epilog,
                                            formatter_class=SmartFormatter)
        if isinstance(self.arguments, dict):
            help = self.arguments.pop('__help__', None) or 'sub-command help'
            subparsers = self.parser.add_subparsers(help=help, dest='sub_command')
            for name, args in self.arguments.items():
                help = ''
                description = ''
                if isinstance(args, dict):
                    help = args.get('help')
                    description = args.get('description')
                    args = args.get('args') or []
                elif isinstance(args, list):
                    pass
                else:
                    raise Exception('Illegal command defaintion')
                parser = subparsers.add_parser(name, help=help, description=description)
                for arg in args:
                    arg.add_to_parser(parser)

        elif isinstance(self.arguments, list):
            for arg in self.arguments:
                arg.add_to_parser(self.parser)

# dictionary with the list of commands
# command_name -> command_instance
_commands = {}

def list_commands():
    return list(_commands.keys())

def register_command(command_class):
    command = command_class()
    _commands[command.name] = command


def load_commands(subparsers, out):
    import os
    commands_dir = os.path.abspath(os.path.dirname(__file__))

    for name in os.listdir(commands_dir):
        name, extension = os.path.splitext(name)
        if extension != '.py':
            continue
        try:
            __import__('ezdev.commands.%s' % name)
        except ImportError as e:
            out.warn("Error importing command %s:\n %s" % (name, e))
    for command in _commands.values():
        command.add_parser(subparsers)


def run(command, conan, args):
    # if the command hasn't been registered, load a module by the same name
    if command not in _commands:
        raise FatalException(_('command not found'))

    return _commands[command].run(conan, args)

class ArgparseArgument(object):

    def __init__(self, *name, **kwargs):
        self.name = name
        self.args = kwargs

    def add_to_parser(self, parser):
        parser.add_argument(*self.name, **self.args)

