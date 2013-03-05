import os
import re
import subprocess
import tempfile

import model.ladder_cpe


def generate(neuron_path, filename, params):

    # Run gnetlist to create a netlist from the schematic.
    def run_netlister(fn):
        f, netlist_fn = tempfile.mkstemp()
        os.close(f)
        p = subprocess.Popen(['gnetlist', '-n', '-g', 'spice', fn, '-o', netlist_fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        s, err = p.communicate()
        p.wait()
        assert err == '', err
        return netlist_fn
    model_fn = run_netlister('model/simple.sch')

    # Find and repeat the compartment motif.

    netlist = filter(lambda l: l != '.END', open(model_fn).read().split('\n'))
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
    for i in range(params['N_compartments']):
        if i == params['N_compartments'] - 1:
            compartment = 'Rpene_bus'
        else:
            compartment = 'compartment_%s' %i 
        place(Rseali, i, compartment, Rseali_out)
        Rseali_out = compartment
        place(Xsheathedcpei, i, Rseali_out, 'electrode_bus')
        place(Rmembranei, i, Rseali_out, 'cell_bus')
        place(Cmembranei, i, Rseali_out, 'cell_bus')

    # Make the CPEs.
    netlist.extend([''] + model.ladder_cpe.generate('extra_cpe', 50, params['alpha'], params['k'] / (params['A_extra'] + 1e-30)))
    netlist.extend([''] + model.ladder_cpe.generate('intra_cpe', 50, params['alpha'], params['k'] / (params['A_intra'] + 1e-30)))
    netlist.extend([''] + model.ladder_cpe.generate('sheathed_cpe', 50, params['alpha'], params['k'] / (params['A_env'] + 1e-30)))

    # Comment.
    netlist.insert(0, '* alpha=%s k=%s R_seal=%s A_intra=%s A_env=%s A_membrane=%s A_extra=%s' % (
            params['alpha'], params['k'], params['R_seal'], params['A_intra'], params['A_env'], params['A_membrane'], params['A_extra']))

    # Find variables.
    S_tm = 0.1
    values = {
        'Rpara': 1e12,
        'Cpara': 4e-12,
        'Rpene': params['R_pene'],
        'Rwholecell': 1e8,
        'Cwholecell': 2e-10,
        'Rsoln': 200,        
        'Xextracpe': 'extra_cpe',
        'Xintracpe': 'intra_cpe',
        'Xsheathedcpe_i': lambda _: 'sheathed_cpe',
        'Rmembrane_i': lambda _: params['N_compartments'] / (S_tm * params['A_membrane']) if params['A_membrane'] > 0 else 1e20,
        'Cmembrane_i': lambda _: (params['A_membrane'] * 0.01) / params['N_compartments'] if params['A_membrane'] > 0 else 1e-20,
        'Rseal_i': lambda _: params['R_seal'] / params['N_compartments']
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
    netlist.append('Vcell %s %s 1v ac' % tuple(Acell)[1:3])
    #netlist.append('%s %%vd([%s, %s]) %s' % tuple(Acell))  # ... DC

    netlist.append('\n.model cell_potential filesource (file="%s", amploffset=[0], amplscale=[1])' % neuron_path)

    f = open(filename, 'w')
    f.write('\n'.join(netlist))
    f.close()

    return filename
