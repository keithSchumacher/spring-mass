import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from itertools import chain

from network_plot import get_offset
from matrix_builder import *
from euler_method import *

def plot_setup(quality=False):
    if quality == 'youtube':
        fig, ax = plt.subplots(dpi=500)
    else:
        fig, ax = plt.subplots()
    ax.set_xlim([-1, 3])
    ax.set_ylim([-1, 3])
    ax.set_title('Networks with Visible Vertices and Edges')
    return fig, ax


def plot_pair(row, spring):
    return  [row[2 * spring[0] - 2], row[2 * spring[1] - 2]], [row[2 * spring[0] - 1], row[2 * spring[1] - 1]]


def update_plot(i, X, drawers, connectivity, offset, numframes, ax):
    #adjust axis
    if i == int(numframes * (3 / 4)):
        ax.set_title('Vibrating Vertices without Visualization Offset')
        ax.set_xlim(-.5, .5)
        ax.set_ylim(-.5, .5)
    if i == int(numframes / 2):
        ax.set_title('Networks with Visible Vertices and Invisible Edges')
    #plot or remove edges
    for j, x in enumerate(X):
        # add or remove offset
        if i < int(numframes * (3 / 4)):
            row = np.ravel(x[i]) + offset
        else:
            row = np.ravel(x[i])
            # scatter plot
        temp = np.array([np.array(coordinate) for coordinate in zip(row[::2], row[1::2])])
        drawers[j][0].set_offsets(temp)
        #plot edges
        if i <= int(numframes / 2):
            for k, spring in enumerate(connectivity):
                drawers[j][k + 1][0].set_data(*plot_pair(row, spring))
        #remove edges and colors
        if i == int(numframes/2)+1:
            colors = np.zeros(temp.shape[0])
            drawers[j][0].set_array(colors)
            for k in range(len(connectivity)):
                drawers[j][k+1][0].set_data([],[])
    return list(chain(*drawers)),


def network_animate(filename=False, x_plots= False, quality=False, spring_constants=False):
    #constants = [.01, .02]
    #X = [euler_method(stiffness_matrix(3, k), *initial_conditions(18)) for k in constants]
    if not x_plots:
        x_plots = generate_data(spring_constants=spring_constants)
    fig, ax = plot_setup(quality)
    connectivity = connectivity_matrix(x_plots[0].shape[1])
    offset = get_offset(x_plots[0].shape[1])
    drawers = [[], []]
    colors =['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    for i, x in enumerate(x_plots):
        row = np.ravel(x[0])
        drawers[i].append(plt.scatter(row[::2], row[1::2], s=45, c=colors[i]))
        for spring in connectivity:
            drawers[i].append(plt.plot(*plot_pair(row, spring), colors[i]))

    numframes = int(x_plots[0].shape[0])
    anim = FuncAnimation(fig, update_plot, frames=range(numframes),
                         fargs=(x_plots, drawers, connectivity, offset, numframes, ax))
    if not filename:
        filename = 'basic_animation.mp4'
    if quality == 'youtube':
        anim.save(filename, fps=30, bitrate=900, extra_args=['-vcodec', 'libx264'])
    else:
        anim.save(filename, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()

