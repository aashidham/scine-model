import json
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
        # Make plot.
        plot_fn = self.platform.file('plot.png')
        subprocess.check_call("gnuplot -e \"set term png; set output '%s'; plot '%s' using 1:2 with linespoints\"" % (plot_fn, data), shell=True)
        return [data, plot_fn]


class ACSpice(SpiceTask):

    params = {
        'exponent_low': float,
        'exponent_high': float,
        'params': dict
        }

    def _run(self):
        data = self.platform.file('the.data')
        f_low = math.pow(10, self['exponent_low'])
        f_high = math.pow(10, self['exponent_high'])
        inp = """
ac dec %f %f %f
wrdata %s mag(electrode_bus) phase(electrode_bus)
quit
""" % (self['exponent_high'] - self['exponent_low'], f_low, f_high, '.'.join(data.split('.')[:-1]))
        subprocess.Popen(['ngspice', '-p', self.in_files['circuit']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)

        # Make plot.
        mag_plot_fn = self.platform.file('plot-mag.png')
        subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 1:2 with linespoints\"" % (mag_plot_fn, data), shell=True)
        phase_plot_fn = self.platform.file('plot-phase.png')
        subprocess.check_call("gnuplot -e \"set term png; set output '%s'; set logscale x; plot '%s' using 3:4 with linespoints\"" % (phase_plot_fn, data), shell=True)

        j = []
        for line in open(data):
            cols = map(float, line.split())
            d = dict(self['params'])
            d.update({
                    'f': cols[0],
                    'mag': cols[1],
                    'phase': cols[3]
                    })
            j.append(d)
        f = open(self.platform.file('thing.json'), 'w')
        f.write(json.dumps(j))
        f.close()

        return [data, mag_plot_fn, phase_plot_fn]
