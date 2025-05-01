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
        self.MJ = pile_MJ if use_MJ_pile else standard_MJ  
        self.use_MJ_algorithm = use_MJ_algoritm
        self.opt = None

    def _do(self, problem, pop, n_survive, algorithm=None, **kwargs):
        gen = algorithm.n_gen
        #print(f"{gen}: ") 
        
        F = pop.get("F")  # Matrice delle funzioni obiettivo, dimensione (n_pop, n_obj)

        F_candidate_sorted = np.argsort(F, axis=0) # Ordino gli indi 
        
        leaderboard = self.MJ(F_candidate_sorted) # pile_MJ if use_MJ_pile else standard_MJ  
        
        # print(leaderboard)
        # print(leaderboard[:n_survive]) 
        if self.use_MJ_algorithm:
            fronts, rank = NonDominatedSorting().do(F, return_rank=True)
            pop.set("rank", rank)
            self.opt = pop[fronts[0]] # Per NSGA3

            crowding = np.full(len(pop), np.nan)
            pop.set("crowding", crowding)
# 
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

        self.survival = MJSurvival(use_MJ_pile=use_MJ_pile, use_MJ_algoritm=True)
