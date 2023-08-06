# This file was ported from conan.io project
# url: https://github.com/conan-io/conan/conans/cli/cli.py
# 
# ==========================================================
import importlib
import os
import pkgutil
import shutil
import signal
import sys
import argparse
from collections import defaultdict
from difflib import get_close_matches
from inspect import getmembers

from colorama import Style

from ezdev import __version__ as ezdev_version
from ezdev.utils.files import exception_message_safe, mkdir
from ezdev.utils.log import logger
from ezdev.errors import EZException, ConfigurationException
from ezdev.enums import ExitCode
from ezdev import commands
from ezdev.utils import _
from ezdev.utils.output import Output
class Cli(object):
    """A single command of the conan application, with all the first level commands. Manages the
    parsing of parameters and delegates functionality to the conan python api. It can also show the
    help of the tool.
    """
    description = "EZDev"

    def __init__(self, output):
        self.args = None
        self._parser = None
        self._out = Output()

    @property
    def parser(self):
        ''' Creates the arguments parser '''
        if self._parser is None:
            self._parser = argparse.ArgumentParser(description=_(self.description))
        return self._parser
        

    def _print_similar(self, command, commands):
        """ Looks for similar commands and prints them if found.
        """
        matches = get_close_matches(
            word=command, possibilities=commands, n=5, cutoff=0.75)

        if len(matches) == 0:
            return

        if len(matches) > 1:
            self._out.info("The most similar commands are")
        else:
            self._out.info("The most similar command is")

        for match in matches:
            self._out.info("    %s" % match)

        self._out.info("")


    def run(self, args):
        """ Entry point for executing commands, dispatcher to class
        methods
        """
        version = sys.version_info
        if version.major == 2 or version.minor <= 4:
            raise EZCException(
                "Unsupported Python version. Minimum required version is Python 3.5")

        # If no commands, make it show the help by default
        if len(args) == 0:
            args = ["-h"]
            
        command = args[0]
        if len(args) ==1 and command in ['-v', '--version']:
            from conans import __version__ as conan_version
            self._out.info("ezdev version %s" % conanx_version)
            return ExitCode.SUCCESS
        
        subparsers = self.parser.add_subparsers(help=_('sub-command help'), dest='command')
        commands.load_commands(subparsers, self._out)
        
        from conanx.commands import list_commands        
        COMMANDs = list_commands()
        
        if command not in COMMANDs:
            self._out.info("'%s' is not a ConanX command. See 'conanx --help'." % command)
            self._out.info("")
            self._print_similar(command, COMMANDs)
            raise ConanXException(f"Unknown command '{command}'")
        self.args = self.parser.parse_args(args)
        
        
        commands.run(command, self.conan_api, self.args)

        return ExitCode.SUCCESS

    def init(self):
        pass
        
    
def cli_out_write(data, fg=None, bg=None):
    data = "{}{}{}{}\n".format(fg or '', bg or '', data, Style.RESET_ALL)
    sys.stdout.write(data)


def main(args):
    """ main entry point of the conan application, using a Command to
    parse parameters

    Exit codes for conan command:

        0: Success (done)
        1: General ConanxException error (done)
        2: Migration error
        3: Ctrl+C
        4: Ctrl+Break
        5: SIGTERM
        6: Invalid configuration (done)
        7: General ConanException error
    """

    def ctrl_c_handler(_, __):
        print('You pressed Ctrl+C!')
        sys.exit(ExitCode.USER_CTRL_C)

    def sigterm_handler(_, __):
        print('Received SIGTERM!')
        sys.exit(ExitCode.ERROR_SIGTERM)

    def ctrl_break_handler(_, __):
        print('You pressed Ctrl+Break!')
        sys.exit(ExitCode.USER_CTRL_BREAK)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, ctrl_break_handler)

    try:
        cli = Cli()
        cli.init()
        exit_error = cli.run(args)
    except SystemExit as exc:
        if exc.code != 0:
            logger.error(exc)
            conan_api.out.error("Exiting with code: %d" % exc.code)
        exit_error = exc.code
    except ConanInvalidConfiguration as exc:
        exit_error = ExitCode.ERROR_INVALID_CONFIGURATION
        conan_api.out.error(exc)
        
    except ConfigurationException as exc:
        exit_error = ExitCode.ERROR_CONFIGURATION
        conan_api.out.error(exc)        
    except ConanException as exc:
        exit_error = ExitCode.ERROR_CONAN_GENERAL
        conan_api.out.error(exc)
    except ConanXException as exc:
        exit_error = ExitCode.ERROR_GENERAL
        conan_api.out.error(exc)
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
        exit_error = ExitCode.ERROR_GENERAL
        msg = exception_message_safe(exc)
        conan_api.out.error(msg)

    sys.exit(exit_error)


def run():
    main(sys.argv[1:])

   