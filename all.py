import chosen_platform
import insert_scine
import model.simple
import progression


for R_pene in progression.Linear(1e3, 1e13, 2): #, 10):
    for deformability in [10000]: #, 1000, 100, 10, 1]:
        for R_seal_total in progression.Linear(1e7, 1e12, 2): # 10):
            insert_scine.insert_scine(2000e-9, 200e-9, 300e-9, deformability, 0.2, R_pene, R_seal_total, 2, model.simple)
