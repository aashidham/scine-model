import re
import subprocess
import tempfile

import ladder


def generate(k, R_seal, A_intra, A_env, A_membrane, A_extra, **kwargs):

    # Run gnetlist to create a netlist from the model1 schematic.
    def run_netlister(fn):
        _, netlist_fn = tempfile.mkstemp()
        p = subprocess.Popen(['gnetlist', '-n', '-g', 'spice', fn, '-o', netlist_fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print netlist_fn
        _, err = p.communicate()
        assert err == '', err
        return netlist_fn
    model1_fn = run_netlister('schematics/model1.sch')

    # Find and repeat the compartment motif.

    netlist = filter(lambda l: l != '.END', open(model1_fn).read().split('\n'))
    def get_component(name, strip=False):
        for n in netlist:
            ns = n.split()
            if ns[0] == name:
                if strip:
                    netlist.remove(n)
                return ns
        raise Exception('component not found');
    Rseali = get_component('Rseal_i', strip=True)
    Rmembranei = get_component('Rmembrane_i', strip=True)
    Cmembranei = get_component('Cmembrane_i', strip=True)
    Xsheathedcpei = get_component('Xsheathedcpe_i', strip=True)

    def place(component, x, i, o):
        c = list(component)
        c[0] += '_%s' % x
        c[1] = str(i)
        c[2] = str(o)
        netlist.append(' '.join(c))
    Rseali_out = 'solution_bus'
    N_compartments = 2
    for i in range(N_compartments):
        if i == N_compartments - 1:
            compartment = 'Rpene_bus'
        else:
            compartment = 'compartment_%s' %i 
        place(Rseali, i, compartment, Rseali_out)
        Rseali_out = compartment
        place(Xsheathedcpei, i, Rseali_out, 'electrode_bus')
        place(Rmembranei, i, Rseali_out, 'cell_bus')
        place(Cmembranei, i, Rseali_out, 'cell_bus')
    
    # Find variables.
    S_tm = 0.1
    values = {
        'Rwholecell': 1,
        'Cwholecell': 1,
        'Xextracpe': k * A_extra,
        'Xintracpe': k * A_intra,
        'Xsheathedcpe_i': lambda _: '',
        'Rmembrane_i': lambda _: N_compartments / (S_tm * A_membrane),
        'Cmembrane_i': lambda _: (A_membrane * 0.01) / N_compartments,
        'Rseal_i': lambda _: R_seal / N_compartments
        }
    for i, n in enumerate(netlist):
        missing = '<No valid value attribute found>'
        if n.endswith(missing):
            c = n.split(' ')[0]
            m = re.search(r'^(.*?)_(\d+)$', c)
            if m:
                v = values[m.group(1)](int(m.group(2)))
            else:
                v = values[c]
            netlist[i] = n.replace(missing, str(v))

    # Add the cell voltage model.
    netlist.append('\n.model cell_potential filesource (file="spike.dat", amploffset=[0], amplscale=[1])')

    f = open('out.cir', 'w')
    f.write('\n'.join(netlist))
    f.close()
