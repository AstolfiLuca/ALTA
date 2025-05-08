import numpy as np

from pymoo.algorithms.base.genetic import GeneticAlgorithm
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.selection.rnd import RandomSelection
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.util.display.multi import MultiObjectiveOutput
from pymoo.core.survival import Survival
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from scripts.mj.standard_mj import majority_judgment as standard_MJ
from scripts.mj.pile_mj import majority_judgment as pile_MJ

class MJSurvival(Survival):
    def __init__(self, filter_infeasible=False, use_MJ_pile=True, use_MJ_algoritm=True):
        super().__init__(filter_infeasible)
        self.opt = None

        self.MJ = pile_MJ if use_MJ_pile else standard_MJ  
        self.use_MJ_algorithm = use_MJ_algoritm

    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        F_candidate_sorted = np.argsort(F, axis=0) # Ordino gli indici 
        
        leaderboard = self.MJ(F_candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        # print(leaderboard)
        # print(leaderboard[:n_survive]) 
        if self.use_MJ_algorithm:
            fronts, rank = NonDominatedSorting().do(F, return_rank=True)
            pop.set("rank", rank)
            self.opt = pop[fronts[0]] # Per NSGA3

            crowding = np.full(len(pop), np.nan)
            pop.set("crowding", crowding)
 
        return pop[leaderboard[:n_survive]]  # Solo indici dei sopravvissuti, dal migliore al peggiore
    

class BUCKET_MJSurvival(Survival):
    def __init__(self, filter_infeasible=False, buckets=6, use_MJ_pile=True, use_MJ_algoritm=True):
        super().__init__(filter_infeasible)
        self.opt = None
        
        self.MJ = pile_MJ if use_MJ_pile else standard_MJ  
        self.use_MJ_algorithm = use_MJ_algoritm
        self.buckets = buckets

    def _calc_ideal_nadir_points(self, F): # Punto con valori minimi per ogni obiettivo
        if F is None or len(F) == 0:
            return np.array([])

        n_obj = F.shape[1]

        ideal = np.zeros(n_obj)
        nadir = np.zeros(n_obj)

        for i in range(n_obj):
            best_idx = np.argmin(F[:, i])
            ideal[i] = F[best_idx, i]

            worst_idx = np.argmax(F[:, i])
            nadir[i] = F[worst_idx, i]
        
        return ideal, nadir

    def _assign_solutions_to_buckets(self, F, ideal, nadir): # Ritorna una matrice (pop_size, n_obj) con i bucket assegnati ad ogni soluzione (divisione da nadir a ideal)
        bucket_matrix = np.zeros(F.shape)

        for j in range(F.shape[1]):
            buckets_intervals = np.linspace(nadir[j], ideal[j], self.buckets + 1) # Si divide lo spazio (da nadir a ideal) nel numero di buckets (per farlo si aggiunge 1 per l'ultimo estremo)

            bucket_indices = np.digitize(F[:, j], bins=buckets_intervals) - 1 # Usiamo digitize per assegnare le soluzioni ad ogni bucket (-1 perché digitize restituisce bin da 1 a N)
            
            bucket_indices = np.clip(bucket_indices, 0, self.buckets - 1) # Clip per sicurezza (in caso di valori esattamente uguali a ideal) (da 0 a n_buckets - 1)

            bucket_matrix[:, j] = bucket_indices

        return bucket_matrix

    def _calc_crowding_distance(self, F):
        n_obj = F.shape[1]
        
        I = np.argsort(F, axis=0) # sort each column and get index
        
        F = F[I, np.arange(n_obj)] # sort the objective space values for the whole matrix
        
        dist = np.row_stack([F, np.full(n_obj, np.inf)]) - np.row_stack([np.full(n_obj, -np.inf), F]) # calculate the distance from each point to the last and next

        # calculate the norm for each objective - set to NaN if all values are equal
        norm = np.max(F, axis=0) - np.min(F, axis=0)
        norm[norm == 0] = np.nan

        # prepare the distance to last and next vectors
        dist_to_last, dist_to_next = dist, np.copy(dist)
        dist_to_last, dist_to_next = dist_to_last[:-1] / norm, dist_to_next[1:] / norm

        # if we divide by zero because all values in one columns are equal replace by none
        dist_to_last[np.isnan(dist_to_last)] = 0.0
        dist_to_next[np.isnan(dist_to_next)] = 0.0

        # sum up the distance to next and last and norm by objectives - also reorder from sorted list
        J = np.argsort(I, axis=0)
        cd = np.sum(dist_to_last[J, np.arange(n_obj)] + dist_to_next[J, np.arange(n_obj)], axis=1) / n_obj

        return cd

    def _sort_within_buckets(self, F, bucket_matrix):
        sorted_indices = []

        unique_buckets, inverse_indices = np.unique(bucket_matrix, axis=0, return_inverse=True)

        for i in range(len(unique_buckets)):
            group_indices = np.where(inverse_indices == i)[0]

            if len(group_indices) <= 2:
                sorted_indices.extend(group_indices.tolist())
            else:
                cd = self._calc_crowding_distance(F[group_indices])
                order = np.argsort(-cd)
                sorted_indices.extend(group_indices[order].tolist())

        return F[sorted_indices] # Ordina F secondo gli indici ottenuti



    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        ideal, nadir = self._calc_ideal_nadir_points(F)

        bucket_matrix = self._assign_solutions_to_buckets(F, ideal, nadir) # bucket_matrix --> Righe: popolazione, colonne: vettore

        crowded_sorted = self._sort_within_buckets(F, bucket_matrix)
        
        candidate_sorted = np.argsort(crowded_sorted, axis=0)

        leaderboard = self.MJ(candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        if gen == 2:
            import sys
            np.set_printoptions(threshold=sys.maxsize)
            print(f"Gen {gen} ideal: {ideal}")
            print(f"Gen {gen} nadir: {nadir}")
            print(f"Gen {gen} F: {F[1]}")
            print(f"Gen {gen} bucket matrix: {bucket_matrix}")
            print(f"Gen {gen} candidate sorted: {candidate_sorted}")
            print(f"Gen {gen} leaderboard: {leaderboard}")

        # print(leaderboard)
        # print(leaderboard[:n_survive]) 
        if not self.use_MJ_algorithm:
            fronts, rank = NonDominatedSorting().do(F, return_rank=True)
            pop.set("rank", rank)
            self.opt = pop[fronts[0]] # Per NSGA3

            crowding = np.full(len(pop), np.nan)
            pop.set("crowding", crowding)
 
        return pop[leaderboard[:n_survive]]  # Solo indici dei sopravvissuti, dal migliore al peggiore


class MJAlgorithm(GeneticAlgorithm):
    def __init__(self, 
                 pop_size=100, 
                 sampling=FloatRandomSampling(), 
                 selection=RandomSelection(), 
                 crossover=SBX(eta=30, prob=1.0), 
                 mutation=PM(eta=20),
                 eliminate_duplicates=False,
                 n_offsprings=None,
                 output=MultiObjectiveOutput(),
                 use_MJ_pile=True,
                 buckets=None,
                 **kwargs
                 ):

        super().__init__(pop_size=pop_size, 
                         sampling=sampling, 
                         selection=selection, 
                         crossover=crossover, 
                         mutation=mutation, 
                         eliminate_duplicates=eliminate_duplicates, 
                         n_offsprings=n_offsprings, 
                         output=output, 
                         **kwargs)

        if buckets:
            self.survival = BUCKET_MJSurvival(use_MJ_pile=use_MJ_pile, use_MJ_algoritm=True, buckets=buckets)
        else:
            self.survival = MJSurvival(use_MJ_pile=use_MJ_pile, use_MJ_algoritm=True)
