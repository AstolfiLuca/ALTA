from scripts.mj.standard_mj import majority_judgment as standard_MJ
from scripts.mj.pile_mj import majority_judgment as pile_MJ

# rows = candidates [M-Dmension] (solutions)
# column = judjes [N-Dmension] (functions)
def test_phi_matrices(random=False, n=1):
    if random:
        phi_matrices = get_random_phi_matrices(n=n)
    else:
        phi_matrices = get_phi_matrices()

    for phi_matrix in phi_matrices:
        print(standard_MJ(phi_matrix))
        print(pile_MJ(phi_matrix))

# --- predefined ---
def get_phi_matrices():
    phi_matrices = []

    # Metodo di ranking, ordine decrescente a partire da 1, che è il miglior voto
    phi_matrices.append([
        [1, 3, 2], 
        [4, 2, 3],
        [2, 1, 1],
        [3, 3, 4]
    ])

    phi_matrices.append([
        # rows = candidates [M-Dmension, M = 4]
        # column = judjes [N-Dmension, N = 3]
        [2, 1, 4, 4, 2, 2, 3, 1, 4], 
        [1, 3, 3, 3, 1, 4, 1, 2, 1],
        [3, 4, 1, 2, 4, 3, 4, 3, 2],
        [4, 2, 2, 1, 3, 1, 2, 4, 3]
    ])

    phi_matrices.append([
        [5, 4, 3],  
        [3, 3, 3],  
        [4, 2, 1]   
    ])

    phi_matrices.append([
        [5, 3, 1],  
        [5, 3, 1],  
        [4, 3, 2]   
    ])

    phi_matrices.append([
        [5, 4, 3, 2],  
        [5, 3, 3, 1],  
        [4, 4, 2, 2]   
    ])

    phi_matrices.append([
        [5, 4, 3, 2, 1],  
        [5, 4, 3, 2, 1],  
        [5, 4, 2, 2, 1],  
        [5, 3, 3, 3, 1]   
    ])

    phi_matrices.append([
        [1, 2, 3],  
        [3, 3, 3],  
        [2, 4, 5]   
    ])

    phi_matrices.append([
        [3, 3, 3],  
        [3, 3, 3],  
        [3, 3, 3]   
    ])

    phi_matrices.append([
        [5],  
        [3],  
        [4]   
    ])

    phi_matrices.append([
        [10, 9, 8, 7, 6, 6, 5, 4, 3, 2, 1],         
        [10, 9, 8, 7, 7, 6, 5, 4, 3, 2, 1],         
        [10, 9, 8, 7, 6, 6, 5, 4, 3, 2, 1],         
        [9, 8, 7, 7, 7, 6, 6, 5, 4, 3, 2],          
        [9, 9, 8, 7, 6, 6, 5, 4, 3, 2, 1],          
        [10, 8, 8, 7, 7, 6, 5, 4, 3, 2, 1],         
        [8, 8, 8, 7, 7, 6, 5, 5, 4, 3, 2],          
        [9, 9, 8, 7, 7, 6, 5, 4, 3, 2, 1],           
        [10, 9, 9, 8, 7, 5, 4, 3, 2, 1, 1],         
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],           
        [10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],        
        [9, 8, 7, 7, 7, 7, 7, 6, 5, 4, 2],          
        [9, 8, 7, 7, 7, 6, 6, 5, 5, 4, 3],          
        [8, 8, 8, 8, 7, 7, 6, 5, 4, 2, 1],          
        [10, 10, 10, 8, 6, 6, 5, 4, 2, 2, 1],       
        [7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 5]           
    ])

    phi_matrices.append([
        [10, 10, 10, 9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6],  
        [10, 10, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3],    
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],      
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10], 
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],      
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1],     
        [9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6, 5, 5, 5],      
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],      
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],      
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],      
        [5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
        [4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 10],   
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],      
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 10], 
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1],      
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6],      
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],       
        [10, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3],     
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],       
    ])

    return phi_matrices

# --- random phi matrices ---
def get_random_phi_matrices(n=1, n_candidates=10, n_judges=15, max_vote=10):
    import random

    phi_matrices = []
    for _ in range(n):

        phi_matrix = []
        for _ in range(n_candidates):

            candidate = []
            for _ in range(n_judges):

                candidate.append(random.randint(1, max_vote))

            phi_matrix.append(candidate)

        phi_matrices.append(phi_matrix)

    return phi_matrices


