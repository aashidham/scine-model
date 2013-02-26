import math
import os.path
import re
import subprocess


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


class PythonTask(object):

    def __init__(self):
        raise NotImplementedError()

    def setup(self):
        for p in self.sys_packages + ['python'] + (['python-virtualenv'] if self.pip_packages else []):
            if subprocess.call(['/usr/bin/dpkg-query', '-l', p]) != 0:
                subprocess.check_call(['/usr/bin/apt-get', '-y', 'install', p])
        if self.pip_packages:
            if not os.path.exists('env'):
                subprocess.check_call(['virtualenv', 'env']) == 0
                for p in self.pip_packages:
                    subprocess.check_call(['pip', 'install', p]) == 0
            # TODO; activate env


class SpiceTask(PythonTask):

    sys_packages = ['ngspice']
    pip_packages = []


class TransientSpice(SpiceTask):

    def __init__(self, cir_path, params):
        self._cir_path = cir_path
        m = re.search(r'(^.*?)\.cir$', os.path.basename(cir_path))
        params['filename'] = 'data/%s' % m.group(1)
        self._params = params

    def run(self):
        inp = """
tran %(transient_step)f %(transient_max_T)f
wrdata %(filename)s electrode_bus solution_bus cell_bus
quit
""" % self._params
        subprocess.Popen(['ngspice', '-p', self._cir_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True).communicate(inp)

