import numpy as np

from pymoo.core.survival import Survival

from scripts.mj.standard_mj import majority_judgment as standard_MJ
from scripts.mj.pile_mj import majority_judgment as pile_MJ

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

class MJ_Survival(Survival):
    def __init__(self, filter_infeasible=True, use_MJ_pile=True):
        super().__init__(filter_infeasible)
        self.MJ_type = pile_MJ if use_MJ_pile else standard_MJ  
        self.opt = None

    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        F_candidate_sorted = np.argsort(F, axis=0) # Ordino 
        
        leaderboard = self.MJ_type(F_candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        # print(leaderboard)
        # print(leaderboard[:n_survive]) # Solo indici dei sopravvissuti, dal migliore al peggiore
        
        fronts, rank = NonDominatedSorting().do(F, return_rank=True)
        pop.set("rank", rank)
        self.opt = pop[fronts[0]] # Per NSGA3
        
        crowding = np.full(len(pop), np.nan)

        pop.set("crowding", crowding)

        return pop[leaderboard[:n_survive]]