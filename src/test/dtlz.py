import matplotlib.pyplot as plt
import math

from pymoo.problems import get_problem

from test.phi_matrices import *
from scripts.results.stamp_results import stamp_results
from scripts.results.get_results import get_results

def test_dltz(algorithms, n_gen=200, n_obj=5, n=range(7), tight_layout=False):
    n_problems = len(n)
    columns = math.ceil(math.sqrt(n_problems))
    rows = math.ceil(n_problems / columns)

    fig, axs = plt.subplots(rows, columns, figsize=(14, 10))
    if n_problems > 1:  
        axs = axs.flatten()
    else:
        axs = [axs]  # Handle the single subplot case
        
    fig.suptitle(f"DLTZ | n_gen={n_gen} | n_obj={n_obj}", fontsize=16)
    
    for i, problem_num in enumerate(n):
        problem_name = f"dtlz{problem_num}"

        results = get_results(get_problem(problem_name, n_obj=n_obj), algorithms, n_gen)
        
        stamp_results(results, title=problem_name, radviz=True, ax=axs[i])
    
    for i in range(n_problems, len(axs)):
        axs[i].set_visible(False)
    
    if tight_layout:
        plt.tight_layout()

    plt.show()