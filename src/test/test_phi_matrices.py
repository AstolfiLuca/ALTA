# from scripts.MJ.pile_MJ import majority_judgment as standard_MJ
    # from scripts.MJ.pile_MJ import majority_judgment as pile_MJ

    # for phi_matrix in get_phi_matrices():
    #     print(standard_MJ(phi_matrix))
    #     print(pile_MJ(phi_matrix))

# rows = candidates [M-Dmension] (solutions)
# column = judjes [N-Dmension] (functions)
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

    return phi_matrices


