from pyrecorder.recorder import Recorder
from pyrecorder.writers.streamer import Streamer
from pyrecorder.writers.video import Video

from scripts.results.get_results import get_results
from scripts.results.stamp_results import stamp_results

import numpy as np

def streaming(problem, algorithms, n_gen=50, sleep_time=0.25):
    with Recorder(Streamer(sleep=sleep_time)) as rec:
        
        results = get_results(problem, algorithms, n_gen, save_history=True)

        for i in range(n_gen):
            for name, res in results.items():
                    tmp_results = {name: res.history[i].pop.get("F")}
                    
                    stamp_results(tmp_results, title=name, radviz=True, no_plot=True)
                    
                    rec.record()