from pymoo.optimize import minimize

def get_results(problem, algorithms, termination, save_history=False, print_name=True, seed=1):
    results = {}

    for name, algorithm in algorithms.items():
        if print_name:
            print(name)
        result = minimize(
            problem, 
            algorithm, 
            termination, 
            save_history=save_history,
            seed=seed
        )
        
        results[name] = result

    return results