import os
import tempfile

import platform


class LocalPlatform(platform.Platform):

    name = 'Runs one task after the other, on this machine.'

    def __init__(self):
        super(LocalPlatform, self).__init__()

    def args(self, parser):
        parser.add_argument('results_directory', type=str, help='Where to store results')

    def execute(self):
        os.mkdir(self._args.results_directory)
        print '%i tasks' % len(self._tasks)
        for i, t in enumerate(self._tasks):
            self._task_results_path = '%s/%i' % (self._args.results_directory, i)
            os.mkdir(self._task_results_path)
            print 'params: %s, inputs: %s, outputs: %s' % (' '.join(map(lambda k: '%s=%s' % (k, t[k]), t.params)), ' '.join(t.in_files.values()), ' '.join(t.go()))

    def file(self, fn):
        return '%s/%s' % (self._task_results_path, fn)

    def get_param(self, ty, name):
        return ty(input('%s = ' % name))


if __name__ == '__main__':
    platform.go(LocalPlatform)
