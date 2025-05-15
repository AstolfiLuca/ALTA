import numpy as np

from pymoo.algorithms.base.genetic import GeneticAlgorithm
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.selection.rnd import RandomSelection
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.util.display.multi import MultiObjectiveOutput
from pymoo.core.survival import Survival
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from pymoo.operators.survival.rank_and_crowding.metrics import calc_crowding_distance

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

        ideal = np.zeros(n_obj) # PROVA ANCHE CON 0
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
            
            bucket_indices = np.clip(bucket_indices, 0, self.buckets - 1) # Clip per sicurezza (in caso di valori esattamente uguali a ideal) 

            bucket_matrix[:, j] = bucket_indices

        return bucket_matrix

    def _sort_within_buckets(self, F, bucket_matrix):
        sorted_indices = []

        # Va fatto solo sui 3/4 sul limite INVERTILA CON IL MAJORITY JUDGMENT

        inverse_indices = np.unique(bucket_matrix, axis=0, return_inverse=True)[1] # Dati i vettori di ogni soluzione, restituisce gli indici dei bucket a cui appartengono

        for i in range(len(inverse_indices)):
            bucket_indices = np.where(inverse_indices == i)[0] # Procediamo con ordine, da 0 a N-1, per ogni bucket

            if len(bucket_indices) > 2:
                cd = calc_crowding_distance(F[bucket_indices])
                order = np.argsort(-cd)
            else:
                order = np.arange(len(bucket_indices)) # Se ci sono 2 o meno soluzioni, non serve ordinare

            sorted_indices.extend(bucket_indices[order].tolist())

        return bucket_matrix[sorted_indices] # Ordina F secondo gli indici ottenuti



    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        ideal, nadir = self._calc_ideal_nadir_points(F)
        bucket_matrix = self._assign_solutions_to_buckets(F, ideal, nadir) # bucket_matrix --> Righe: popolazione, colonne: vettore
        candidate_sorted = self._sort_within_buckets(F, bucket_matrix)
        
        #candidate_sorted = np.argsort(crowded_sorted, axis=0)

        leaderboard = self.MJ(candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        # LA CROWDING DISTANCE VA FATTA QUI

        if gen == 600:
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
        # if not self.use_MJ_algorithm:
        #     fronts, rank = NonDominatedSorting().do(F, return_rank=True)
        #     pop.set("rank", rank)
        #     self.opt = pop[fronts[0]] # Per NSGA3

        #     crowding = np.full(len(pop), np.nan)
        #     pop.set("crowding", crowding)
 
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
