import colorsys

from pymoo.visualization.scatter import Scatter
from pymoo.visualization.radviz import Radviz

import matplotlib
matplotlib.use("QtAgg")

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
            plot.save("scatter")


        plot.do() 

    if radviz and n_res > 1:
        plot = Radviz(title=title, legend=True)
        
        for index, (name, res) in enumerate(results.items()):
            #print(len(res.F))
            plot.add(res.F, label=name, color=colors[index])
        
        if save_file:
            plot.save("radvis")
        
        plot.do() 
       
    if ax:
        plot.ax = ax
        no_plot = True

    if not no_plot:
        plot.show()