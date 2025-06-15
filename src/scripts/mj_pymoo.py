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

        if use_MJ_pile:
            self.MJ = pile_MJ
        else:   
            self.MJ = standard_MJ  

    # Applica majority judgment (MJ)
    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        F_candidate_sorted = np.argsort(F, axis=0) # Ordino gli indici 
        
        leaderboard = self.MJ(F_candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
 
        return pop[leaderboard[:n_survive]]  # Solo indici dei sopravvissuti, dal migliore al peggiore
    

class BUCKET_MJSurvival(Survival):
    def __init__(self, filter_infeasible=False, buckets=6, use_MJ_pile=True, use_MJ_algoritm=True):
        super().__init__(filter_infeasible)
        self.opt = None
        
        if use_MJ_pile:
            self.MJ = pile_MJ
        else:   
            self.MJ = standard_MJ

        self.buckets = buckets
    
    # Calcola i punti ideal e nadir per ogni obiettivo (ideal: min, nadir: max)
    def _calc_ideal_nadir_points(self, F, zero_ideal=False): 
        if F is None or len(F) == 0:
            return np.array([])

        n_obj = F.shape[1]

        ideal = np.zeros(n_obj)
        nadir = np.zeros(n_obj)

        for i in range(n_obj):
            if not zero_ideal:
                ideal[i] = np.min(F[:, i])
            nadir[i] = np.max(F[:, i])

        return ideal, nadir

    # Ritorna una matrice (pop_size, n_obj) con i bucket assegnati ad ogni soluzione (divisione da nadir a ideal)
    def _assign_solutions_to_buckets(self, F, ideal, nadir): 
        bucket_matrix = np.zeros(F.shape)

        for j in range(F.shape[1]):
            buckets_intervals = np.linspace(nadir[j], ideal[j], self.buckets + 1) # Si divide lo spazio (da nadir a ideal) nel numero di buckets (per farlo si aggiunge 1 per l'ultimo estremo)

            bucket_indices = np.digitize(F[:, j], bins=buckets_intervals) - 1 # Usiamo digitize per assegnare le soluzioni ad ogni bucket (-1 perché digitize restituisce bin da 1 a N)
            
            bucket_indices = np.clip(bucket_indices, 0, self.buckets - 1) # Clip per sicurezza (in caso di valori esattamente uguali a ideal) 

            bucket_matrix[:, j] = bucket_indices

        return bucket_matrix

    # Applica majority judgment (MJ) poi Crowding distance
    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        F = pop.get("F")  

        ideal, nadir = self._calc_ideal_nadir_points(F)

        bucket_matrix = self._assign_solutions_to_buckets(F, ideal, nadir)

        candidate_sorted = self.MJ(bucket_matrix)

        crowding_distances_order = calc_crowding_distance(F[candidate_sorted]) # Non c'è bisogno di calcolare il crowding distance per ogni front, perchè useremo solo i candidati ordinati

        leaderboard = np.lexsort((-crowding_distances_order, candidate_sorted))  # Ordina prima per MJ, poi per crowding distance 
        
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
                 buckets=0,
                 
                 **kwargs):

        super().__init__(pop_size=pop_size, sampling=sampling, selection=selection, crossover=crossover, mutation=mutation, eliminate_duplicates=eliminate_duplicates, n_offsprings=n_offsprings, output=output, **kwargs)
        
        if not buckets:
            self.survival = MJSurvival(use_MJ_pile=use_MJ_pile)
        else:
            self.survival = BUCKET_MJSurvival(use_MJ_pile=use_MJ_pile, buckets=buckets)
            


        
