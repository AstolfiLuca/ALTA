import math
import matplotlib.pyplot as plt

from pymoo.problems import get_problem
from scripts.results.get_results import get_results
from scripts.results.stamp_results import stamp_results

def do_dtlz(problem_num, algorithms, n_gen, n_obj, seed=1, ax=None, save_file=False, verbose=False):
    problem_name = f"dtlz{problem_num}"

    problem = get_problem(problem_name, n_obj=n_obj)        
    
    results = get_results(problem, algorithms, n_gen, verbose=verbose, seed=seed) 

    stamp_results(results, title=f"{problem_name}_seed{seed}", radviz=True, save_file=save_file, ax=ax)


def test_dtlz(dtlz_idx, algorithms, n_gen, n_obj, verbose=True):
    n_problems = len(dtlz_idx)

    columns = math.ceil(math.sqrt(n_problems))
    rows = math.ceil(n_problems / columns)

    fig, axs = plt.subplots(rows, columns, figsize=(14, 10))
        
    fig.suptitle(f"DLTZ | n_gen={n_gen} | n_obj={n_obj}", fontsize=16)

    if n_problems > 1:  
        axs = axs.flatten()
    else: # Gestione caso singolo 
        axs = [axs] 
    
    # Eseguiamo i problemi DTLZ
    for i, problem_num in enumerate(dtlz_idx):
        do_dtlz(problem_num, algorithms, n_gen, n_obj, ax=axs[i], save_file=False, verbose=verbose)

        axs[i].set_title(f"DTLZ {dtlz_idx[i]}", fontsize=14)

        if verbose:
            print(f"DTLZ {problem_num} done")

    # Nascondiamo gli assi non utilizzati
    for i in range(n_problems, len(axs)):
        axs[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()


def save_img_dtlz(dtlz_idx, seed_idx, algorithms, n_gen, n_obj, verbose=True):
    for seed in seed_idx:
        for problem_num in dtlz_idx:
            do_dtlz(problem_num, algorithms, n_gen, n_obj, seed, save_file=True, verbose=verbose)



