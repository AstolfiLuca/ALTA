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
Da fare:
-? Controllare la motivazione di sole 6 soluzioni
- Sistemare streaming e video
-*? Sistemare GD e GDPLUS --> preferisci il plus
-* Modificare l'algoritmo, da NSGA a:
    - *NSGA3
    - *GA ma trasformandolo in multi-obiettivo

- Aggiungere l'importanza delle funzioni (quindi "duplicare" alcune colonne della tabella)

- Modifica gd e gdplus con la pareto front del problema


-* Implementare, tramite "GeneticAlgorithm" un nuovo algoritmo usando le cose base:
    - pop_size=None,
    - sampling=FloatRandomSampling(),
    - selection=RandomSelection(),
    - crossover=SBX(eta=30, prob=1.0),
    - mutation=PM(eta=20),
    - eliminate_duplicates=True, --> Prova mettendolo a false (nel caso di pari risultati)
    - n_offsprings=None,
    - output=MultiObjectiveOutput(),
"""


#@realtimer
def main():
    n_gen = 200
    n_obj = 5 
    #n_var = n_obj // 2 # Con troppi vincoli 

    ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=n_obj + 2) # se ref_dirs > pop_size, il numero della popolazione aumenta in base ad esse

    problem = get_problem("dtlz1", n_obj=n_obj) # in base al problema cambia il numero di risultati

    pareto_front_problem = problem.pareto_front(ref_dirs=ref_dirs)


    algorithms = {
        "STANDARD_MJ_NSGA3": NSGA3(survival=MJSurvival(use_MJ_pile=False), ref_dirs=ref_dirs),
        #"PILE_MJ_NSGA3": NSGA3(survival=MJSurvival(use_MJ_pile=True), ref_dirs=ref_dirs),

        #"STANDARD_MJ_ALGORITHM": MJAlgorithm(use_MJ_pile=False, eliminate_duplicates=False),
        "PILE_MJ_ALGORITHM": MJAlgorithm(pop_size=330, use_MJ_pile=True, eliminate_duplicates=False),

        #"NSGA2": NSGA2(),
        #"NSGA3": NSGA3(ref_dirs=ref_dirs),
        #"RVEA": RVEA(ref_dirs=ref_dirs)
    }


    #results = get_results(problem, algorithms, n_gen, print_name=True) 
    #performance(results, name="gd", pareto_front_problem=pareto_front_problem, normalized=True, print_performance=True)
    #stamp_results(results, radviz=True)
    

    test_dtlz(algorithms, n_gen=n_gen, n_obj=n_obj, n=list(range(1,8)), tight_layout=True)

    #streaming(get_problem("dtlz1", n_obj=n_obj), algorithms, n_gen=n_gen) # WIP


if __name__ == "__main__":
    main()

    