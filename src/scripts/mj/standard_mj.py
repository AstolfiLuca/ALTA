# Complessità: O(mn^2+mlogm⋅n) nel caso peggiore O(n^3)
 
def compute_majority_sequence(grades):
    sequence = []
    sorted_grades = sorted(grades)
    
    while sorted_grades:
        num_grades = len(sorted_grades)
        median_index = (num_grades - 1) // 2
        median_value = sorted_grades[median_index]
        sequence.append(median_value)
        sorted_grades.pop(median_index)
    
    return sequence


def majority_judgment(phi_matrix):
    candidate_sequences = []
    
    for candidate_index in range(len(phi_matrix)):
        grades = phi_matrix[candidate_index]
        sequence = compute_majority_sequence(grades)
        candidate_sequences.append((sequence, candidate_index))
    
    sorted_sequences = sorted(candidate_sequences, key=lambda x: x[0], reverse=True)
    
    result_indices = []
    for sequence_pair in sorted_sequences:
        result_indices.append(sequence_pair[1])
    
    return result_indices