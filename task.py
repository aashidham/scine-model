import argparse
import os
import os.path
import subprocess
import sys

import platform.local


DEVNULL = open(os.devnull, 'wb')


class Task(object):

    params = {}

    platform = None
    sys_packages = []
    in_files = {}

    def __init__(self, in_files, **kwargs):
        assert set(in_files.keys()) == set(self.in_files)
        self.in_files = in_files
        assert set(kwargs) <= set(self.params), kwargs
        self.params = dict(self.params)
        self.params.update(kwargs)

    def go(self):
        assert self.platform is not None
        self._setup()
        out_fns = self._run()
        self._teardown()
        return out_fns

    def _setup(self):
        for p in self.sys_packages + ['python'] + (['python-virtualenv'] if self.pip_packages else []):
            if subprocess.call(['/usr/bin/dpkg-query', '-l', p], stdout=DEVNULL) != 0:
                subprocess.check_call('sudo apt-get -y --force-yes -qq install %s' % p, shell=True)

    def _run(self):
        raise NotImplementedError()

    def _teardown(self):
        pass

    def to_command_line(self):
        in_files = ' '.join(map(lambda kv: '--in-%s=%s' % kv, self.in_files.items()))
        return 'python -m task %s %s %s %s' % (self.__module__, self.__class__.__name__, ' '.join(map(str, self._args)), in_files)

    def __getitem__(self, name):
        """ Get a parameter value. """
        assert self.platform is not None
        if type(self.params[name]) is type:
            self.params[name] = self.platform.get_param(self.params[name], name)
        return self.params[name]


if __name__ == '__main__':

    # First parse: get the module and class.
    parser = argparse.ArgumentParser()
    parser.add_argument('module', help='Which module contains the task class.')
    parser.add_argument('cls', help='The task class.')
    parser.add_argument('params', nargs='*', default=[])
    args = parser.parse_args(sys.argv[1:3])

    # Get the class and parse the rest of the arguments for input files.
    module = __import__(args.module, globals(), locals(), [], -1)
    cls = getattr(module, args.cls)
    for key in cls.in_files:
        parser.add_argument('--in-%s' % key, type=str, required=True)
    task_args = []
    for key in cls.params:
        task_args.append(key)
        if type(cls.params[key]) is type:
            parser.add_argument('--%s' % key, type=cls.params[key])#, required=True)
        else:
            parser.add_argument('--%s' % key, type=type(cls.params[key]))
    args = parser.parse_args(sys.argv[1:])

    # Run the task!
    task_args = dict((a, getattr(args, a)) for a in task_args)
    for k, v in task_args.items():
        if v is None:
            del task_args[k]
    t = cls(dict([(key, getattr(args, 'in_%s' % key)) for key in cls.in_files]), **task_args)
    s = platform.local.LocalPlatform()
    s(t)
    s.execute()


class PythonTask(Task):

    pip_packages = []

    def _setup(self):
        super(PythonTask, self)._setup()
        if self.pip_packages:
            if not os.path.exists('env'):
                subprocess.check_call(['virtualenv', 'env']) == 0
                for p in self.pip_packages:
                    subprocess.check_call(['pip', 'install', p]) == 0
            # TODO; activate env

    def teardown(self):
        # deactivate env
        super(PythonTask, self).teardown()
