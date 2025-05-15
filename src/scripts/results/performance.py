import numpy as np

from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from pymoo.util.normalization import normalize

def performance(results, name, pareto_front_problem = None, normalized=False, print_performance=False):
    if name == "hv":
        all_F = np.vstack([res.F for res in results.values()])
        worst = np.max(all_F, axis=0)
        best = np.min(all_F, axis=0)

        ref_point = worst + 0.1 * (worst - best)  # margine 10% (quel 0.1)
        
        ind = HV(ref_point=ref_point)
    else:
        if name == "gd":
            ind = GD(pareto_front_problem)

            # CREA UN GRAFICO DOVE SI MOSTRA, PER OGNI F, (OGNI 1-5 GENERAZIONI), QUANTO VALE LA GD NEL TEMPO  
        
        elif name == "gd+":
            ind = GDPlus(pareto_front_problem)

    performance = [ind(res.F) for res in results.values()]

    if normalized:
        scores = normalize(np.array(performance).reshape(-1, 1)).flatten()
    else:
        scores = performance

    if print_performance:
        for score, algorithm in zip(scores, results.keys()):
            print(f"{name}: {score}, name: {algorithm}")
    
    return scores