import numpy as np
from pyrecorder.recorder import Recorder
from pyrecorder.writers.video import Video

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.visualization.scatter import Scatter


# with Recorder(Video("example.mp4")) as rec:

#     for k in range(10):
#         X = np.random.random((100, 2))
#         Scatter(title=str(k)).add(X).do()
#         rec.record()


from pymoo.problems import get_problem
from pymoo.optimize import minimize

problem = get_problem("zdt1")

algorithm = NSGA2(pop_size=100, eliminate_duplicates=True)

ret = minimize(problem,
               algorithm,
               termination=('n_gen', 100),
               seed=1,
               save_history=True,
               verbose=False)

# use the video writer as a resource
with Recorder(Video("ga.mp4")) as rec:

    # for each algorithm object in the history
    for entry in ret.history:
        sc = Scatter(title=("Gen %s" % entry.n_gen))
        sc.add(entry.pop.get("F"))
        sc.add(entry.problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
        sc.do()

        # finally record the current visualization to the video
        rec.record()