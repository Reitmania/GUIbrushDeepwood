from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
import matplotlib.pyplot as plt
import math

def test(values):
    Y = np.zeros([values.shape[0]])
    A = 7
    B = 0.1

    for i, X in enumerate(values):
        Y[i] = math.sin(X[0]) + A * math.pow(math.sin(X[1]), 2) + \
            B * math.pow(X[2], 4) * math.sin(X[0])

    return Y

def test2(values):
    Y = np.zeros([values.shape[0]])
    for i, X in enumerate(values):
        Y[i] = 3 * X[0] + X[1]
    return Y 


problem2 = {
    'num_vars': 2,
    'names': ['x1','x2'],
    'bounds': [[-np.pi, np.pi]]*3
}

problem = {
  'num_vars': 3,
  'names': ['x1', 'x2', 'x3'],
  'bounds': [[-np.pi, np.pi]]*3
}

# Generate samples
param_values = saltelli.sample(problem2, 1000)

# Run model (example)
Y_new = test(param_values)


# Perform analysis
Si = sobol.analyze(problem2, Y_new, print_to_console=True)
# Returns a dictionary with keys 'S1', 'S1_conf', 'ST', and 'ST_conf'
# (first and total-order indices with bootstrap confidence intervals)