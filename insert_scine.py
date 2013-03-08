import json
import math

import spice
import the_platform


def insert_scine(model, **params):

    # The length of the electrode inside of, enveloped by, and outside
    # of the cell over time.
    # Kenv / Kpene = params['Deform'] , Kenv + Kpene = 1
    L_intra = []
    L_env = []
    L_extra = []
    T = []
    t = 0
    k_env = params['Deform'] / float(1 + params['Deform'])
    k_pene = 1 - k_env
    while True:
        L_env.append(k_env * t)
        L_intra.append(k_pene * t)
        L_extra.append(params['Length'] - t)
        T.append(t)
        assert L_extra[-1] >= 0, (t, L_extra[-1])
        if L_extra[-1] == 0:
            break
        t += params['Length'] / params['Nsteps']
        t = min(t, params['Length'])

    # The surface area of the electrode inside of, enveloped by, and
    # outside of the cell over time.
    cap = math.pi * pow(params['Dia'] / 2.0, 2)
    A_per_L = math.pi * params['Dia']
    A_intra = [cap + (A_per_L * l) if (l > 0) and (params['Deform'] < 1000) else 0 for l in L_intra]
    A_env = [A_per_L * l if l > 0 else 0 for l in L_env]
    A_extra = [A_per_L * l for l in L_extra]

    # The surface area of the membrane enveloping the electrode over
    # time, where the enveloping membrane is a cylinder with diameter
    # = electrode diameter + 100nm, and with length = electrode
    # length.
    A_membrane = [math.pi * (params['Dia'] + 100e-9) * l for l in L_env]

    # The seal resistance over time.
    R_seal_total = [params['Neher'] * l / params['Dia'] for l in L_env]
    R_seal = [r / params['compartments'] for r in R_seal_total]

    for i in range(len(T)):

        # Save derived parameters
        the_platform.set_path('t=%i' % i)
        derived_params = {
            'R_seal_i': R_seal[i],
            'A_intra': A_intra[i],
            'A_env': A_env[i],
            'A_membrane': A_membrane[i],
            'A_extra': A_extra[i],
            'L_intra': L_intra[i],
            'L_env': L_env[i],
            'L_extra': L_extra[i],
            't': T[i],
            'Rmembrane_i': params['compartments'] / (params['Mem_cond'] * A_membrane[i]) if A_membrane[i] > 0 else 1e20,
            'Cmembrane_i': (A_membrane[i] * 0.01) / params['compartments'] if A_membrane[i] > 0 else 1e-20,
            }
        print derived_params
        f = open(the_platform.file('derived_params.json'), 'w')
        f.write(json.dumps(derived_params))
        f.close()

        # Mix together all params, the model will need them all. And
        # do the analysis.
        p = dict(params)
        for k, v in derived_params.items():
            assert k not in p
            p[k] = v
        cir_path = model.generate('data/short-spike', the_platform.file('model1.cir'), p)
        spice.ac_analysis(cir_path, -5, 5)
