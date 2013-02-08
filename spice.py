import os.path
import re
import subprocess


def run(cir_path, params):
    m = re.search(r'(^.*?)\.cir$', os.path.basename(cir_path))
    params['filename'] = 'data/%s' % m.group(1)
    inp = """
tran %(transient_step)f %(transient_max_T)f
wrdata %(filename)s electrode_bus solution_bus cell_bus
quit
""" % params
    subprocess.Popen(['ngspice', '-p', cir_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(inp)


