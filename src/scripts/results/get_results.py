from pymoo.optimize import minimize

def get_results(problem, algorithms, termination, callback=None, save_history=False, seed=1):
    results = {}

    for name, algorithm in algorithms.items():
        result = minimize(
            problem, 
            algorithm, 
            termination, 
            callback=callback,
            save_history=save_history,
            seed=seed
        )
        
        results[name] = result

    return results