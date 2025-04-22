import numpy as np


from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.normalization import normalize

def get_ref_point(results):
    Fs = [res.F for res in results.values()]
    all_solutions = np.vstack(Fs)

    worst = np.max(all_solutions, axis=0)
    best = np.min(all_solutions, axis=0)

    ref_point = worst + 0.1 * (worst - best)  # margine 10% (quel 0.1)

    return ref_point

def hv_performance(results, normalized_hv=False, print_performance=False):
    ref_point = get_ref_point(results)

    ind = HV(ref_point=ref_point)

    performance = [ind(res.F) for res in results.values()]

    if normalized_hv:
        scores = normalize(np.array(performance).reshape(-1, 1)).flatten()  # Normalizza i punteggi HV
    else:
        scores = performance

    if print_performance:
        for score, name in zip(scores, results.keys()):
            print(f"hv: {score}, name: {name}")
    
    return scores

def gd_performance(results, plus=False, normalized_gd=False, print_performance=False):
    ref_point = get_ref_point(results)

    if plus:
        ind = GDPlus(ref_point)
    else:
        ind = GD(ref_point)

    performance = [ind(res.F) for res in results.values()]

    if normalized_gd:
        scores = normalize(np.array(performance).reshape(-1, 1)).flatten()  # Normalizza i punteggi HV
    else:
        scores = performance
    
    if print_performance:
        for score, name in zip(scores, results.keys()):
            print(f"hv: {score}, name: {name}")