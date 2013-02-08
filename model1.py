import re
import subprocess
import tempfile

import ladder


def generate(filename, alpha, k, R_seal, R_pene, A_intra, A_env, A_membrane, A_extra, data_path):

    # Run gnetlist to create a netlist from the model1 schematic.
    def run_netlister(fn):
        _, netlist_fn = tempfile.mkstemp()
        p = subprocess.Popen(['gnetlist', '-n', '-g', 'spice', fn, '-o', netlist_fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    
    # Make the CPEs. TODO make alpha and d_p free params.
    path, extra_cpe = ladder.generate(50, alpha, k / (A_extra + 1e-30), 'generated')
    netlist.insert(1, '.include %s' % path)
    path, intra_cpe = ladder.generate(50, alpha, k / (A_intra + 1e-30), 'generated')
    netlist.insert(1, '.include %s' % path)
    path, sheathed_cpe = ladder.generate(50, alpha, k / (A_env + 1e-30), 'generated')
    netlist.insert(1, '.include %s' % path)

    netlist.insert(0, '* alpha=%s k=%s R_seal=%s A_intra=%s A_env=%s A_membrane=%s A_extra=%s' % (alpha, k, R_seal, A_intra, A_env, A_membrane, A_extra))

    # Find variables.
    S_tm = 0.1
    values = {
        # TODO make these into free params.
        'Rpara': 1e12,
        'Cpara': 4e-12,
        'Rpene': R_pene,
        'Rwholecell': 1e8,
        'Cwholecell': 2e-10,
        'Rsoln': 200,
        
        'Xextracpe': extra_cpe,
        'Xintracpe': intra_cpe,
        'Xsheathedcpe_i': lambda _: sheathed_cpe,
        'Rmembrane_i': lambda _: N_compartments / (S_tm * A_membrane) if A_membrane > 0 else 1e20,
        'Cmembrane_i': lambda _: (A_membrane * 0.01) / N_compartments if A_membrane > 0 else 1e-20,
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

    # Add the cell voltage model, and fixup the connections for the
    # Acell.
    Acell = get_component('Acell', strip=True)
    assert len(Acell) == 4
    netlist.append('%s %%vd([%s, %s]) %s' % tuple(Acell))
    netlist.append('\n.model cell_potential filesource (file="%s", amploffset=[0], amplscale=[1])' % data_path)

    f = open(filename, 'w')
    f.write('\n'.join(netlist))
    f.close()

    return filename
