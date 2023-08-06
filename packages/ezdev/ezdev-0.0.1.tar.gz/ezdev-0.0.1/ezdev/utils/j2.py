
import os
import pathlib
from jinja2 import Environment, FileSystemLoader, BaseLoader

def abspath(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    path = os.path.normpath(path)
    return path


def win_path(path):
    path = os.path.normpath(path)
    path = path.replace('/', '\\')
    return path

def unix_path(path):
    return pathlib.PurePath(path).as_posix()

class Jinja2(object):
    Filters = {
        'basename': os.path.basename,
        'dirname': os.path.dirname,
        'abspath': abspath,
        'win_path': win_path,
        'unix_path': unix_path
    }

    def __init__(self, directory=None, context=None):
        self._dir = directory
        self._context = context or {}

    def _add_filters(self, env):
        for name, fn in self.Filters.items():
            env.filters[name] = fn
        return env

    def render(self, template, context={}, outfile=None, encoding='utf-8', trim_blocks=False):
        
        path = abspath(self._dir or '.')

        env = Environment(loader=FileSystemLoader(path))
        includes_loader = FileSystemLoader(path)
        includes_env = Environment(loader=includes_loader)

        env.trim_blocks = trim_blocks
        self._add_filters(env)
        T = env.get_template(template)
        T.environment = includes_env
        context = dict(self._context, **context)
        text = T.render(context)
        #if newline == '\n':
        #    text.replace("\r\n", "\n")
        if outfile:
            path = os.path.abspath(outfile)
            folder = os.path.dirname(path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(path, 'wb') as f:
                f.write(bytes(text, encoding=encoding))
        return text

    def parse(self, text, context={}):
        env = Environment(loader=BaseLoader())
        self._add_filters(env)
        T = env.from_string(text)
        context = dict(self._context, **context)
        return T.render(context)
