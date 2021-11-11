import numpy as np
from matrix_builder import *

def euler_method(S, x_initial, v_initial):
    n = 50000
    time_step = .01
    time = np.array([i*time_step for i in range(n)])
    x = np.matrix([0*np.zeros(time.shape[0]) for _ in x_initial]).T
    v = np.matrix([0*np.zeros(time.shape[0]) for _ in x_initial]).T
    f = np.matrix([0*np.zeros(time.shape[0]) for _ in x_initial]).T
    #eulers method
    for i, t in enumerate(time):
        if i == 0:
            f[i] = S.dot(x_initial).copy()
            v[i] = v_initial
            x[i] = x_initial
        else:
            f[i] = -1.0*S.dot(np.ravel(x[i-1])).copy()
            v[i] = v[i-1] + f[i-1]*time_step
            x[i] = x[i-1] + v[i-1]*time_step
    return x


def initial_conditions(n_masses, random_init=False):
    if random_init:
        x_initial = np.random.rand(n_masses)/10
    else:
        if n_masses == 6:
            x_initial = np.array([-.1, 0, 0, 0, .1, 0])
        elif n_masses == 10:
            x_initial = np.array([-.1, -.1, .1, -.1,
                              0, 0,
                              .1, -.1, .1, .1])
        elif n_masses == 18:
            x_initial = np.array([-.1, -.1, 0, -.1, .1, -.1,
                              0, 0, 0, 0, 0, 0,
                              -.1, .1, 0, .1, .1, .1])
    return x_initial, np.zeros(x_initial.shape[0])


def reduce_size(X):
    #Only use every nth element in the time series.
    #Euler method results in each time series having 50,000 elements, which is unwieldly.
    n = 100
    l = range(X[0].shape[0])[0::n]
    reduced_x = [np.ndarray(shape=(len(l), X[0].shape[1])) for _ in X]
    for i, x in enumerate(X):
        for j in range(len(l)):
            reduced_x[i][j] = x[l[j]]
    return reduced_x


def generate_data(topology=3, random_init=False, spring_constants=False):
    X = [euler_method(stiffness_matrix(i, topology, spring_constants),
                          *initial_conditions(18, random_init)) for i in range(2)]
    return reduce_size(X)