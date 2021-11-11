import numpy as np
from functools import reduce

def row_constructor(size, n, m, theta):
    row = np.empty(size)
    for i in range(1, size + 1):
        if i == 2 * n - 1:
            # print(i)
            row[i - 1] = np.cos(theta)
        elif i == 2 * m - 1:
            row[i - 1] = np.cos(theta)
        elif i == 2 * n:
            row[i - 1] = np.sin(theta)
        elif i == 2 * m:
            row[i - 1] = -1.0 * np.sin(theta)
        else:
            row[i - 1] = 0
    return row


def node_edge_incidence(n_vertices, n_edges, connectivity):
    A = np.empty((n_edges, n_vertices))
    for i, row in enumerate(connectivity):
        A[i, :] = row_constructor(n_vertices, *row)
    return A


def connectivity_matrix(topology):
    if topology == 6:
        connectivity = [[1,2,0],
                        [2,3,0]]
    elif topology == 10:
        connectivity = [[1, 4, np.pi / 2],
                    [1, 3, np.pi / 4],
                    [1, 2, 0],
                    [2, 3, 3 * np.pi / 4],
                    [2, 5, np.pi],
                    [3, 4, 3 * np.pi / 4],
                    [3, 5, np.pi / 4],
                    [4, 5, 0]]
    elif topology == 18:
        connectivity = [[1, 4, np.pi / 2],
                    [1, 5, np.pi / 4],
                    [1, 2, 0],
                    [2, 4, 3 * np.pi / 4],
                    [2, 5, np.pi / 2],
                    [2, 6, np.pi / 4],
                    [2, 3, 0],
                    [3, 5, 3 * np.pi / 4],
                    [3, 6, np.pi / 2],
                    [4, 7, np.pi / 2],
                    [4, 8, np.pi / 4],
                    [4, 5, 0],
                    [5, 7, 3 * np.pi / 4],
                    [5, 8, np.pi / 2],
                    [5, 9, np.pi / 4],
                    [5, 6, 0],
                    [6, 8, 3 * np.pi / 4],
                    [6, 9, np.pi / 2],
                    [7, 8, 0],
                    [8, 9, 0]]
    return connectivity

def spring_constant_matrix(i, n_springs, spring_constants=False):
    constants = [.01, .02]
    if not spring_constants:
        K = constants[i] * np.identity(n_springs)
    else:
        K = np.diag(np.random.rand(n_springs) / 10)
    return K



def stiffness_matrix(i, topology, spring_constants=False):
    if topology == 1:
        n_springs = 2
        masses = 6
    elif topology == 2:
        n_springs = 8
        masses = 10
    elif topology == 3:
        n_springs = 20
        masses = 18
    connectivity = connectivity_matrix(masses)
    A = node_edge_incidence(masses, n_springs, connectivity)
    K = spring_constant_matrix(i=i, n_springs=n_springs, spring_constants=spring_constants) #spring_constant * np.identity(n_springs)
    S = reduce(np.dot, [A.T, K, A])
    return S

# np.set_printoptions(precision=2, suppress=True)
