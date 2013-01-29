import math
import matplotlib.pyplot as plt
import string

def insert_scine(tmpl, fig, L, d, k_pene, k_deform):

    # Time goes from 0 to however long
    steps = 1000
    T = [(L / (k_pene + k_deform)) * (i / float(steps)) for i in range(steps)]

    # The length of the electrode inside of, enveloped by, and outside
    # of the cell over time.
    L_intra = [k_pene * t for t in T]
    L_env = [k_deform * t for t in T]
    L_extra = [L - intra - env for intra, env in zip(L_intra, L_env)]

    p = fig.add_subplot(2, 2, 1)
    p.set_title('Electrode length')
    p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    p.set_ylabel('m')
    p.plot(T, L_extra, 'r', T, L_intra, 'g', T, L_env, 'b')
    p.legend(['L_extra', 'L_intra', 'L_env'])

    # The surface area of the electrode inside of, enveloped by, and
    # outside of the cell over time.
    cap = math.pi * pow(d / 2.0, 2)
    A_per_L = math.pi * d
    A_intra = [(cap if l > 0 else 0) + (A_per_L * l) for l in L_intra]
    A_env = [A_per_L * l for l in L_env]
    A_extra = [A_per_L * l for l in L_extra]

    # The surface area of the membrane enveloping the electrode over
    # time, where the enveloping membrane is a cylinder with diameter
    # = electrode diameter + 100nm, and with length = electrode
    # length.
    A_membrane = [math.pi * (d + 100e-9) * l for l in L_env]

    p = fig.add_subplot(2, 2, 2)
    p.set_title('Electrode surface area')
    p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    p.set_ylabel('m^2')
    p.plot(T, A_extra, 'r', T, A_intra, 'g', T, A_env, 'b', T, A_membrane, 'y')
    p.legend(['A_extra', 'A_intra', 'A_env', 'A_membrane'])

    # The seal resistance over time.
    R_seal = [10e9 * l / (d * math.pi) for l in L_env]

    #eei_circuit(q0=50000, n=0.5)

tmpl = string.Template(open('eei.cir', 'r').read())
def eei_circuit(**kwargs):
    fn = ''
    for k, v in kwargs.items():
        fn = '%s%s_%s' % (fn + '__' if fn else '', k, str(v))
    open('eei/%s.cir' % fn, 'w').write(tmpl.substitute(kwargs))

fig = plt.figure()
insert_scine(tmpl, fig, 5000e-9, 500e-9, 2, 1)
fig.show()
raw_input('enter to continue')
