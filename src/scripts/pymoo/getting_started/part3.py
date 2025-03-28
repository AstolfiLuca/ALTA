from part2 import * # Importo ciò che è stato fatto nel passo precedente

# Decomposition function
from pymoo.decomposition.asf import ASF

# La scala delle due funzioni è molto differente, stessa cosa per i valori e i limiti, va normalizzata
fl = F.min(axis=0)
fu = F.max(axis=0)
print(f"Scale f1: [{fl[0]}, {fu[0]}]")
print(f"Scale f2: [{fl[1]}, {fu[1]}]")

# Qui viene mostrata a che punto bisogna avvicinarsi (ideal) e a quale allontanarsi (nadir)
approx_ideal = F.min(axis=0)
approx_nadir = F.max(axis=0)
plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.scatter(approx_ideal[0], approx_ideal[1], facecolors='none', edgecolors='red', marker="*", s=100, label="Ideal Point (Approx)")
plt.scatter(approx_nadir[0], approx_nadir[1], facecolors='none', edgecolors='black', marker="p", s=100, label="Nadir Point (Approx)")
plt.title("Objective Space")
plt.legend()
plt.show()

# Normalizzazione
nF = (F - approx_ideal) / (approx_nadir - approx_ideal)

fl = nF.min(axis=0)
fu = nF.max(axis=0)
print(f"Scale f1: [{fl[0]}, {fu[0]}]")
print(f"Scale f2: [{fl[1]}, {fu[1]}]")

plt.figure(figsize=(7, 5))
plt.scatter(nF[:, 0], nF[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.title("Objective Space")
plt.show()


weights = np.array([0.2, 0.8]) # Scelgo dei pesi in base al mio volere (il peso di ogni funzione, 0.2 per f1 e 0.8 per f2)

decomp = ASF()

i = decomp.do(nF, 1/weights).argmin() 

print("Best regarding ASF: Point \ni = %s\nF = %s" % (i, F[i]))

plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.scatter(F[i, 0], F[i, 1], marker="x", color="red", s=200)
plt.title("Objective Space")
plt.show()