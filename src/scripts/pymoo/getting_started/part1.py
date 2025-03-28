import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

# --- Campionamento di 500 punti su tutto il piano da -2 a 2 --- 
# Nota, sul piano:
# X1 è x 
# X2 è y

X1, X2 = np.meshgrid(np.linspace(-2, 2, 500), np.linspace(-2, 2, 500)) 

# --- Funzioni obiettivo ---

F1 = 100 * (X1**2 + X2**2)
F2 = (X1 - 1)**2 + X2**2

# --- Vincoli --- 

G1 = 2 * (X1[0] - 0.1) * (X1[0] - 0.9)  # <= 0
G2 = 20 * (X1[0] - 0.4) * (X1[0] - 0.6) # >= 0


# --- Curve di livello ---

# Note
# - Le curve di livello sono l'insieme di punti dove la funzione ottiene lo stesso valore del livello
# - In questo caso hanno lo stesso valore nei punti (0,0) del cerchio grande e (1,0) del cerchio piccolo

levels = np.array([0.02, 0.1, 0.25, 0.5, 0.8])
CS = plt.contour(X1, X2, F1, 10 * levels, colors='black', alpha=0.5)
CS = plt.contour(X1, X2, F2, levels, linestyles="dashed", colors='black', alpha=0.5)

# --- Stampo i vincoli ---

# G1
plt.plot(X1[0], G1, linewidth=2.0, color="green", linestyle='dotted') # Stampo tutto G1
plt.plot(X1[0][G1 < 0], G1[G1 < 0], label="$g_1(x)$", linewidth=2.0, color="green") # Ma evidenzio solo i punti < 0 (nota che gli passo sia x=X1[0] che y=G1)

# G2
plt.plot(X1[0], G2, linewidth=2.0, color="blue", linestyle='dotted') # Stampo tutto G2
plt.plot(X1[0][X1[0] > 0.6], G2[X1[0] > 0.6], label="$g_2(x)$", linewidth=2.0, color="blue")
plt.plot(X1[0][X1[0] < 0.4], G2[X1[0] < 0.4], linewidth=2.0, color="blue") # Ma evidenzio solo i punti < 0.4

# --- Stampo la regione ammissibile ---

plt.plot(np.linspace(0.1, 0.4, 100), np.zeros(100), linewidth=3.0, color="orange")
plt.plot(np.linspace(0.6, 0.9, 100), np.zeros(100), linewidth=3.0, color="orange")

plt.xlim(-0.5, 1.5)
plt.ylim(-0.5, 1)
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=4, fancybox=True, shadow=False)

plt.tight_layout()
plt.show()

# --- Pareto (su un altro grafico) ---
# Quello che è successo è questo:
# X2 può essere solo 0, viene semplificato e quindi rimane: 
# f1(x) = 100*x1^2 
# f2(x) = −(x1−1)^2
# e quindi può essere riscritto come:

f2 = lambda f1: - ((f1/100) ** 0.5 - 1)**2 # Funzione anonima (lambda)


F1_a = np.linspace(1,  16, 300) # 1,  16 sono i valori che si ottengono inserendo x1 in f1
F1_b = np.linspace(36, 81, 300) # 36, 81 sono i valori che si ottengono inserendo f1(x1) in f2

F2_a = f2(F1_a)
F2_b = f2(F1_b)

plt.plot(F1_a, F2_a, linewidth=2.0, color="green", label="Pareto-front")
plt.plot(F1_b, F2_b, linewidth=2.0, color="green")

plt.xlabel("$f_1$")
plt.ylabel("$f_2$")

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=4, fancybox=True, shadow=False)

plt.tight_layout()
plt.show()
