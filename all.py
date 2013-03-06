import os.path
import sys


class Platform(object):

    @classmethod
    def change_root(cls, path):
        cls._root = path
        os.mkdir(cls._root)

    @classmethod
    def file(cls, fn):
        fn = '%s/%s' % (cls._root, fn)
        assert not os.path.exists(fn)
        return fn


Platform.change_root('derp')


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


for R_pene in progression.Linear(1e3, 1e13, 10):
    for deformability in [10000, 1000, 100, 10, 1]:
        for R_seal_total in progression.Linear(1e7, 1e12, 10):
            Platform.change_root('derp/thing')
            insert_scine.insert_scine(2000e-9, 200e-9, 300e-9, deformability, 0.2, R_pene, R_seal_total, 2, model.simple)
