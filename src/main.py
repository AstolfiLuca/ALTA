# import matplotlib
# matplotlib.use('TkAgg')  
# import matplotlib.pyplot as plt
# from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.problems import get_problem
# from pymoo.indicators.hv import HV
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA

from scripts.survival_mj import MJ_Survival
from scripts.results.stamp_results import stamp_results
from scripts.results.hypervolume import hv_performance, gd_performance
from scripts.timer import realtimer
from scripts.results.get_results import get_results
from scripts.results.graphic_visualization import streaming

from test.phi_matrices import *
from test.dtlz import *
from test.wfg import *

#@realtimer
def main():
    pop_size = 100
    
    n_gen = 50
    n_obj = 5
    n_var = n_obj // 2 # nota perchè funzioni: n_obj = n_var / 2

    ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=12) # le ref_dirs sono troppe se n_partition > 12 e pop_size = 100

    algorithms = {
        "STANDARD_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=False)),
        "PILE_MJ": NSGA2(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=True)),
        #"NSGA2": NSGA2(pop_size=pop_size),
        #"NSGA3": NSGA3(pop_size=pop_size, ref_dirs=ref_dirs),
        #"RVEA": RVEA(pop_size=pop_size, ref_dirs=ref_dirs)
    }  

    streaming(get_problem("dtlz1", n_obj=n_obj, n_var=n_var), algorithms, n_gen=n_gen)

    #results = get_results(get_problem("dtlz1", n_obj=n_obj, n_var=n_var), algorithms, get_termination("n_gen", n_gen)) 
    #performance = gd_performance(results, plus=False, normalized_gd=True, print_performance=True)
    #stamp_results(results, radviz=True)
    
    # n = [1, 3, 4]
    # test_dltz(algorithms, n_gen=n_gen, n_obj=n_obj, n=n, tight_layout=True)

    return True

if __name__ == "__main__":
    main()

    