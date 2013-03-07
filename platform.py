import os.path
import sys


class Platform(object):

    @classmethod
    def set_root(cls, path):
        os.makedirs(path)
        cls._root = list(os.path.split(path))
        cls._path = []

    @classmethod
    def set_path(cls, path):
        cls._path = list(filter(None, os.path.split(path)))
        os.makedirs(os.path.join(*(cls._root + cls._path)))

    @classmethod
    def file(cls, fn):
        fn = os.path.join(*(cls._root + cls._path + [fn]))
        print fn
        assert not os.path.exists(fn)
        return fn


class Importer(object):

    def find_module(self, name, path):
        if name == 'the_platform':
            return self
        else:
            return None

    def load_module(self, name):
        return Platform


def install():
    sys.meta_path.insert(0, Importer())




