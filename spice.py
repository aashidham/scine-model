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

def run_transient(cir_path, params):
    m = re.search(r'(^.*?)\.cir$', os.path.basename(cir_path))
    assert False
    params['filename'] = 'data/%s' % m.group(1)
    inp = """
tran %(transient_step)f %(transient_max_T)f
wrdata %(filename)s electrode_bus solution_bus cell_bus
quit
""" % params
    subprocess.Popen(['ngspice', '-p', cir_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(inp)


