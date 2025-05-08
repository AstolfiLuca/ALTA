import matplotlib.pyplot as plt
import math

from pymoo.problems import get_problem

from test.phi_matrices import *
from scripts.results.stamp_results import stamp_results
from scripts.results.get_results import get_results

def test_dtlz(algorithms, n_gen=200, n_obj=5, n=range(7), var=False, print_name=True, tight_layout=False):
    n_problems = len(n)
    columns = math.ceil(math.sqrt(n_problems))
    rows = math.ceil(n_problems / columns)

    n_var = 0
    if var:
        n_var = n_obj + 9
    
    fig, axs = plt.subplots(rows, columns, figsize=(14, 10))
    if n_problems > 1:  
        axs = axs.flatten()
    else:
        axs = [axs]  # Handle the single subplot case
        
    fig.suptitle(f"DLTZ | n_gen={n_gen} | n_obj={n_obj}", fontsize=16)
    
    for i, problem_num in enumerate(n):
        problem_name = f"dtlz{problem_num}"

        results = get_results(get_problem(problem_name, n_obj=n_obj, n_var=n_var), algorithms, n_gen, print_name=print_name)
        
        stamp_results(results, title=problem_name, radviz=True, ax=axs[i])
    
    for i in range(n_problems, len(axs)):
        axs[i].set_visible(False)
    
    if tight_layout:
        plt.tight_layout()

    plt.show()