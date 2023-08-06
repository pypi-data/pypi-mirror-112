"""
    Copyright 2016-2021 Stephane De Mita, Mathieu Siol

    This file is part of EggLib.

    EggLib is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EggLib is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with EggLib.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, re, tempfile, shutil
from .. import _interface

def _write_sample(obj, fname):
    if not isinstance(obj, (_interface.SampleView, str)): raise TypeError('invalid type for `obj` argument')
    f = open(fname, 'w')

    if isinstance(obj, _interface.SampleView):
        name = obj[0]
        sequence =list(obj[1].string())
        f.write('>{0}\n'.format(name))
        for j in range(0, len(sequence), 60):
            f.write(''.join(sequence[j:j+60]) + '\n')
    elif isinstance(obj, str):
        sequence =list(obj)
        f.write('>String_to_fasta\n')
        for j in range(0, len(sequence), 60):
            f.write(''.join(sequence[j:j+60]) + '\n')
    f.close()

def _write(obj, fname, mapping):
    f = open(fname, 'w')
    for i, sam in enumerate(obj):
        n = 'seq-{0}'.format(len(mapping) + 1)
        f.write('>{0}\n'.format(n))
        for j in range(0, len(sam.sequence), 100):
            f.write(sam.sequence[j:j+100] + '\n')
        mapping[n] = sam
    f.close()

def _protect_run(f):
    """
    This function is designed to be a decorator for wrapper functions.
    It runs the argument function into a temporary directory, ensuring
    that the temporary directory is deleted after completion of the
    function.
    """
    def _f(*args, **kwargs):
        tmp = None
        curr = os.getcwd()
        try:
            tmp = tempfile.mkdtemp()
            os.chdir(tmp)
            return f(*args, **kwargs)
        finally:
            os.chdir(curr)
            if tmp is not None:
                shutil.rmtree(tmp)
    _f.__name__ = f.__name__
    _f.__doc__ = f.__doc__
    return _f

class _Paths(object):
    """
    Class (designed to be a singleton) holding external applications.
    Each application is represented by an _App instance.
    """

    def __init__(self):
        self._apps = {}

    def _add(self, app):
        """
        Add an application wrapper.

        :param app: a :class:`._App` instance.
        :param key: the application's name.
        :param default: the default path.
        """
        self._apps[app._key] = app

    def __iter__(self):
        for i in self._apps:
            yield i

    def __getitem__(self, app):
        if app not in self._apps: raise ValueError('invalid application name: {0}'.format(app))
        return self._apps[app].get_path()

    def __setitem__(self, app, path):
        if app not in self._apps: raise ValueError('invalid application name: {0}'.format(app))
        self._apps[app].set_path(path, True)

    def autodetect(self, verbose=False):
        failed = {}
        passed = 0
        n = len(self._apps)
        sz = len(str(n))
        if verbose:
            print('Detecting external applications: ' + '0'.rjust(sz) + '/' + str(n), flush=True, end='')
        for key, app in self._apps.items():
            result = app.set_path(app._default, False)
            if result is None:
                passed += 1
            else:
                app.set_path(None, True)
                failed[key] = app._default, result
            if verbose:
                print('\b'*(2*sz+1) + str(passed+len(failed)).rjust(sz) + '/' + str(n), flush=True, end='')
        if verbose:
            print('\b'*(2*sz+1) + str(passed).rjust(sz) + '/' + str(n) + ' passed')
            for k, (cmd, msg) in failed.items():
                print(k, ' [', cmd, ']: ', msg, sep='')
        return passed, len(failed), failed

    def save(self):
        fname = os.path.join(os.path.dirname(__file__), 'apps.conf')
        try:
            f = open(fname, 'w')
        except IOError as e:
            if e.errno == 13: raise ValueError('administrator rights are required')
            else: raise
        for app, path in self._apps.items():
            path = path.get_path()
            if path is None: f.write('{0}: *\n'.format(app))
            else: f.write('{0}: {1}\n'.format(app, path))
        f.close()

    def load(self):
        fname = os.path.join(os.path.dirname(__file__), 'apps.conf')
        if not os.path.isfile(fname):
            # if file doesn't exist, set all paths to None
            for key in self._apps:
                self._apps[key]._path = None
            #raise RuntimeError('cannot find configuration file `apps.conf`')
            return

        f = open(fname)
        for linenum, line in enumerate(f):
            line = line.strip()
            if line == '': continue         # support empty lines
            if line[0] == '#': continue     # support comment lines
            mo = re.match('^([a-z]+): *((?![ #]).+?) *(\#.+)?$', line)
            if mo is None: raise RuntimeError('invalid file `apps.conf` (line {0})'.format(linenum+1))
            key, path, comment = mo.groups()
            if key not in self._apps: raise RuntimeError('invalid file `apps.conf` (unknown application: {0})'.format(key))
            if path == '*': self._apps[key]._path = None
            else: self._apps[key]._path = path
        f.close()

    def __str__(self):
        return str(dict([(i, j.get_path()) for (i,j) in self._apps.items()]))

    def as_dict(self):
        return dict([(i, j.get_path()) for (i,j) in self._apps.items()])

class _App(object):
    def __init__(self, key, default):
        self._path = None
        self._key = key
        self._default = default

    def get_path(self):
        """ Get the application path. """
        return self._path

    def set_path(self, path, critical):
        """
        Set the application path. The path is set if the check function
        (to be implemented as _check_path) succeeds. If it fails, a
        :exc:`~.exceptions.ValueError` is raised (if *critical* is
        ``True``), or the path is set to ``None`` and the error message
        string is returned (otherwise).
        """
        if path is None:
            self._path = None
        else:
            result = self._check_path(path)
            if result is None: self._path = path
            elif critical: raise ValueError('cannot set path for {0}: {1}'.format(self._key, result))
            else: return result

    key = property(lambda self: self._key, doc='key of the object _App')

paths = _Paths()
