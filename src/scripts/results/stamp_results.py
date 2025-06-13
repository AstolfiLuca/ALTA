import colorsys

from pymoo.visualization.scatter import Scatter
from pymoo.visualization.radviz import Radviz

import matplotlib
matplotlib.use("QtAgg")

def get_colors(n_res):
    return [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]

def stamp_gd_results(named_gd_values):
    n_res = len(all_gd_values)

    colors = get_colors(n_res)

    plt.figure()
    
    for i, (gd_values, name) in enumerate(named_gd_values.items()):
        plt.plot(range(len(gd_values)), gd_values, marker='', color=colors[i], label=name, linewidth=2)
    
    plt.xlabel("Generazione")
    plt.ylabel("GD+")
    plt.title("Andamento GD+ per generazione")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def stamp_results(results, title="default_title", scatter=False, radviz=False, ax=None, save_file=False, no_plot=False):
    assert results, "Results Dict is Empty"  
    assert scatter or radviz, "It is necessary to choose a specific plot"
    
    n_res = len(results)

    colors = [colorsys.hsv_to_rgb(i / n_res, 1, 1) for i in range(n_res)]
    
    if scatter:
        plot = Scatter(title=title, legend=True)

        for index, (name, res) in enumerate(results.items()):
            plot.add(res.F, color=colors[index], edgecolor="black", label=name)

        if save_file:
            no_plot = True
            plot.save(f"scatter_{title}")


        plot.do() 

    if radviz and n_res > 1:
        plot = Radviz(title=title, legend=True)
        
        for index, (name, res) in enumerate(results.items()):
            plot.add(res.F, label=name, color=colors[index])
        
        if save_file:
            no_plot = True
            plot.save(f"radviz_{title}")
        
        plot.do() 
       
    if ax:
        plot.ax = ax
        no_plot = True

    if not no_plot:
        plot.show()