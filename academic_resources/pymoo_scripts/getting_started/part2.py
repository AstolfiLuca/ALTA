import numpy as np
# Problem
from pymoo.core.problem import ElementwiseProblem

# Algorithm
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling

# Termination
from pymoo.termination import get_termination

# Assemble
from pymoo.optimize import minimize

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2, # variabili
            n_obj=2, # funzioni obiettivo
            n_ieq_constr=2, # vincoli (disequazioni=ieq, equazioni=eq)
            xl=np.array([-2,-2]), # lower bound
            xu=np.array([2,2]) # upper bound
        )

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = 100 * (x[0]**2 + x[1]**2)
        f2 = (x[0]-1)**2 + x[1]**2

        g1 = 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
        g2 = - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8 # Nota che il segno è invertito perchè si può avere solo <= per vincoli e minimizzazioni per le funzioni

        out["F"] = [f1, f2]
        out["G"] = [g1, g2]


problem = MyProblem()

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 100)



'''
n_gen = Generazioni della popolazione
n_eval = Valutazioni della funzione obiettivo 
n_nds = Dimensione del fronte di Pareto (numero di soluzioni non dominate, max 40 nel nostro caso, ossia tutta la popolazione)   
cv_min = Minimo valore della funzione di violazione dei vincoli (quanto le soluzioni sono fuori dai vincoli, dovrebbe tendendere a 0)
cv_avg = Medio  valore della funzione di violazione dei vincoli
eps = "Epsilon progress" ossia la misura della convergenza del fronte di Pareto (valore più piccolo indica che il fronte sta cambiando poco)
indicator = Qualità della soluzione (f = buono, ideal = ottimo, nadir = pessimo/peggiora, ...?)
'''

res = minimize(
    problem,
    algorithm,
    termination,
    seed=1,
    save_history=True,
    verbose=False
)


X = res.X
F = res.F


import matplotlib.pyplot as plt

if __name__ == "__main__":
    xl, xu = problem.bounds()
    plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='red') # s = 30 è la dimensione del puntino

    plt.xlim(xl[0], xu[0])
    plt.ylim(xl[1], xu[1])
    plt.title("Design Space")
    plt.show()

    plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue') 
    plt.title("Objective Space")
    plt.show()