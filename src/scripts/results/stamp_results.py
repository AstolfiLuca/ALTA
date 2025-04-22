import numpy as np
import colorsys
from pymoo.visualization.scatter import Scatter
from pymoo.visualization.radviz import Radviz
from pymoo.util.normalization import normalize
import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")

def stamp_results(results, title="default_title", scatter=False, radviz=False, ax=None, save_file=False, no_plot=False):
    assert results, "Results Dict is Empty"  
    assert scatter or radviz, "It is necessary to choose a specific plot"
    
    n_res = len(results)

    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]
    
    if scatter:
        plot = Scatter(title=title, legend=True)

        for index, (name, result) in enumerate(results.items()):
            plot.add(result.F, color=colors[index], edgecolor="black", label=name)
            plot.do()

        if save_file:
            plot.save("scatter")

        plot.do()

    if radviz and n_res > 1:
        plot = Radviz(title=title, legend=True)

        all_F = np.concatenate([res.F for res in results.values()], axis=0)
        xl = all_F.min(axis=0)
        xu = all_F.max(axis=0)
        F_normalized = [normalize(res.F, xl=xl, xu=xu) for res in results.values()]
        
        for index, (name, F_norm) in enumerate(zip(results.keys(), F_normalized)):
            plot.add(F_norm, label=name, color=colors[index])
            plot.do()
        
        if save_file:
            plot.save("radvis")
        
        
    
    if ax:
        plot.ax = ax


    if not no_plot:
        plot.show()