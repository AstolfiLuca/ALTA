import numpy as np

from pymoo.core.problem import Problem

class MultiObjectiveProblem(Problem):
    def __init__(self):
        super().__init__(
            n_var=2, 
            n_obj=2, 
            n_constr=0,
            xl=np.array([-5, -5]), 
            xu=np.array([5, 5])
        )
    
    def _evaluate(self, X, out, *args, **kwargs):
        f1 = X[:, 0]**2 + X[:, 1]**2
        f2 = (X[:, 0] - 2)**2 + (X[:, 1] - 2)**2
        
        out["F"] = np.column_stack([f1, f2])


