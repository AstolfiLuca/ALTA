import matplotlib
matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt

from pymoo.optimize import minimize

from pymoo.termination import get_termination
from pymoo.problems import get_problem

from pymoo.indicators.hv import HV

import colorsys
from pymoo.visualization.scatter import Scatter
from pymoo.visualization.radviz import Radviz
from pymoo.util.normalization import normalize
import numpy as np

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA
from pymoo.util.ref_dirs import get_reference_directions

from scripts.pymoo_survival import MJ_Survival
from test.test_phi_matrices import *

def get_results(problem, algorithms, termination, hv=False, save_history=False, seed=1):
    results = {}

    F = []

    for name, algorithm in algorithms.items():
        result = minimize(
            problem, 
            algorithm, 
            termination, 
            save_history=save_history,
            seed=seed
        )

        if hv:
            F.append(result.F)
        
        results[name] = result

    if hv:
        all_solutions = np.vstack(F)
        worst = np.max(all_solutions, axis=0)
        ref_point = worst + 0.1 * (worst - np.min(all_solutions, axis=0))  # margine 10% (quel 0.1)
        ind = HV(ref_point=ref_point)
        
        return results, ind
    else:    
        return results

    
def print_results(results, title="default_title", scatter=False, radviz=False, ax=None, save_file=False):
    assert results, "Results Dict is Empty"  
    assert scatter or radviz, "It is necessary to choose a specific plot"
    
    n_res = len(results)

    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]

    if scatter:
        plot = Scatter(title=title, legend=True)

        for index, (name, result) in enumerate(results.items()):
            plot.add(result.F, color=colors[index], edgecolor="black", label=name)

        if save_file:
            plot.save("scatter")

    if radviz and n_res > 1:
        plot = Radviz(title=title, legend=True)

        all_F = np.concatenate([res.F for res in results.values()], axis=0)
        xl = all_F.min(axis=0)
        xu = all_F.max(axis=0)
        F_normalized = [normalize(res.F, xl=xl, xu=xu) for res in results.values()]
        
        for index, (name, F_norm) in enumerate(zip(results.keys(), F_normalized)):
            plot.add(F_norm, label=name, color=colors[index])
        
        if save_file:
            plot.save("radvis")
    
    if ax:
        plot.ax = ax
        plot.do()
    else:
        plot.show()

def test_dltz(algorithms, n_gen = 200, n_obj=5, n = range(7), tight_layout=False):
    fig, axs = plt.subplots(2, 4, figsize=(14, 10))
    fig.suptitle(f"DLTZ | n_gen={n_gen} | n_obj={n_obj}", fontsize=16)
    
    axs = axs.flatten()

    F = []

    for i in range(7):
        if i + 1 not in n:
            fig.delaxes(axs[i])
            continue

        problem_name = f"dtlz{i + 1}"
        print(problem_name)
        
        problem = get_problem(problem_name, n_obj=n_obj)
        termination = get_termination("n_gen", n_gen)

        results = get_results(problem, algorithms, termination)

        print_results(results, title=problem_name, radviz=True, fig=fig, ax=axs[i])

    fig.delaxes(axs[7])

    if tight_layout:
        plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    pop_size = 100
    
    # ref_dirs = get_reference_directions("das-dennis", n_dim=5, n_partitions=3)

    algorithms = {
        "standard_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=False)),
        "pile_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=True)),
        "NSGA2": NSGA2(pop_size=pop_size),
        # "NSGA3": NSGA3(pop_size=pop_size, ref_dirs=ref_dirs),
        # "RVEA": RVEA(pop_size=pop_size, ref_dirs=ref_dirs)
    }


    n = [1, 3, 4]
    n_gen = 100
    n_obj = 3

    results, hv = get_results(get_problem("dtlz1"), algorithms, get_termination("n_gen", n_gen), hv=True)

    for name, res in results.items():
        print(f"hv: {hv(res.F)}, name: {name}")

    #test_dltz(algorithms, n_gen=n_gen, n_obj=n_obj, n=n, tight_layout=True)


    