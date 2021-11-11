import numpy as np
from matrix_builder import *
import matplotlib.pyplot as plt

def get_offset(topology):
    if topology == 6:
        offset = np.array([0, 0,  1, 0, 2, 0])
    elif topology == 10:
        offset = np.array([0, 0, 1, 0, .5, .5, 0, 1, 1, 1])
    elif topology == 18:
        offset = np.array([0, 0, 1, 0, 2, 0,
                      0, 1, 1, 1, 2, 1,
                      0, 2, 1, 2, 2, 2])
    return offset

def setup_static_plot():
    fig, axs = plt.subplots(1, 3, figsize=(15, 6), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.2)
    axs = axs.ravel()
    titles = ['3 masses, 2 springs', '5 masses, 8 springs', '9 masses, 20 springs']
    for ax, title in zip(axs, titles):
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_title(title)
    return axs


def network_plot(x, ax):
    x_plot = np.ravel(get_offset(x[0].shape[1]) + np.array(x))
    for spring in connectivity_matrix(x[0].shape[1]):
        ax.plot([x_plot[2 * spring[0] - 2], x_plot[2 * spring[1] - 2]],
                        [x_plot[2 * spring[0] - 1], x_plot[2 * spring[1] - 1]], 'black')
        for coordinate in zip(x_plot[::2], x_plot[1::2]):
            ax.plot(*coordinate, 'o', markersize=10)