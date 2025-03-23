def get_phi_matrix():
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
