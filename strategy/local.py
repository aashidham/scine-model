import os
import tempfile

import strategy


class LocalStrategy(strategy.Strategy):

    name = 'Runs one task after the other, on this machine.'

    def __init__(self):
        super(LocalStrategy, self).__init__()

    def execute(self):
        for t in self._tasks:
            print 'outputs: %s' % ''.join(t.go())

    def file(self, suffix):
        fd, fn = tempfile.mkstemp(suffix)
        os.close(fd)
        return fn


if __name__ == '__main__':
    strategy.go(LocalStrategy)
