from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
from pyrecorder.writers.video import Video
from pymoo.visualization.radviz import Radviz
from pymoo.util.normalization import normalize
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from get_results import get_results
from stamp_results import stamp_results

import numpy as np

import matplotlib
matplotlib.use("Agg")

problem = get_problem("dtlz1", n_obj=4)

algorithms = {
    "NSGA2": NSGA2(pop_size=100),
    "NSGA2_large": NSGA2(pop_size=200)
}

def streaming(algorithms, sleep_time=0.25):
    with Recorder(Streamer(sleep=sleep_time)) as rec:
        n_gen = 50
        results = get_results(problem, algorithms, n_gen, save_history=True)

        for i in range(n_gen):

            for name, res in results.items():
                    tmp_results = {name: res.history[i].pop.get("F")}
                    
                    stamp_results(tmp_results, title=name, radviz=True, no_plot=True)
                    
                    rec.record()

streaming(algorithms)