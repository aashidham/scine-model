import math
import os.path
import re
import subprocess

import task


class SpiceTask(task.PythonTask):

    sys_packages = ['ngspice']
    pip_packages = []

    in_files = ['circuit']

    def derivatives(self, fn):
        # Make plot.
        plot_fn = self.platform.file('plot.png')
        subprocess.check_call("gnuplot -e \"set term png; set output '%s'; plot '%s' using 1:2 with linespoints\"" % (plot_fn, fn), shell=True)
        return [plot_fn]


class TransientSpice(SpiceTask):

    params = {
        'transient_step': float,
        'transient_max_T': float
        }

    def _run(self):
        data = self.platform.file('the.data')
        inp = """
tran %f %f
wrdata %s electrode_bus solution_bus cell_bus
quit
""" % (self['transient_step'], self['transient_max_T'], '.'.join(data.split('.')[:-1]))
        subprocess.Popen(['ngspice', '-p', self.in_files['circuit']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)
        return [data] + self.derivatives(data)


class ACSpice(SpiceTask):

    def _run(self, exponent_low, exponent_high, **kwargs):
        exponent_low, exponent_high = map(float, [exponent_low, exponent_high])
        data = self.platform.file('the.data')
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
