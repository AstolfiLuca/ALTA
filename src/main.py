from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.problems import get_problem

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
    
    algorithm_pile_MJ = NSGA2(
        pop_size=100,
        survival=ParetoSurvival(use_MJ_pile=True)
    )

    algorithm_standard_MJ = NSGA2(
        pop_size=100,
        survival=ParetoSurvival(use_MJ_pile=False)
    )
    
    algorithm_NSGA2 = NSGA2(
        pop_size=100
    )

    termination = get_termination("n_gen", 50)

    """
    res = minimize(
        MultiObjectiveProblem(), 
        algorithm_MJ, 
        termination, 
        seed=1
    )
   
    plot = Scatter(title="Majority Judjment")
    plot.add(res.F, color="red", edgecolor="black", label="Majority Judjment")
    plot.show()

    # --- Normal NSGA2 (Custom problem) 

    res = minimize(
        MultiObjectiveProblem(), 
        algorithm_NSGA2, 
        termination, 
        seed=1
    )
   
    plot = Scatter(title="Majority Judjment")
    plot.add(res.F, color="red", edgecolor="black", label="Majority Judjment")
    plot.show()
    """

    problem = get_problem("dtlz1")

    print(problem.n_obj)

    res_pile_MJ = minimize(
        problem, 
        algorithm_pile_MJ, 
        termination, 
        seed=1
    )

    res_standard_MJ = minimize(
        problem, 
        algorithm_standard_MJ, 
        termination, 
        seed=1
    )

    res_NSGA2 = minimize(
        problem, 
        algorithm_NSGA2, 
        termination, 
        seed=1
    )
   # plot = Scatter(title="Majority Judjment")
    # plot.add(res.F, color="red", edgecolor="black", label="Majority Judjment")
    # plot.show()

    # plot = Scatter(title="Majority Judjment")
    # plot.add(res.F, color="red", edgecolor="black", label="Majority Judjment")
    # plot.show()

    from pymoo.visualization.radviz import Radviz
    from pymoo.util.normalization import normalize

    F_pile_MJ = res_pile_MJ.F
    F_standard_MJ = res_standard_MJ.F
    F_NSGA2 = res_NSGA2.F

    # Normalizzazione dei dati per RadViz
    F_pile_MJ_normalized = normalize(F_pile_MJ)
    F_standard_MJ_normalized = normalize(F_standard_MJ, xl=F_pile_MJ.min(axis=0), xu=F_pile_MJ.max(axis=0))
    F_NSGA2_normalized = normalize(F_NSGA2, xl=F_pile_MJ.min(axis=0), xu=F_pile_MJ.max(axis=0))

    # Visualizzazione con RadViz
    plot = Radviz()
    plot.add(F_pile_MJ_normalized, label="Pile Majority Judgment", color="red")
    plot.add(F_standard_MJ_normalized, label="Standard Majority Judgment", color="green")
    plot.add(F_NSGA2_normalized, label="NSGA-II", color="blue")
    plot.show()




    