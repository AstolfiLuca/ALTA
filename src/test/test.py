def get_phi_matrix_1():
    # Metodo di ranking, ordine decrescente a partire da 1, che è il miglior voto
    phi_matrix = [
        # rows = candidates [M-Dmension, M = 4]
        # column = judjes [N-Dmension, N = 3]
        [1, 3, 2], 
        [4, 2, 3],
        [2, 1, 1],
        [3, 3, 4]
    ]

    return phi_matrix

def get_phi_matrix_2():
    # Metodo di ranking, ordine decrescente a partire da 1, che è il miglior voto
    phi_matrix = [
        # rows = candidates [M-Dmension, M = 4]
        # column = judjes [N-Dmension, N = 3]
        [2, 1, 4, 4, 2, 2, 3, 1, 4], 
        [1, 3, 3, 3, 1, 4, 1, 2, 1],
        [3, 4, 1, 2, 4, 3, 4, 3, 2],
        [4, 2, 2, 1, 3, 1, 2, 4, 3]
    ]

    return phi_matrix