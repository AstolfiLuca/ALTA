import numpy as np

from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from pymoo.util.normalization import normalize

from scripts.results.stamp_results import stamp_gd_results

def performance(results, name, pareto_front_points = None, normalized=False, print_performance=False, print_graph=False):
    ind = None

    match name:
        case "hv":
            all_F = np.vstack([res.F for res in results.values()])
            worst = np.max(all_F, axis=0)
            best = np.min(all_F, axis=0)

            ref_point = worst + 0.1 * (worst - best)  # margine 10% (quel 0.1)
            
            ind = HV(ref_point=ref_point)

        case "gd" | "gd+":
            if name == "gd":
                ind = GD(pareto_front_points)
            else:
                ind = GDPlus(pareto_front_points)
            
            
            # CREA UN GRAFICO DOVE SI MOSTRA, PER OGNI F, (OGNI 1-5 GENERAZIONI), QUANTO VALE LA GD NEL TEMPO  

            

            # qua devo fare un array con tutti i valori di GD+ per ogni generazione
            # così lo posso passare alla stamp_gd_results
            


            # for name, res in results.items():
            #     gd_values = []

            # for gen in res.history:
            #     F = gen.pop.get("F")

            #     ideal = F.min(axis=0)
            #     nadir = F.max(axis=0)

            #     pareto_front = (res.problem.pareto_front(F.shape[0]) - ideal) / (nadir - ideal)

            #     F_selected = (F - ideal) / (nadir - ideal)

            #     ind = GDPlus(pareto_front)

            #     gd_values.append(ind(F_selected))

            if print_graph:
                gd_values = []

                for name, res in results.items():
                    gd_values.append(ind(res.F))

                stamp_gd_results(gd_values, list(results.keys()))


    performance = [ind(res.F) for res in results.values()]

    if print_performance:
        for score, algorithm in zip(performance, results.keys()):
            print(f"{name}: {score}, name: {algorithm}")
    
    return performance