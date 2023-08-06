from conanx import HOME_DIR
import os
from conanx.core.profile import PLATFORM
from conanx.commands import Command, register_command, ArgparseArgument
from conanx.errors import UsageException
from conanx.utils import system_info
from conanx.core.project import Project


PLATFORM = system_info()[0]

class GitlabRunner(Command):
    """
    Builds a binary package and storage in local cache.

    """

    name = 'gitlab-runner'
    help = 'Builds a binary package for the project and cache it in local.'
    prog = 'epm [-p PROFILE] [-s SCHEME] [-r RUNNER] %s' % name

    def __init__(self):
            args = [
                ArgparseArgument("--profile", type=str, help="profile of the package to create."),
                ArgparseArgument("--scheme", default=None, type=str, help="scheme of the package to create."),
                ArgparseArgument("--test", default=None, action='append', 
                                    help="this option only use for test/debug program. if the program specifed"
                                         "only run building of pargram (which in program.location), the package"
                                         "creatation should be done. if --test disable/None all program will not"
                                         "be build"),
                ArgparseArgument("--docker", default=False, action='store_true', 
                                    help="use docker build (if the profile supported)"),


                ArgparseArgument("--storage", default=None,
                                    help="all conan package will be download and cached under project directory"
                                         "that is conan storage path will be set at .conan folder in project."),

                ArgparseArgument("--clear", default=False, action="store_true",
                                    help="clear local cache of .conan in project"),

                ArgparseArgument("--archive", default=None, help="archive the package to specified path"),
                ArgparseArgument("--with-deps", dest="with_deps", default=False, action='store_true',
                                 help="archive the dependent packages, this option vaild on --archive set."),
                
                

            ]
            Command.__init__(self, args)

    def run(self, args):
        print(args)


register_command(GitlabRunner)
