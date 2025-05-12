# import matplotlib
# matplotlib.use('TkAgg')  
# import matplotlib.pyplot as plt
# from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.problems import get_problem
# from pymoo.indicators.hv import HV
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.base.genetic import GeneticAlgorithm
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA

from scripts.mj_algorithm import *
from scripts.results.stamp_results import stamp_results
from scripts.results.performance import performance
from scripts.timer import realtimer
from scripts.results.get_results import get_results
from scripts.results.graphic_visualization import streaming

from test.phi_matrices import get_phi_matrices, get_random_phi_matrices
from test.dtlz import test_dtlz
from test.wfg import test_wfg


"""
1: otteniamo il nadir (attuale, mix del valore migliore tra quelli che abbiamo) e ideal (idem)
2: utilizza vari bucket 5
3: uso il bucket per fare rank


Per evitare di avere troppe soluzioni nella stessa regione è utilizzare:
- rank di MJ 
- crowding distance di NSGA2 (in caso di pareggio tra le ultime)

Utilizza vettore/norma
- memorizzo lo storico dei valori (per debug)


prove con 6/7 obj

------------------------------

Implementazione di un algoritmo (majority judjment) che serve per selezionare le soluzioni da mantenere alla 
generazione successiva in un algoritmo di genetic programming ma nel caso multiobiettivo

"""



#@realtimer
def main():
    n_gen = 600 # Mantieni 400-600 
    n_obj = 6 # Mantieni 6-7
    #n_var = n_obj + 9 # Per DTLZ: n_var = n_obj + k - 1
    seed = 1

    #ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=n_obj + 2) # se ref_dirs > pop_size, il numero della popolazione aumenta in base ad esse
    pop_size = 100
    #pop_size = len(ref_dirs)
    
    problem = get_problem("dtlz1", n_obj=n_obj)#, n_var=n_var) # in base al problema cambia il numero di risultati

    #pareto_front_problem = problem.pareto_front(ref_dirs=ref_dirs)

    algorithms = {
        #"STANDARD_MJ_NSGA3": NSGA3(survival=MJSurvival(use_MJ_pile=False), ref_dirs=ref_dirs),
        #"PILE_MJ_NSGA3": NSGA3(survival=MJSurvival(use_MJ_pile=True), ref_dirs=ref_dirs),

        #"STANDARD_MJ_ALGORITHM": MJAlgorithm(use_MJ_pile=False, eliminate_duplicates=False),
        "PILE_MJ_ALGORITHM": MJAlgorithm(pop_size=pop_size, use_MJ_pile=True, eliminate_duplicates=False),

        #"STANDARD_MJ_ALGORITHM_BUCKETS": NEW_MJAlgorithm(use_MJ_pile=False, eliminate_duplicates=False),
        "PILE_MJ_ALGORITHM_BUCKETS": MJAlgorithm(pop_size=pop_size, use_MJ_pile=True, eliminate_duplicates=False, buckets=6),

        #"NSGA2": NSGA2(),
        #"NSGA3": NSGA3(ref_dirs=ref_dirs),
        #"RVEA": RVEA(ref_dirs=ref_dirs)
    }

    results = get_results(problem, algorithms, n_gen, print_name=True, seed=seed) 
    #performance(results, name="gd+", pareto_front_problem=pareto_front_problem, normalized=False, print_performance=True)
    stamp_results(results, radviz=True)
    
    # n = [2, 6]
    # test_dtlz(algorithms, n_gen=n_gen, n_obj=n_obj, var=True, n=n, tight_layout=True)

    #streaming(problem, algorithms, n_gen=n_gen) # WIP


    # for problem_id in range(1, 6):
    #     problem_name = f"dtlz{problem_id}"

    #     problem = get_problem(problem_name, n_obj=n_obj)
        
    #     for seed_id in range(1, 6):
    #         results = get_results(problem, algorithms, n_gen, print_name=True, seed=seed_id) 
    #         stamp_results(results, title=f"{problem_name}_seed{seed_id}", radviz=True, save_file=True)

if __name__ == "__main__":
    main()

    