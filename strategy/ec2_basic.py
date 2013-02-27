import math
import os
import random
import subprocess
import tempfile

import strategy


class BasicEC2Strategy(strategy.Strategy):

    name = 'Runs tasks over a given number of instances.'

    def __init__(self):
        super(BasicEC2Strategy, self).__init__()

    def args(self, parser):
        parser.add_argument('ami', type=str, help='Which amazon machine image')
        parser.add_argument('instance_type', type=str, help='What type of instance')
        parser.add_argument('instance_count', type=int, help='How many instances')
        self._args = parser.parse_args()

    def execute(self):

        # Divide up tasks among workers.
        tasks = list(self._tasks)
        random.shuffle(tasks)
        queues = dict((i, []) for i in range(min(self._args.instance_count, len(self._tasks))))
        evenly_count = len(tasks) / self._args.instance_count
        for q in queues:
            queues[q].extend(tasks[:evenly_count])
            tasks = tasks[evenly_count:]
        for i in range(len(tasks) % self._args.instance_count):
            queues[queues.keys()[i]].append(tasks.pop())

        # Make a sources tarball.
        fd, fn = tempfile.mkstemp('.tar.gz')
        subprocess.check_call('tar czf %s $(git ls-files)' % fn, shell=True)
        os.close(fd)

        # For every worker,
        for tasks in queues.items():

            # start an EC2 worker,

            # scp source tarball over,

            # ssh in and extract tarball,

            # and drop in S3 credentials.

            # Do all job setups and start jobs, adapted to EC2HostedTask.

            pass

        # Wait until all workers have 'completed' meta states.

        # Get all outputs from S3.


if __name__ == '__main__':
    strategy.go(BasicEC2Strategy)
