import numpy as np

from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from pymoo.util.normalization import normalize

from scripts.results.stamp_results import stamp_gd_results

def get_pareto_front_points(problem, n_points):
    return problem.pareto_front(ref_dirs=n_points)

def get_all_gd_values(results, plus=False):
    # CREA UN GRAFICO DOVE SI MOSTRA, PER OGNI F, (OGNI 1-5 GENERAZIONI), QUANTO VALE LA GD NEL TEMPO  

    # qua devo fare un array con tutti i valori di GD+ per ogni generazione
    # così lo posso passare alla stamp_gd_results

    all_gd_values = {}
    for name, res in results.items():  # Scorro gli algoritmi
        gd_values = []

        
        for n_gen, gen in enumerate(res.history): # Scorro le generazioni
            F = gen.pop.get("F")

            ideal = F.min(axis=0)
            nadir = F.max(axis=0)

            pf = res.problem.pareto_front(F.shape[0])

            pareto_front = (pf - ideal) / (nadir - ideal)
            F_selected = (F - ideal) / (nadir - ideal)

            if plus:
                ind = GDPlus(pareto_front)
            else:
                ind = GD(pareto_front)

            gd_values.append(ind(F_selected))

        all_gd_values[name] = gd_values

    return all_gd_values


def performance(results, name, problem, print_performance=False):
    match name:
        case "hv":
            all_F = np.vstack([res.F for res in results.values()])
            worst = np.max(all_F, axis=0)
            best = np.min(all_F, axis=0)

            ref_point = worst + 0.1 * (worst - best)  # margine 10% (quel 0.1)
            
            ind = HV(ref_point=ref_point)

        case "gd" | "gd+":
            pareto_front_points = get_pareto_front_points(problem, n_points=1000)

            if name == "gd":
                ind = GD(pareto_front_points)
            else:
                ind = GDPlus(pareto_front_points)

    performances = [ind(res.F) for res in results.values()]

    if print_performance:
        for performance, algorithm_name in zip(performances, results.keys()):
            print(f"{name} {algorithm_name}: {performance} ")
    
    return performances