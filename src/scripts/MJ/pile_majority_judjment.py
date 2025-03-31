# O(mnlogm) nel caso peggiore O(m^2 * n)

import numpy as np
from collections import deque 

def majority_judment(phi_matrix, reversed=False):
    phi_matrix = np.sort(np.array(phi_matrix), axis=1) #[:, ::-1] # Trasformo phi_matrix in matrice numpy ed Ordino riga per riga (dal più grande al più piccolo)

    leaderboard = [] # Creo la leaderboard

    pila = deque()

    pila.append(list(range(phi_matrix.shape[0])))

    candidati_precedenti = None

    while pila:
        candidati_selezionati = pila.pop()

        # print(f"candidati precedenti: {candidati_precedenti}")
        # print(f"candidati selezionati: {candidati_selezionati}")

        if len(candidati_selezionati) == 1:
            leaderboard.append(candidati_selezionati[0])
            # print(f"leaderboard: {leaderboard}")
            continue

        if candidati_selezionati != candidati_precedenti:
            tmp_matrix = phi_matrix[candidati_selezionati]
        else:
            tmp_matrix = np.delete(tmp_matrix, middle_index, axis=1) 

        N = tmp_matrix.shape[1] # Ottengo il numero di votanti (dimensione della riga / numero di colonne)

        middle_index = N // 2
        middle_column = tmp_matrix[:, middle_index]

        votes = {}
        for judje_vote, candidate in zip(middle_column, candidati_selezionati):
            if judje_vote not in votes:
                votes[judje_vote] = []

            votes[judje_vote].append(candidate)

        votes = sorted(votes.items(), reverse=reversed)


        for vote in votes:
            pila.append(vote[1])


        # print(f"tmp_matrix: \n{tmp_matrix}")
        # print(f"N: {N}")
        # print(f"middle_index: {middle_index}")
        # print(f"middle_column: {middle_column}")
        # print(f"votes: {votes}")
        # print(f"pila: {pila}")
        # print(f"ultimo: {pila[-1]}")
        # print("\n\n")

        candidati_precedenti = candidati_selezionati

    return leaderboard
