import matplotlib
matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt

from pymoo.termination import get_termination
from pymoo.problems import get_problem

from test.phi_matrices import *
from scripts.results.stamp_results import stamp_results
from scripts.results.get_results import get_results

def test_wfg(algorithms, n_gen = 200, n_obj=5, n_var=6, n = range(9), tight_layout=False):
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    axs = axs.flatten()
    fig.suptitle(f"WFG | n_gen={n_gen} | n_obj={n_obj}", fontsize=16)

    for i in range(9):
        if i + 1 not in n:
            fig.delaxes(axs[i])
            continue

        problem_name = f"wfg{i + 1}"

        results = get_results(get_problem(problem_name, n_var=n_var, n_obj=n_obj), algorithms, n_gen)

        stamp_results(results, title=problem_name, radviz=True, ax=axs[i])

    if tight_layout:
        plt.tight_layout()

    plt.show()