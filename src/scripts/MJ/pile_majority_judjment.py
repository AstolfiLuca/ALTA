import numpy as np

from collections import deque 

def majority_judment(phi_matrix, gen=None, increasing=False, limit=None):
    phi_matrix = np.array(phi_matrix)
    
    leaderboard = [] 

    previous_candidates = None

    phi_matrix = np.sort(phi_matrix, axis=1) # c * j * log(j)

    pile = deque()
    pile.append(list(range(phi_matrix.shape[0]))) # All candidates

    while pile:
        selected_candidates = pile.pop()

        # print(f"candidati precedenti: {previous_candidates}")
        # print(f"candidati selezionati: {selected_candidates}")

        if len(selected_candidates) == 1:
            leaderboard.append(selected_candidates[0])
            # print(f"leaderboard: {leaderboard}")
            continue

        if selected_candidates != previous_candidates:
            tmp_matrix = phi_matrix[selected_candidates]
        else:
            tmp_matrix = np.delete(tmp_matrix, middle_index, axis=1)
            if tmp_matrix.size == 0: # DUE CANDIDATI SONO ESATTAMENTE IDENTICI
                leaderboard.append(selected_candidates[0])
                continue

        middle_index = tmp_matrix.shape[1] // 2 
        if gen == 4:
            print(tmp_matrix)
        middle_column = tmp_matrix[:, middle_index]
        
        votes = {}
        for judje_vote, candidate in zip(middle_column, selected_candidates): # c
            if judje_vote not in votes:
                votes[judje_vote] = []

            votes[judje_vote].append(candidate)

        votes = sorted(votes.items(), reverse=increasing)

        for vote in votes: # n = number of grades/votes (worst case)
            pile.append(vote[1]) # candidate list of a certain vote
        
        # print(f"tmp_matrix: \n{tmp_matrix}")
        # print(f"N: {N}")
        # print(f"middle_index: {middle_index}")
        # print(f"middle_column: {middle_column}")
        # print(f"votes: {votes}")
        # print(f"pile: {pile}")
        # print(f"ultimo: {pile[-1]}")
        # print("\n\n")

        previous_candidates = selected_candidates

    return leaderboard[:None]
