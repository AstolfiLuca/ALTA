from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.problems import get_problem

# --- Majority Judjment --- 
from scripts.MJ.standard_majority_judjment import majority_judgment as standard_MJ

# --- New Majority Judjment---
from scripts.MJ.pile_majority_judjment import majority_judment as pile_MJ
from scripts.pymoo.mj_implementation.mj_survival import ParetoSurvival

# --- Test PyMoo ---
from test.test import get_phi_matrix_1, get_phi_matrix_2
from test.pymoo.multi_obj_problem import MultiObjectiveProblem


def get_results(problem, algorithms, termination, seed=1):
    results = {}

    for name, algorithm in algorithms.items():
        results[name] = minimize(
            problem, 
            algorithm, 
            termination, 
            seed=seed
        )

    return results
    
def print_results(results, title="default_title", scatter=True, radvis=True):
    assert results, "Results Dict is Empty"
    
    assert (scatter or radvis), "It is necessary to choose a specific plot"
     
    n_res = len(results)

    import colorsys
    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]

    if scatter:
        plot = Scatter(title=title)

        for index, (name, result) in zip(range(n_res), results.items()):
            plot.add(result.F, color=colors[index], edgecolor="black", label=name)

        plot.show()

    if radvis and n_res > 1:
        from pymoo.visualization.radviz import Radviz
        from pymoo.util.normalization import normalize

        F_normalizer = list(results.values())[0]
        
        F_normalized = []
        for res_F in results.values():
            F_normalized.append(normalize(res_F.F, xl=F_normalizer.F.min(axis=0), xu=F_normalizer.F.max(axis=0)))


        plot = Radviz()
        for index, name, F_norm in zip(range(n_res), results.keys(), F_normalized):
            plot.add(F_norm, label=name, color=colors[index])

        plot.show()

if __name__ == "__main__":
    pop_size = 100
    n_gen = 50
    problem_name = "dtlz1"

    problem = get_problem(problem_name)
    
    algorithm_pile_MJ = NSGA2(
        pop_size=pop_size,
        survival=ParetoSurvival(use_MJ_pile=True)
    )

    algorithm_standard_MJ = NSGA2(
        pop_size=pop_size,
        survival=ParetoSurvival(use_MJ_pile=False)
    )
    
    algorithm_NSGA2 = NSGA2(
        pop_size=pop_size
    )

    algorithms = {
        "pile_MJ": algorithm_pile_MJ,
        "standard_MJ": algorithm_standard_MJ,
        "NSGA2": algorithm_NSGA2
    }

    termination = get_termination("n_gen", n_gen)

    results = get_results(problem, algorithms, termination)

    print_results(results, title=problem_name, scatter=False)

    




    