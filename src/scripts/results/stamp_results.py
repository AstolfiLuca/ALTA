import numpy as np
import colorsys

from pymoo.visualization.scatter import Scatter
from pymoo.visualization.radviz import Radviz

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt

def get_colors(n_res):
    return [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]


def stamp_gdplus_results(all_gd_values, poly_degree=3):
    n_res = len(all_gd_values)
    colors = get_colors(n_res)

    plt.figure()
    
    for i, (name, gd_values) in enumerate(all_gd_values.items()):
        x = np.arange(len(gd_values))

        plt.plot(x, gd_values, marker='', color=colors[i], label=name, linewidth=2)

        # Fit polinomiale
        if len(gd_values) > poly_degree:
            coeffs = np.polyfit(x, gd_values, deg=poly_degree)
            poly_fit = np.polyval(coeffs, x)
            plt.plot(x, poly_fit, color=colors[i], linestyle='dotted', linewidth=2, label=f"{name} trend (grado {poly_degree})")

    plt.xlabel("Generazione")
    plt.ylabel("GD+")
    plt.title("Andamento GD+ per generazione")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    

def stamp_results(results, title="Results", scatter=False, radviz=False, ax=None, save_file=False, no_plot=False):
    assert results, "Results Dict is Empty"  
    assert scatter or radviz, "It is necessary to choose a specific plot"
    
    n_res = len(results)

    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]
    
    plot = None

    if scatter:
        plot = Scatter(title=title, legend=True)

        for index, (name, res) in enumerate(results.items()):
            plot.add(res.F, color=colors[index], edgecolor="black", label=name)

        if save_file:
            no_plot = True
            plot.save(f"scatter_{title}")

    if radviz and n_res > 1:
        plot = Radviz(title=title, legend=True)

        
        for index, (name, res) in enumerate(results.items()):
            plot.add(res.F, label=name, color=colors[index])
        
        if save_file:
            no_plot = True
            plot.save(f"radviz_{title}")
       
    if ax:
        plot.ax = ax
        no_plot = True
    
    plot.do() 

    if not no_plot:
        plot.show()