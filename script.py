import math
import string

import chosen_strategy
import progression
import model.simple
import spice


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

    #p = fig.add_subplot(2, 2, 1)
    #p.set_title('Electrode length')
    #p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #p.set_ylabel('m')
    #p.plot(T, L_extra, 'r', T, L_intra, 'g', T, L_env, 'b')
    #p.legend(['L_extra', 'L_intra', 'L_env'])

    # The surface area of the membrane enveloping the electrode over
    # time, where the enveloping membrane is a cylinder with diameter
    # = electrode diameter + 100nm, and with length = electrode
    # length.
    A_membrane = [math.pi * (d + 100e-9) * l for l in L_env]

    #p = fig.add_subplot(2, 2, 2)
    #p.set_title('Electrode surface area')
    #p.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #p.set_ylabel('m^2')
    #p.plot(T, A_extra, 'r', T, A_intra, 'g', T, A_env, 'b', T, A_membrane, 'y')
    #p.legend(['A_extra', 'A_intra', 'A_env', 'A_membrane'])

    # The seal resistance over time.
    R_seal = [R_seal_total * neher * l / (d * math.pi) for l in L_env]

    for i in range(len(T)):
        cir_path = model.generate(
            'spike.short.dat',
            'generated/model1_L@%s_d@%s_deformability@%s_neher@%s_Rpene@%s_Rseal@%s_compartments@%s_t@%s.cir' % (L, d, deformability, neher, R_pene, R_seal_total, N_compartments, T[i]),
            {
                'N_compartments': N_compartments,
                'alpha': 0.5,
                'k': 0.14,
                'R_seal': R_seal[i],
                'A_intra': A_intra[i],
                'A_env': A_env[i],
                'A_membrane': A_membrane[i],
                'A_extra': A_extra[i],
                'R_pene': R_pene
                }
            )
        #spice.run_ac(cir_path, {
        #        'exponent_low': -5,
        #        'exponent_high': 5
        #        })
        chosen_strategy(spice.TransientSpice({'circuit': cir_path}, {'data': 'nang'}, 1e-5, 0.005))


#fig = plt.figure()
#for R_pene in progression.Linear(1e3, 1e13, 10):
#    for deformability in [10000, 1000, 100, 10, 1]:
#        for R_seal_total in progression.Linear(1e7, 1e12, 10):
#insert_scine(2000e-9, 200e-9, 300e-9, deformability, 0.2, R_pene, R_seal_total, 2, model.simple)
insert_scine(2000e-9, 200e-9, 300e-9, 5, 0.2, 1e10, 1e12, 2, model.simple)

#fig.show()
#while True:
#    pass
