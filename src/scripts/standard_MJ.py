# Complessità: O(mn^2+mlogm⋅n) nel caso peggiore O(n^3)
 
def majority_judgment(candidates_grades):
    """
    Ordina i candidati in base al Majority Judgment usando solo le liste di voti.
    
    Args:
        candidates_grades: Una lista di liste di voti (es. [[5,3,2,...], [1,4,3,...]]).
                    
    Returns:
        Una lista di indici (corrispondenti ai candidati in input) ordinati dal migliore al peggiore.
    """
    def generate_tie_breaker(grades):
        current = sorted(grades.copy())
        tie_breaker = []
        while current:
            n = len(current)
            median = current[(n - 1) // 2]  # Mediana "lower"
            tie_breaker.append(median)
            # Rimuove la prima occorrenza della mediana
            idx = current.index(median)
            current = current[:idx] + current[idx+1:]
        return tie_breaker
    
    # Genera le sequenze di tie-breaker per ogni candidato
    candidate_scores = [generate_tie_breaker(grades) for grades in candidates_grades]
    
    # Ordina gli indici in base alle sequenze di tie-breaker (ordine lessicografico inverso)
    leaderboard = sorted(
        range(len(candidates_grades)), 
        key=lambda i: candidate_scores[i], 
        reverse=True
    )
    
    return leaderboard