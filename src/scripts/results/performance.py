import numpy as np

from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.normalization import normalize

def performance(results, name, normalized=False, print_performance=False):
    all_F = np.vstack([res.F for res in results.values()])
    worst = np.max(all_F, axis=0)
    best = np.min(all_F, axis=0)

    ref_point = worst + 0.1 * (worst - best)  # margine 10% (quel 0.1)

    metrics = {
        "hv": HV(ref_point=ref_point),
        "gd": GD(all_F), # WIP
        "gd+": GDPlus(all_F) # WIP
    }

    ind = metrics[name]

    performance = [ind(res.F) for res in results.values()]

    if normalized:
        scores = normalize(np.array(performance).reshape(-1, 1)).flatten()
    else:
        scores = performance

    if print_performance:
        for score, algorithm in zip(scores, results.keys()):
            print(f"{name}: {score}, name: {algorithm}")
    
    return scores