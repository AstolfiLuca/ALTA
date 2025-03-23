import numpy as np

from test.test import get_phi_matrix

def resolve_majority_ties(phi_matrix, F, N):
    phi_matrix
    pass


def find_duplicates(arr):
    if not arr:
        return {}

    duplicates = {} 

    for index, value in enumerate(arr):
        if value in duplicates:
            duplicates[value].append(index)
        else:
            if arr.count(value) > 1:
                duplicates[value] = [index]

    return duplicates


def get_middle_voter_index(candidate):
    N = len(candidate)

    if N % 2 == 1:
        # odd:  r(n+1)/2
        middle_voter_index = int((N + 1) / 2)  
    else:
        # even: r(n+2)/2
        middle_voter_index = int((N + 2) / 2) 

    return middle_voter_index - 1


def calculate_F(matrix):
    F = []

    for candidate in matrix:
        candidate = sorted(candidate, reverse=True)
        
        # Se diverso da []
        if candidate:
            middle_voter_index = get_middle_voter_index(candidate)

            F.append(candidate[middle_voter_index])
        else:
            F.append([])

    return F

def majority_grade(phi_matrix):
    duplicates = True

    while duplicates:
        F = calculate_F(phi_matrix)
        print(F)
    
        duplicates = find_duplicates(F)

        for duplicate in duplicates:
            for tie_candidate in duplicates[duplicate]:

                middle_voter_index = get_middle_voter_index(phi_matrix[tie_candidate])


                # VA ORDINATOOOOOOOOO NON FUNZIONA ORA


                phi_matrix[tie_candidate].pop(middle_voter_index)
                
    return F

def app():
    phi_matrix = get_phi_matrix()

    F = majority_grade(phi_matrix)
