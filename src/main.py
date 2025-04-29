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
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.rvea import RVEA

from scripts.survival_mj import MJ_Survival
from scripts.results.stamp_results import stamp_results
from scripts.results.performance import performance
from scripts.timer import realtimer
from scripts.results.get_results import get_results
from scripts.results.graphic_visualization import streaming

from test.phi_matrices import *
from test.dtlz import *
from test.wfg import *


"""
Da fare:
-* Controllare la motivazione di sole 6 soluzioni
- Sistemare streaming e video
- Sistemare GD e GDPLUS
- Rimuovere normalizzazione (se serve)
-* Modificare l'algoritmo, da NSGA a ???
    - *NSGA3
    - GA ma trasformandolo in multi-obiettivo
-* Testare su 500 e 1000 generazioni (con quale metrica?)

- Aggiungere l'importanza delle funzioni (quindi "duplicare" alcune colonne della tabella)
"""


#@realtimer
def main():
    pop_size = 100
    
    n_gen = 200
    n_obj = 5
    n_var = n_obj // 2 # nota perchè funzioni: n_obj = n_var / 2

    ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=4) # le ref_dirs sono troppe se n_partition > 12 e pop_size = 100

    algorithms = {
        "STANDARD_MJ": NSGA3(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=False), ref_dirs=ref_dirs),
        "PILE_MJ": NSGA3(pop_size=pop_size, survival=MJ_Survival(use_MJ_pile=True), ref_dirs=ref_dirs),
        "NSGA2": NSGA2(pop_size=pop_size),
        # "NSGA3": NSGA3(pop_size=pop_size, ref_dirs=ref_dirs),
        # "RVEA": RVEA(pop_size=pop_size, ref_dirs=ref_dirs)
    }  

    #results = get_results(get_problem("dtlz2", n_obj=n_obj, n_var=n_var), algorithms, n_gen, print_name=True) 
    #performance(results, name="gd", normalized=True, print_performance=True)
    #stamp_results(results, radviz=True)
    
    n = [1, 3, 4]
    test_wfg(algorithms, n_gen=n_gen, n_obj=n_obj, n=n, tight_layout=True)

    #streaming(get_problem("dtlz1", n_obj=n_obj), algorithms, n_gen=n_gen) # WIP


if __name__ == "__main__":
    main()

    