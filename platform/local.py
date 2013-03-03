import os
import tempfile

import platform


class LocalPlatform(platform.Platform):

    name = 'Runs one task after the other, on this machine.'

    def __init__(self):
        super(LocalPlatform, self).__init__()

    def execute(self):
        print '%i tasks' % len(self._tasks)
        for t in self._tasks:
            print '%s %s %s %s' % (' '.join(map(str, t._args)), ' '.join(map(lambda kv: '%s=%s' % kv, t._kwargs.items())), ' '.join(t.in_files.values()), ''.join(t.go()))

    def file(self, suffix):
        fd, fn = tempfile.mkstemp(suffix)
        os.close(fd)
        return fn


if __name__ == '__main__':
    platform.go(LocalPlatform)
