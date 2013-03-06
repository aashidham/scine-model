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


Platform.set_root('all')


class Importer(object):

    def find_module(self, name, path):
        if name == 'platform':
            return self
        else:
            return None

    def load_module(self, name):
        return Platform

sys.meta_path.insert(0, Importer())


import insert_scine
import model.simple
import progression


i = 0
for R_pene in progression.Linear(1e3, 1e13, 10):
    for deformability in [10000, 1000, 100, 10, 1]:
        for R_seal_total in progression.Linear(1e7, 1e12, 10):
            i += 1
            Platform.set_root('all/trial=%i' % i)
            insert_scine.insert_scine(2000e-9, 200e-9, 300e-9, deformability, 0.2, R_pene, R_seal_total, 2, model.simple)
