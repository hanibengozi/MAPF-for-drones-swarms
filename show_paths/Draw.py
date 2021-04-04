'''
This is a help file to draw a 3D graph of paths.
'''

# Imports:
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# Consts and globals:
PROJECTION_TEXT = '3d'
X = "X"
Y = "Y"
Z = "Z"
END_MARKER = '>'

ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
TEN = 10

GRAPH_FONT_SIZE = 20
GRAPH_FONT_STYLE = '$'

FIG_SUFFIX = '.png'
GRAPH_NAME = 'graph'
GRAPH_SUFFIX = '.gif'
GRAPH_MODE = 'I'


# Functions:
def draw_graph_prev(raw_data):
    '''
    This function gets data of quadcopers paths and draws the paths on a 3d graph.
    :param raw_data: data of quadcopers paths (dictionary)
    :return: fig - a 3d figure shows a path for each quadcoper
    '''
    fig = plt.figure()
    ax = plt.axes(projection=PROJECTION_TEXT)

    for quadcopter, path in raw_data.items():
        # Data of path for current quadcopter
        z = [coordinate[ONE] for coordinate in path]
        y = [coordinate[TWO] for coordinate in path]
        x = [coordinate[THREE] for coordinate in path]

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        # Data of start and end points
        x_start = x[ZERO]
        y_start = y[ZERO]
        z_start = z[ZERO]
        x_end = x[-ONE]
        y_end = y[-ONE]
        z_end = z[-ONE]

        # Draw 3d graph
        p = ax.plot3D(x, y, z, label=str(quadcopter))
        ax.legend()
        ax.scatter3D(x_start, y_start, z_start, color=p[ZERO].get_color())
        ax.scatter3D(x_end, y_end, z_end, color=p[ZERO].get_color(), marker=END_MARKER)

        # Set labels of axises:
        ax.set_xlabel(f'{GRAPH_FONT_STYLE}{X}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)
        ax.set_ylabel(f'{GRAPH_FONT_STYLE}{Y}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)
        ax.set_zlabel(f'{GRAPH_FONT_STYLE}{Z}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)

    return fig

def draw_graph(raw_data):
    '''
    This function gets data of quadcopers paths and draws the paths on a 3d graph.
    :param raw_data: data of quadcopers paths (dictionary)
    :return: None
    '''
    fig = plt.figure()

    paths = [path for path in raw_data.values()]
    amount_of_quadcopers = len(raw_data.keys())
    max_len_path = len(max(paths, key=len))

    fig_counter = 0
    filenames = []

    for i in range(ONE, max_len_path):
        ax = plt.axes(projection=PROJECTION_TEXT)
        new_paths = {}
        for quadcopter in range(amount_of_quadcopers):
            z_path = [paths[quadcopter][j][ONE] for j in range(min(i, len(paths[quadcopter])))]
            y_path = [paths[quadcopter][j][TWO] for j in range(min(i, len(paths[quadcopter])))]
            x_path = [paths[quadcopter][j][THREE] for j in range(min(i, len(paths[quadcopter])))]

            new_paths.update({quadcopter: {X: x_path, Y: y_path, Z: z_path}})

        for quadcopter in range(amount_of_quadcopers):
            if len(new_paths[quadcopter][X]) == ONE:
                ax.scatter3D(new_paths[quadcopter][X], new_paths[quadcopter][Y], new_paths[quadcopter][Z], label=str(quadcopter))
            else:
                ax.plot3D(new_paths[quadcopter][X], new_paths[quadcopter][Y], new_paths[quadcopter][Z], label=str(quadcopter))

        # Set labels of axises:
        ax.set_xlabel(f'{GRAPH_FONT_STYLE}{X}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)
        ax.set_ylabel(f'{GRAPH_FONT_STYLE}{Y}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)
        ax.set_zlabel(f'{GRAPH_FONT_STYLE}{Z}{GRAPH_FONT_STYLE}', fontsize=GRAPH_FONT_SIZE)

        filename = f'{fig_counter}{FIG_SUFFIX}'
        plt.savefig(filename)
        filenames.append(filename)
        fig_counter += 1

    # Build GIF
    with imageio.get_writer(f'{GRAPH_NAME}{GRAPH_SUFFIX}', mode=GRAPH_MODE) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)
            writer.append_data(image)

    # Remove files
    for filename in set(filenames):
        os.remove(filename)

    print("FINISHED")
