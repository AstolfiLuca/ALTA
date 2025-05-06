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
    

class NEW_MJSurvival(Survival):
    def __init__(self, filter_infeasible=False, use_MJ_pile=True, use_MJ_algoritm=True):
        super().__init__(filter_infeasible)
        self.MJ = pile_MJ if use_MJ_pile else standard_MJ  
        self.use_MJ_algorithm = use_MJ_algoritm
        self.opt = None

    def _calc_crowding_distance(self, F, **kwargs):
        n_points, n_obj = F.shape

        # sort each column and get index
        I = np.argsort(F, axis=0)

        # sort the objective space values for the whole matrix
        F = F[I, np.arange(n_obj)]

        # calculate the distance from each point to the last and next
        dist = np.row_stack([F, np.full(n_obj, np.inf)]) - np.row_stack([np.full(n_obj, -np.inf), F])

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

    def _calc_ideal_point(population):
        if not population:
            return []
        
        num_objectives = len(population[0])
        ideal = [float('inf')] * num_objectives
        
        for solution in population:
            for i in range(num_objectives):
                ideal[i] = min(ideal[i], solution[i])
        
        return ideal

    def _calc_nadir_point(population):
        if not population:
            return []
        
        num_objectives = len(population[0])
        nadir = [float('-inf')] * num_objectives
        
        for solution in population:
            for i in range(num_objectives):
                nadir[i] = max(nadir[i], solution[i])
        
        return nadir

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
