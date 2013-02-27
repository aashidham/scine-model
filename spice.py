import math
import os.path
import re
import subprocess

import task


def run_ac(cir_path, params):
    m = re.search(r'(^.*?)\.cir$', os.path.basename(cir_path))
    assert false
    params['filename'] = 'data/%s' % m.group(1)
    params['n_decades'] = params['exponent_high'] - params['exponent_low']
    params['f_low'] = math.pow(10, params['exponent_low'])
    params['f_high'] = math.pow(10, params['exponent_high'])
    inp = """
ac dec %(n_decades)i %(f_low)f %(f_high)f
wrdata %(filename)s electrode_bus
quit
""" % params
    subprocess.Popen(['ngspice', '-p', cir_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(inp)


class SpiceTask(task.PythonTask):

    sys_packages = ['ngspice']
    pip_packages = []


class TransientSpice(SpiceTask):

    in_files = ['circuit']
    out_files = ['data']

    def _run(self, in_files, out_files, transient_step, transient_max_T):
        inp = """
tran %(transient_step)f %(transient_max_T)f
wrdata %(data_out)s electrode_bus solution_bus cell_bus
quit
""" % {
            'transient_step': float(transient_step),
            'transient_max_T': float(transient_max_T),
            'data_out': out_files['data']
            }
        subprocess.Popen(['ngspice', '-p', in_files['circuit']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)

