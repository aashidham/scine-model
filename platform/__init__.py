import argparse
import sys


class Platform(object):

    name = None

    def __init__(self):
        self._tasks = []

    def args(self, parser):
        pass

    def __call__(self, task):
        task.platform = self
        self._tasks.append(task)

    def execute(self):
        raise NotImplementedError()

    def file(self):
        raise NotImplementedError()


def go(platform_cls):

    class Importer(object):

        def find_module(self, name, path):
            if name == 'chosen_platform':
                return self
            else:
                return None

        def load_module(self, name):
            return platform_cls()

    sys.meta_path.insert(0, Importer())
    parser = argparse.ArgumentParser(description=platform_cls.name)
    parser.add_argument('module', help='Which module to command')
    args = parser.parse_args(sys.argv[1:2])
    to_command = __import__(args.module, globals(), locals(), [], -1)
    to_command.chosen_platform.args(parser)
    to_command.chosen_platform.execute()
