import platform


platform.install()
platform.Platform.set_root('all')


import insert_scine
import model.simple
import progression


i = 0
for deformability in [10000, 1000, 100, 10, 1]:
    i += 1
    platform.Platform.set_root('all/trial=%i' % i)
    params = {
        'Length': 2000e-9,
        'Nsteps': 10,
        'Dia': 300e-9,
        'Deform': deformability,
        'Neher': 1e9,
        'Mem_cond': 10,
        'compartments': 2,
        'CStray': 1e-12,
        'RStray': 1e12,
        'Cwholecell': 2e-10,
        'Rwholecell': 1e8,
        'CPE_alpha': 0.5,
        'CPE_k': 0.159,
        'R_pene': 1e9,
        'Rbath': 200
    }
    insert_scine.insert_scine(model.simple, **params)
