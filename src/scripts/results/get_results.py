from pymoo.optimize import minimize
from pymoo.termination import get_termination

def get_results(problem, algorithms, n_gen, save_history=False, print_name=False, seed=1):
    results = {}

    termination = get_termination("n_gen", n_gen)

    for name, algorithm in algorithms.items():
        if print_name:
            print(name)
        
        # Già qui mi restituisce 30 soluzioni
        result = minimize(
            problem, 
            algorithm, 
            termination, 
            save_history=save_history,
            seed=seed
        )

        print(f"Pop size finale: {len(result.pop)}")
        print(f"Soluzioni non dominate in F: {len(result.F)}")

        
        results[name] = result

    return results