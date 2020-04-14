# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
import numpy as np
from pyswarms.single.global_best import GlobalBestPSO


from pyswarm import pso

def banana(x):
    x1 = x[0]
    x2 = x[1]
    return x1**4 - 2*x2*x1**2 + x2**2 + x1**2 - 2*x1 + 5

def con(x):
    x1 = x[0]
    x2 = x[1]
    return [-(x1 + 0.25)**2 + 0.75*x2]

lb = [-3, -1]
ub = [2, 6]

#xopt, fopt = pso(banana, lb, ub, f_ieqcons=con)


def banana2(x):
    x1 = x[0]
    x2 = x[1]
    return x1*x2

def con2(x):
    x1 = x[0]
    x2 = x[1]
    return [x1*5+x2]

lb = [-2, -2]
ub = [2, 2]

#xopt, fopt = pso(banana2, lb, ub, f_ieqcons=con2)

#print(xopt)
#print(fopt)

############################### PYSWARMS #################################

# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call instance of PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2, options=options)
# Perform optimization
#cost, pos = optimizer.optimize(fx.sphere_func, print_step=100, iters=1000, verbose=2)

#print(cost)
#print(pos)
def rosenbrock_with_args(x, a, b, c=0):
    f = (a - x[:, 0]) ** 2 + b * (x[:, 1] - x[:, 0] ** 2) ** 2 + c
    return f

# instatiate the optimizer
x_max = 10 * np.ones(2)
x_min = -1 * x_max
bounds = (x_min, x_max)
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
optimizer = GlobalBestPSO(n_particles=10, dimensions=2, options=options, bounds=bounds)
# now run the optimization, pass a=1 and b=100 as a tuple assigned to args
cost, pos = optimizer.optimize(rosenbrock_with_args, 1000, print_step=100, verbose=3, a=1, b=100, c=0)

