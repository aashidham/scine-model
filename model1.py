import re
import subprocess
import tempfile


def make(data):

    # Run gnetlist to create a netlist from the model1 schematic.
    def run_netlister(fn):
        _, netlist_fn = tempfile.mkstemp()
        p = subprocess.Popen(['gnetlist', '-n', '-g', 'spice', fn, '-o', netlist_fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = p.communicate()
        assert err == ''
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
    Rseali = get_component('Rseali', strip=True)
    Rmembranei = get_component('Rmembranei', strip=True)
    Cmembranei = get_component('Cmembranei', strip=True)
    Xsheathedcpei = get_component('Xsheathedcpei', strip=True)
    Rpene = get_component('Rpene')
    Xextracpe = get_component('Xextracpe')

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
    for i, n in enumerate(netlist):
        missing = '<No valid value attribute found>'
        if n.endswith(missing):
            c = n.split(' ')[0]
            m = re.search(r'^(.*?)_(\d+)$', c)
            if m:
                v = data[(m.group(1),)](int(m.group(2)))
            else:
                v = data[c]
            netlist[i] = n.replace(missing, str(v))

    # Add the cell voltage model.
    netlist.append('\n.model cell_potential filesource (file="spike.dat", amploffset=[0], amplscale=[1])')

    f = open('out.cir', 'w')
    f.write('\n'.join(netlist))
    f.close()

make({
        ('Rmembranei',): lambda i: 0.14 + i,
        ('Cmembranei',): lambda i: 0.14 + i,
        ('Rseali',): lambda i: 0.65 + i,
        ('Xsheathedcpei',): lambda i: 0.66 + i,
        'Xextracpe': 5,
        'Xintracpe': 5,
        'Rwholecell': 5,
        'Cwholecell': 5
        })
