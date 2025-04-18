import numpy as np

from pymoo.core.survival import Survival

# --- Majority Judgment --- 
from scripts.pile_MJ import majority_judgment as standard_MJ

# --- New Majority Judgment Algorithm--- 
from scripts.pile_MJ import majority_judgment as pile_MJ

from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

class MJ_Survival(Survival):
    def __init__(self, filter_infeasible=True, use_MJ_pile=True):
        super().__init__(filter_infeasible)
        self.MJ_type = pile_MJ if use_MJ_pile else standard_MJ  

    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        F_candidate_sorted = np.argsort(F, axis=0) # Ordino 
        
        leaderboard = self.MJ_type(F_candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        # print(leaderboard)
        # print(leaderboard[:n_survive]) # Solo indici dei sopravvissuti, dal migliore al peggiore
        
        result = NonDominatedSorting().do(F, return_rank=True)
                
        fronts, rank = result
        
        pop.set("rank", rank)

        crowding = np.full(len(pop), np.nan)

        pop.set("crowding", crowding)

        return pop[leaderboard[:n_survive]]
        
        """
        # Calcola la crowding distance per ciascun fronte (per avere soluzioni molto sparse, no overlap)
        crowding = np.full(len(pop), np.nan)  # Main array for the entire population
        for front in fronts:
            F_front = F[front]
            n_pop_front, n_obj_front = F_front.shape
            
            # Temporary array for the current front's crowding
            front_crowding = np.zeros(n_pop_front)
            
            for i in range(n_obj_front):
                ordered_front = np.argsort(F_front[:, i])
                front_crowding[ordered_front[0]] = front_crowding[ordered_front[-1]] = np.inf
                norm = F_front[ordered_front[-1], i] - F_front[ordered_front[0], i]
                
                if norm > 0:
                    front_crowding[ordered_front[1:-1]] += (F_front[ordered_front[2:], i] - F_front[ordered_front[:-2], i]) / norm
            
            # Assign the computed crowding to the main array
            crowding[front] = front_crowding
        
        pop.set("crowding", crowding)
        
        survivors = []
        for front in fronts:
            if len(survivors) + len(front) > n_survive:
                front_crowding = pop.get("crowding")[front]
                indices = np.argsort(-front_crowding)[:(n_survive - len(survivors))]
                survivors.extend(np.array(front)[indices])
                break
            else:
                survivors.extend(front)
        
        return pop[survivors[:n_survive]]"
        """