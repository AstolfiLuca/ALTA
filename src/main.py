from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.problems import get_problem

# --- Majority Judgment --- 
from scripts.MJ.standard_majority_judgment import majority_judgment as standard_MJ

# --- New Majority Judgment---
from scripts.MJ.pile_majority_judgment import majority_judgment as pile_MJ
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
    
def print_results(results, title="default_title", scatter=True, radviz=True, save_file=False):
    assert results, "Results Dict is Empty"
    
    assert (scatter or radviz), "It is necessary to choose a specific plot"

    import matplotlib
    matplotlib.use('Qt5Agg')  # Usa un backend interattivo
    import matplotlib.pyplot as plt
     
    n_res = len(results)

    import colorsys
    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]

    if scatter:
        plot = Scatter(title=title, legend=True)

        for index, (name, result) in zip(range(n_res), results.items()):
            plot.add(result.F, color=colors[index], edgecolor="black", label=name)

        if save_file:
            plot.save("scatter")
        
        plot.show()
        

    if radviz and n_res > 1:
        from pymoo.visualization.radviz import Radviz
        from pymoo.util.normalization import normalize

        F_normalizer = list(results.values())[0]
        
        F_normalized = []
        for res_F in results.values():
            F_normalized.append(normalize(res_F.F, xl=F_normalizer.F.min(axis=0), xu=F_normalizer.F.max(axis=0)))


        plot = Radviz(title=title, legend=True)
        for index, name, F_norm in zip(range(n_res), results.keys(), F_normalized):
            plot.add(F_norm, label=name, color=colors[index])

        if save_file:
            plot.save("radvis")
        
        plot.show()

# W.I.P.
def test_problems(algorithms = [], problem_names = [], n_objs = [], n_gens = []):
    assert algorithms, "Missing algorithms"
    assert n_gens, "Missing number of generations"
    assert problem_names, "Missing problem names"
    assert n_obj, "Missing number of objective function"
    
    for problem_name in problem_names:
        for n_obj in n_objs:
            for n_gen in n_gens:
                termination = get_termination("n_gen", n_gen)
                
                problem = get_problem(problem_name, n_obj=n_obj)
                
                results = get_results(problem, algorithms, termination)

                print_results(results, title=f"{problem_name}, {n_obj}, {n_gen}")


if __name__ == "__main__":
    pop_size = 100
    n_gen = 200
    problem_name = "dtlz1"

    problem = get_problem(problem_name, n_obj=5)
    
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
    #test_problems([50, 200], )

    




    