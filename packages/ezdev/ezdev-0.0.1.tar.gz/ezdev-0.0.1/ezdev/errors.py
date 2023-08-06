# This file was ported from GStreamer cebero project
# url:  https://gitlab.freedesktop.org/gstreamer/cerbero/errors.py
#  
# ------------------------------------------------------------
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


from gettext import gettext as _


class EZException(Exception):
    header = ''
    msg = ''

    def __init__(self, msg=''):
        self.msg = msg
        Exception.__init__(self, self.header + msg)

class FatalError(EZException):
    header = 'Fatal Error: '
    def __init__(self, msg='', arch=''):
        self.arch = arch
        EZException.__init__(self, msg)
        
FatalException = FatalError


class ConfigurationException(EZException):
    header = 'Configuration Error: '


class UsageException(EZException):
    header = 'Usage Error: '



class CommandException(EZException):
    header = 'Command Error: '
    def __init__(self, msg, cmd, returncode):

        msg = 'Running {!r} returned {}\n{}'.format(cmd, returncode, msg or '')
        FatalException.__init__(self, msg)

        
class AbortedError(Exception):
    pass
