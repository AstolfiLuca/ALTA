from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination

# --- Majority Judjment --- 
from scripts.MJ.standard_majority_judjment import majority_judgment as standard_MJ

# --- New Majority Judjment Algorithm--- 
from scripts.MJ.pile_majority_judjment import majority_judment as pile_MJ

# --- Test Phi Matrix ---
from test.test import get_phi_matrix_1, get_phi_matrix_2

# --- New PyMoo Survival With Majority judjment---
from scripts.pymoo.mj_implementation.mj_survival import ParetoSurvival

# --- Test PyMoo ---
from test.pymoo.multi_obj_problem import MultiObjectiveProblem


if __name__ == "__main__":
    print(pile_MJ(get_phi_matrix_1(), increasing=True))
    #print(standard_MJ(get_phi_matrix_2()))
    
    algorithm = NSGA2(
        pop_size=100,
        survival=ParetoSurvival()
    )

    termination = get_termination("n_gen", 50)

    res = minimize(
        MultiObjectiveProblem(), 
        algorithm, 
        termination, 
        seed=1
    )
   
    plot = Scatter(title="Majority Judjment")
    plot.add(res.F, color="red", edgecolor="black", label="Majority Judjment")
    plot.show()
