# --- pymoo import ---
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.problems import get_problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA

# --- scripts import ---
from scripts.mj_pymoo import *
from scripts.results.stamp_results import stamp_gdplus_results, stamp_results
from scripts.results.performance import get_all_gdplus_values, get_all_hv_values
from scripts.timer import realtimer
from scripts.results.get_results import get_results

# --- test import ---
from test.phi_matrices import get_phi_matrices, get_random_phi_matrices
from test.dtlz import test_dtlz, save_img_dtlz
from test.wfg import test_wfg

#@realtimer
def main():
    verbose = True

    # --- Dati ---
    seed = 1

    n_gen = 600 # Mantieni 400-600 
    n_obj = 6 # Mantieni 6-7GA
    #n_var = n_obj + 2 # Per DTLZ: n_var = n_obj + k - 1
    #n_partitions = n_obj + 2

    #ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=n_partitions) # se ref_dirs > pop_size, il numero della popolazione aumenta in base ad esse
    pop_size = 100 #len(ref_dirs)

    buckets = 6
    
    algorithms = {  
        #"STANDARD_MJ_ALGORITHM": MJAlgorithm(pop_size=pop_size, use_MJ_pile=False), 
        "PILE_MJ_ALGORITHM":     MJAlgorithm(pop_size=pop_size, use_MJ_pile=True),

        #"STANDARD_MJ_ALGORITHM_BUCKETS": MJAlgorithm(pop_size=pop_size, use_MJ_pile=False, buckets=buckets),
        "PILE_MJ_ALGORITHM_BUCKETS":     MJAlgorithm(pop_size=pop_size, use_MJ_pile=True,  buckets=buckets),

        #"NSGA2": NSGA2(),
        #"NSGA3": NSGA3(ref_dirs=ref_dirs),
        #"RVEA":  RVEA(ref_dirs=ref_dirs),
        #"STANDARD_MJ_NSGA3": NSGA3(survival=MJSurvival(use_MJ_pile=False), ref_dirs=ref_dirs),
        #"PILE_MJ_NSGA3":     NSGA3(survival=MJSurvival(use_MJ_pile=True),  ref_dirs=ref_dirs),
    }

    # --- Main ---
    problem = get_problem("dtlz1", n_obj=n_obj)#, n_var=n_var)

    results = get_results(problem, algorithms, n_gen, save_history=True, verbose=verbose, seed=seed) 
    
    #stamp_results(results, radviz=True)
    
    all_gd_values = get_all_gdplus_values(results)
    stamp_gdplus_results(all_gd_values, poly_degree=5)
    
    # --- dtlz test ---
    #dtlz_idx = [2, 6] # range(1, 8) # DTLZ 1-7
    #seed_idx = [1, 2, 3, 4, 5]
    #test_dtlz(dtlz_idx, algorithms, n_gen=n_gen, n_obj=n_obj)
    #save_img_dtlz(dtlz_idx, seed_idx, algorithms, n_gen, n_obj, verbose=verbose)
    
if __name__ == "__main__":
    main()

    