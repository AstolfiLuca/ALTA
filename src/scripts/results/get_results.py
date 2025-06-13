from pymoo.optimize import minimize
from pymoo.termination import get_termination


def get_results(problem, algorithms, n_gen, save_history=False, print_name=False, seed=1):
    results = {}

    for name, algorithm in algorithms.items():
        results[name] = compute_results(problem, algorithm, n_gen, save_history, seed)

        if print_name:
            print(name) 


    return results


def compute_results(problem, algorithm, n_gen, save_history, seed):
    termination = get_termination("n_gen", n_gen)

    result = minimize(
            problem, 
            algorithm, 
            termination, 
            save_history=save_history,
            seed=seed
        )

    return result