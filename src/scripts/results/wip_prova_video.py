# from pymoo.algorithms.soo.nonconvex.ga import GA
# from pymoo.core.callback import Callback
# from pymoo.problems import get_problem
# from pymoo.optimize import minimize
# from pymoo.visualization.pcp import PCP
# from pyrecorder.recorder import Recorder
# from pyrecorder.writers.streamer import Streamer

import matplotlib
matplotlib.use("agg")

from pymoo.core.callback import Callback
from pymoo.visualization.radviz import Radviz
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
import numpy as np
from pymoo.util.normalization import normalize

from get_results import get_results


class MyCallback(Callback):

    def __init__(self, save_file=False, algo_name="Algorithm", color_map=None):
        super().__init__()
        self.rec = Recorder(Streamer(sleep=0.2))
        self.save_file = save_file
        self.algo_name = algo_name

        # Salverà F a ogni generazione per ciascun algoritmo
        self.results = {}

        # Mappa nome algoritmo -> colore
        self.color_map = color_map or {}
        if algo_name not in self.color_map:
            # Assegna un colore automaticamente se non specificato
            default_palette = ["black", "blue", "red", "green", "orange", "purple", "brown", "cyan"]
            assigned = len(self.color_map)
            self.color_map[algo_name] = default_palette[assigned % len(default_palette)]

    def notify(self, algorithm):
        gen = algorithm.n_gen

        # Salva la popolazione corrente
        if self.algo_name not in self.results:
            self.results[self.algo_name] = []
        self.results[self.algo_name].append(algorithm.pop.get("F"))

        # Prepara i dati normalizzati per tutti gli algoritmi
        all_F = np.concatenate([np.concatenate(fs, axis=0) for fs in self.results.values()], axis=0)
        xl = all_F.min(axis=0)
        xu = all_F.max(axis=0)

        plot = Radviz(title=f"Generation {gen}", legend=True)

        for name, all_gen_F in self.results.items():
            F = np.concatenate(all_gen_F, axis=0)
            F_norm = normalize(F, xl=xl, xu=xu)
            plot.add(F_norm, label=name, color=self.color_map[name])

        plot.do()
        self.rec.record()


pop_size = 100

algorithms = {
    "NSGA2": NSGA2(pop_size=pop_size),
    "NSGA2": NSGA2(pop_size=pop_size * 2)
}  

get_results(get_problem("dtlz1", n_obj=5), algorithms, get_termination("n_gen", 100), callback=MyCallback()) 