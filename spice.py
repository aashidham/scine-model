import math
import os.path
import re
import subprocess

import task


class SpiceTask(task.PythonTask):

    sys_packages = ['ngspice']
    pip_packages = []

    in_files = ['circuit']


class TransientSpice(SpiceTask):

    def _run(self, platform, transient_step, transient_max_T, **kwargs):
        data = platform.file('.data')
        inp = """
tran %(transient_step)f %(transient_max_T)f
wrdata %(data_out)s electrode_bus solution_bus cell_bus
quit
""" % {
            'transient_step': float(transient_step),
            'transient_max_T': float(transient_max_T),
            'data_out': '.'.join(data.split('.')[:-1])
            }
        subprocess.Popen(['ngspice', '-p', self.in_files['circuit']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)
        return [data]


class ACSpice(SpiceTask):

    def _run(self, platform, exponent_low, exponent_high, **kwargs):
        exponent_low, exponent_high = map(float, [exponent_low, exponent_high])
        data = platform.file('.data')
        inp = """
ac dec 100 %(f_low)f %(f_high)f
wrdata %(data_out)s electrode_bus solution_bus cell_bus
quit
""" % {
            'f_high': math.pow(10, exponent_high),
            'f_low': math.pow(10, exponent_low),
            'data_out': '.'.join(data.split('.')[:-1])
            }
        subprocess.Popen(['ngspice', '-p', self.in_files['circuit']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)
        return [data]
