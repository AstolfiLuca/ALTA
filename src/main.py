from scripts.MJ.pile_majority_judjment import majority_judment as pile_MJ
from scripts.MJ.standard_majority_judjment import majority_judgment as standard_MJ

from test.test import *

if __name__ == "__main__":
    print(pile_MJ(get_phi_matrix_2()))
    print(standard_MJ(get_phi_matrix_2()))
