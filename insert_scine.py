import math

import spice
import the_platform


def insert_scine(L, t_step, d, deformability, neher, R_pene, R_seal_total, N_compartments, model):

    # The length of the electrode inside of, enveloped by, and outside
    # of the cell over time.
    # Kenv / Kpene = deformability , Kenv + Kpene = 1
    L_intra = []
    L_env = []
    L_extra = []
    T = []
    t = 0
    k_env = deformability / float(1 + deformability)
    k_pene = 1 - k_env
    while True:
        L_env.append(k_env * t)
        L_intra.append(k_pene * t)
        L_extra.append(L - t)
        T.append(t)
        if L_extra[-1] <= 0:
            L_env.pop()
            L_intra.pop()
            L_extra.pop()
            T.pop()
            break
        t += t_step

    # The surface area of the electrode inside of, enveloped by, and
    # outside of the cell over time.
    cap = math.pi * pow(d / 2.0, 2)
    A_per_L = math.pi * d
    A_intra = [cap + (A_per_L * l) if (l > 0) and (deformability < 1000) else 0 for l in L_intra]
    A_env = [A_per_L * l if l > 0 else 0 for l in L_env]
    A_extra = [A_per_L * l for l in L_extra]

    # The surface area of the membrane enveloping the electrode over
    # time, where the enveloping membrane is a cylinder with diameter
    # = electrode diameter + 100nm, and with length = electrode
    # length.
    A_membrane = [math.pi * (d + 100e-9) * l for l in L_env]

    # The seal resistance over time.
    R_seal = [R_seal_total * neher * l / (d * math.pi) for l in L_env]

    for i in range(len(T)):
        the_platform.set_path('t=%i' % i)
        model_params = {
            'N_compartments': N_compartments,
            'alpha': 0.5,
            'k': 0.14,
            'R_seal': R_seal[i],
            'A_intra': A_intra[i],
            'A_env': A_env[i],
            'A_membrane': A_membrane[i],
            'A_extra': A_extra[i],
            'R_pene': R_pene,
            'L': L,
            'd': d,
            'deformability': deformability,
            'neher': neher,
            'R_seal_total': R_seal_total,
            'N_compartments': N_compartments,
            't': T[i]
            }
        cir_path = model.generate(
            'data/short-spike',
            the_platform.file('model1_L@%s_d@%s_deformability@%s_neher@%s_Rpene@%s_Rseal@%s_compartments@%s_t@%s.cir' % (L, d, deformability, neher, R_pene, R_seal_total, N_compartments, T[i])),
            dict(model_params)
            )
        spice.ac_analysis(cir_path, -5, 5)
