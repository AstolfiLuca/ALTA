import matplotlib
matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt

from pymoo.termination import get_termination
from pymoo.problems import get_problem


# --- Test PyMoo ---
from test.test import *


def get_results(problem, algorithms, termination, seed=1):
    from pymoo.optimize import minimize
    results = {}

    for name, algorithm in algorithms.items():
        results[name] = minimize(
            problem, 
            algorithm, 
            termination, 
            seed=seed
        )

    return results
    
def print_results(results, title="default_title", scatter=False, radviz=True, multi_problems=False, save_file=False):
    assert results, "Results Dict is Empty"
    
    assert (scatter or radviz), "It is necessary to choose a specific plot"
    
    n_res = len(results)

    import colorsys
    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]

    if scatter:
        from pymoo.visualization.scatter import Scatter

        plot = Scatter(title=title, legend=True)

        for index, (name, result) in zip(range(n_res), results.items()):
            plot.add(result.F, color=colors[index], edgecolor="black", label=name)

        if save_file:
            plot.save("scatter")
        
        

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

    plt.tight_layout()

    if not multi_problems:
        plot.show()

def test_all_problems(algorithms = {}, problem_names = [], n_objs = [], n_gens = [], scatter=False, radviz=True, save_file=False):
    assert algorithms, "Missing algorithms"
    assert problem_names, "Missing problem names"
    assert n_objs, "Missing number of objective function"
    assert n_gens, "Missing number of generations"
    
    fig, axes = plt.subplots(len(problem_names), len(n_objs), figsize=(5 * len(n_objs), 5 * len(problem_names)))

    # Se c'è solo un'asse, metti in lista
    if len(problem_names) == 1:
        axes = [axes]

    all_results = []
    for problem_name in problem_names:
        for n_obj in n_objs:
            for n_gen in n_gens:
                termination = get_termination("n_gen", n_gen)
                
                problem = get_problem(problem_name, n_obj=n_obj)
                
                results = get_results(problem, algorithms, termination)

                print_results(results, title=f"{problem_name}, {n_obj}, {n_gen}", scatter=scatter, radviz=radviz, save_file=save_file)

    plt.show()


if __name__ == "__main__":
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.algorithms.moo.nsga3 import NSGA3
    from pymoo.algorithms.moo.rvea import RVEA
    from pymoo.util.ref_dirs import get_reference_directions
    from scripts.pymoo.mj_survival import MJ_Survival

    pop_size = 100
    
    ref_dirs = get_reference_directions("das-dennis", n_dim=3, n_partitions=12)

    algorithms = {
        "pile_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=True)),
        "standard_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=False)),
        "NSGA2": NSGA2(pop_size=pop_size),
        # "nsga3": NSGA3(pop_size=pop_size, ref_dirs=ref_dirs),
        # "rvea": RVEA(pop_size=pop_size, ref_dirs=ref_dirs)
    }

    #n_gen = 200
    #problem_name = "dtlz1"
    #problem = get_problem(problem_name, n_obj=5)
    # termination = get_termination("n_gen", n_gen)
    # results = get_results(problem, algorithms, termination)
    # print_results(results, title=problem_name, scatter=False)
    
    problems = [f"dtlz{i}" for i in range(1, 8)]
    n_objs = [3, 5, 9]
    n_gens = [50, 200, 400]

    test_all_problems(algorithms, problems, n_objs, n_gens, radviz=True)


    