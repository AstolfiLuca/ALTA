from pymoo.optimize import minimize
from pymoo.termination import get_termination

def get_results(problem, algorithms, n_gen, save_history=False, seed=1):
    results = {}

    termination = get_termination("n_gen", n_gen)

    for name, algorithm in algorithms.items():
        result = minimize(
            problem, 
            algorithm, 
            termination, 
            save_history=save_history,
            seed=seed
        )
        
        results[name] = result

    return results