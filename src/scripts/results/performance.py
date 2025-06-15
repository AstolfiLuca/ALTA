import numpy as np

from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from pymoo.util.normalization import normalize

def get_all_gdplus_values(results):
    all_gd_values = {}

    # Scorro gli algoritmi
    for name, res in results.items():  
        gd_values = []
        
        # Scorro le generazioni
        for gen in res.history: 
            F = gen.pop.get("F")
            pf = res.problem.pareto_front(F.shape[0])

            # Normalizzo 
            ideal = F.min(axis=0)
            nadir = F.max(axis=0)

            F_selected = (F - ideal) / (nadir - ideal)
            pareto_front = (pf - ideal) / (nadir - ideal)
            
            # Calcolo GD+
            ind = GDPlus(pareto_front)
            gd_values.append(ind(F_selected))

        # Aggiungo i valori GD+ per l'algoritmo corrente
        all_gd_values[name] = gd_values

    return all_gd_values

def get_all_hv_values(results, verbose=False):
    F = np.vstack([res.F for res in results.values()])

    worst = np.max(F, axis=0)
    best = np.min(F, axis=0)

    ref_point = worst + 0.1 * (worst - best) # margine 10% (quel 0.1)
    
    ind = HV(ref_point=ref_point)

    performances = [ind(res.F) for res in results.values()]

    if verbose:
        for performance, algorithm_name in zip(performances, results.keys()):
            print(f"HV {algorithm_name}: {performance} ")
    
    return performances