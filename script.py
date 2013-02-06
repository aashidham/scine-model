import math
import matplotlib.pyplot as plt
import string

import model1
import util


class LinearProgression(object):

    def __init__(self, low, high, n_samples):
        assert high > low
        self._low = float(low)
        self._high = float(high)
        assert (type(n_samples) == int) and (n_samples > 1)
        self._n_samples = n_samples
        self._i = 0

    def __iter__(self):
        return self

    def next(self):
        if self._i < self._n_samples:
            v = (self._i * (self._high - self._low) / (self._n_samples - 1)) + self._low
            self._i += 1
            return v
        else:
            raise StopIteration()


def insert_scine(fig, L, d, deformability, model):

    # The length of the electrode inside of, enveloped by, and outside
    # of the cell over time.
    # Kenv / Kpene = deformability , Kenv + Kpene = 1
    assert (deformability > 0) and (deformability < 1)
    L_intra = []
    L_env = []
    L_extra = []
    T = []
    t = 0
    while True:
        k_env = deformability / (1 + deformability)
        L_env.append(k_env * t)
        L_intra.append((1 - k_env) * t)
        L_extra.append(L - t)
        T.append(t)
        if L_extra[-1] <= 0:
            L_env.pop()
            L_intra.pop()
            L_extra.pop()
            T.pop()
            break
        t += 1000e-9 # TODO HELP 1e-9

    # The surface area of the electrode inside of, enveloped by, and
    # outside of the cell over time.
    cap = math.pi * pow(d / 2.0, 2)
    A_per_L = math.pi * d
    A_intra = [cap + (A_per_L * l) for l in L_intra]
    A_env = [A_per_L * l for l in L_env]
    A_extra = [A_per_L * l for l in L_extra]

    p = fig.add_subplot(2, 2, 1)
    p.set_title('Electrode length')
    p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    p.set_ylabel('m')
    p.plot(T, L_extra, 'r', T, L_intra, 'g', T, L_env, 'b')
    p.legend(['L_extra', 'L_intra', 'L_env'])

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

    # The seal resistance over time. TODO We'll insert a free
    # parameter here later. neher
    R_seal = [10e9 * l / (d * math.pi) for l in L_env]

    for i in range(len(T)):
        spice = model.generate(
            'generated/model1_L@%s_d@%s_deformability@%s_t@%s.cir' % (L, d, deformability, T[i]),
            # TODO alpha, k should be free params
            0.5, 10,
            R_seal[i],
            A_intra[i],
            A_env[i],
            A_membrane[i],
            A_extra[i]
            )
        #spice.run()


import model1

fig = plt.figure()
insert_scine(fig, 5000e-9, 500e-9, 0.5, model1)
#fig.show()
#while True:
#    pass
