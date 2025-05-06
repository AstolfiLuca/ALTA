from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
from pyrecorder.writers.video import Video

from scripts.results.get_results import get_results
from scripts.results.stamp_results import stamp_results

import matplotlib.pyplot as plt

import numpy as np

def streaming(problem, algorithms, n_gen=50, sleep_time=0.25):
    results = get_results(problem, algorithms, n_gen, save_history=True)
    
    with Recorder(Streamer(sleep=sleep_time)) as rec:
        for i in range(min(n_gen, len(next(iter(results.values())).history))):
            tmp_results = {}
            
            for name, res in results.items():
                # Crea una copia dei dati invece di modificare l'originale
                F_data = res.history[i].pop.get("F")
                if F_data is not None and len(F_data) > 0:
                    tmp_results[name] = type('obj', (object,), {'F': F_data})
            
            if tmp_results:  # Verifica che ci siano risultati da mostrare
                stamp_results(tmp_results, title=f"Generazione {i+1}", radviz=True, no_plot=False)
                rec.record()