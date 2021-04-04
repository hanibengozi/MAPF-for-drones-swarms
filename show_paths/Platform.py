'''
This is a main file to run a client side platform of a project.
'''

# Imports:
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
from show_paths.Draw import *
from World import *
import Search
import json
import os
from tkinter import filedialog as fd

# Consts and globals:
GRAPH_TEXT = "Graph of results will be shown here"
BACKGROUND_COLOR = "lightblue"
BUTTON_COLOR = "blue"
TITLE_TEXT = "Project"
START_COO_TEXT = "Start coordinate:"
END_COO_TEXT = "End coordinate:"
SAVE_TEXT = "Save"
QUADCOPTERS_TEXT = "Quadcopters: "
DRAW_TEXT = "Draw Graph"
ADD_TEXT = "Add Quadcopter"
RESET_TEXT = "Reset"
FONT_TYPE = "Courier"
LABEL_STYLE = "groove"

HEIGHT = 650
WIDTH = 700

w, h = 80, 30

FONT_SIZE = 14
ENTRY_WIDTH = 15

# root = tk.Tk()
root = tk.Toplevel()
root.title(TITLE_TEXT)

WIN_HEIGHT = root.winfo_screenheight()
WIN_WIDTH = root.winfo_screenwidth()

input_data = []


# Functions:
def toggle_geom():
    '''
    This is a help function to set window's geometry.
    :return: None
    '''
    global _geom
    geom = root.winfo_geometry()
    root.geometry(_geom)
    _geom = geom

def add_quadcopter():
    root.add_quadcopter_window = tk.Toplevel(root)
    root.canvas_add_quadcopter_window = tk.Canvas(root.add_quadcopter_window, height=HEIGHT, width=WIDTH, bg=BACKGROUND_COLOR)

    start_title_label = ttk.Label(root.add_quadcopter_window, text="choose file")
    start_title_label.config(background=BACKGROUND_COLOR)
    start_title_label.grid(column=ZERO, row=ZERO)

    file_path = tk.IntVar()
    root.file_path = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=file_path)
    root.file_path.grid(column=ZERO, row=ONE)

    # choose file button
    choose_file_button = tk.Button(root.add_quadcopter_window, text="choose file", bg=BUTTON_COLOR, command=select_file)
    choose_file_button.grid(column=ONE, row=ONE)

    # Save button
    save_button = tk.Button(root.add_quadcopter_window, text=SAVE_TEXT, bg=BUTTON_COLOR, command=close_canvas)
    save_button.grid(column=ZERO, row=FOUR)


# def add_quadcopter():
#     '''
#     This is a help function to add start and end coordinates for a new quadcoper.
#     :return: None
#     '''
#     root.add_quadcopter_window = tk.Toplevel(root)
#     root.canvas_add_quadcopter_window = tk.Canvas(root.add_quadcopter_window, height=HEIGHT, width=WIDTH, bg=BACKGROUND_COLOR)
#
#     # Start coordinate
#     start_title_label = ttk.Label(root.add_quadcopter_window, text=START_COO_TEXT)
#     start_title_label.config(background=BACKGROUND_COLOR)
#     start_title_label.grid(column=ZERO, row=ZERO)
#
#     x_start_label = ttk.Label(root.add_quadcopter_window, text=X)
#     x_start_label.config(background=BACKGROUND_COLOR)
#     x_start_label.grid(column=ZERO, row=ONE)
#     x_start_entry = tk.IntVar()
#     root.x_start_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=x_start_entry)
#     root.x_start_entered.grid(column=ONE, row=ONE)
#
#     y_start_label = ttk.Label(root.add_quadcopter_window, text=Y)
#     y_start_label.config(background=BACKGROUND_COLOR)
#     y_start_label.grid(column=ZERO, row=TWO)
#     y_start_entry = tk.IntVar()
#     root.y_start_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=y_start_entry)
#     root.y_start_entered.grid(column=ONE, row=TWO)
#
#     z_start_label = ttk.Label(root.add_quadcopter_window, text=Z)
#     z_start_label.config(background=BACKGROUND_COLOR)
#     z_start_label.grid(column=ZERO, row=THREE)
#     z_start_entry = tk.IntVar()
#     root.z_start_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=z_start_entry)
#     root.z_start_entered.grid(column=ONE, row=THREE)
#
#     # End coordinate
#     end_title_label = ttk.Label(root.add_quadcopter_window, text=END_COO_TEXT)
#     end_title_label.config(background=BACKGROUND_COLOR)
#     end_title_label.grid(column=TWO, row=ZERO)
#
#     x_end_label = ttk.Label(root.add_quadcopter_window, text=X)
#     x_end_label.config(background=BACKGROUND_COLOR)
#     x_end_label.grid(column=TWO, row=ONE)
#     x_end_entry = tk.IntVar()
#     root.x_end_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=x_end_entry)
#     root.x_end_entered.grid(column=THREE, row=ONE)
#
#     y_end_label = ttk.Label(root.add_quadcopter_window, text=Y)
#     y_end_label.config(background=BACKGROUND_COLOR)
#     y_end_label.grid(column=TWO, row=TWO)
#     y_end_entry = tk.IntVar()
#     root.y_end_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=y_end_entry)
#     root.y_end_entered.grid(column=THREE, row=TWO)
#
#     z_end_label = ttk.Label(root.add_quadcopter_window, text=Z)
#     z_end_label.config(background=BACKGROUND_COLOR)
#     z_end_label.grid(column=TWO, row=THREE)
#     z_end_entry = tk.IntVar()
#     root.z_end_entered = ttk.Entry(root.add_quadcopter_window, width=ENTRY_WIDTH, textvariable=z_end_entry)
#     root.z_end_entered.grid(column=THREE, row=THREE)
#
#     # Save button
#     save_button = tk.Button(root.add_quadcopter_window, text=SAVE_TEXT, bg=BUTTON_COLOR, command=close_canvas)
#     save_button.grid(column=ZERO, row=FOUR)


def close_canvas(path = ''):
    '''
    This is a help function to close canvas.
    The function calls to an update function to update the list of coordinates, and closes current window.
    :return: None
    '''
    if path == '':
        update_input_data(root.file_path.get())
    else:
        update_input_data(path)
    root.add_quadcopter_window.destroy()
    update_quadcopters_list()


def update_input_data(path):
    if(os.path.isfile(path)):
        with open(path) as inputs:
            data = json.load(inputs)
            print(data)
            for agent in data:
                input_data.append(tuple(data[agent][0]))
    else:
        messagebox.showwarning("Warning", "invalid path!")


# def update_input_data():
#     '''
#     A help function to save new coordinates in a list.
#     The function checks if all inputs are valid.
#     if they are - the new coordinates are save,
#     else - the user gets a warning message.
#     :return: None
#     '''
#     x1 = root.x_start_entered.get()
#     y1 = root.y_start_entered.get()
#     z1 = root.z_start_entered.get()
#     x2 = root.x_end_entered.get()
#     y2 = root.y_end_entered.get()
#     z2 = root.z_end_entered.get()
#     coordinates = [z1, y1, x1, z2, y2, x2]
#     if all(item.isnumeric() for item in coordinates):
#         coordinates = [int(coordinate) for coordinate in coordinates]
#         input_data.append(tuple(coordinates))
#     else:
#         messagebox.showwarning("Warning", "At least one coordinate is invalid.\nLast change was not saved")


def update_quadcopters_list():
    '''
    A help function to update quadcopers list.
    :return: None
    '''
    coordinates_str = ''
    for i, coordinates in enumerate(input_data):
        coordinates_str += f'\n{i + ONE}: {str(coordinates)}'
    root.quadcopters_label.configure(text=QUADCOPTERS_TEXT + coordinates_str, font=(FONT_TYPE, FONT_SIZE))


def reset():
    '''
    A help function to reset coordinates list and paths graph.
    :return: None
    '''
    global input_data
    input_data = []
    update_quadcopters_list()
    del_lab_label()


def del_lab_label():
    '''
    A help function to delete graph label.
    :return: None
    '''
    try:
        # del root.lab_draw
        root.lab_draw.destroy()
    except:
        pass


def calc_paths():
    '''
    A help function to calculate paths of quadcopers and draw them on a 3D graph.
    :return: None
    '''
    del_lab_label()

    # --------- real date received from user ----------------
    world = World(600, 800, 800)
    world.add_agents(input_data)  # add the agents to world
    agents = world.get_agents()
    paths = Search.path_finding(agents, world)  # get the paths for the agents
    paths = {34: [(5, 1, 9), (5, 1, 8), (5, 1, 7), (5, 1, 6), (5, 1, 5), (5, 1, 4), (5, 1, 3), (5, 1, 2), (5, 1, 1), (5, 1, 0), (5, 2, 0), (5, 3, 0), (5, 4, 0), (5, 5, 0), (5, 6, 0), (5, 7, 0), (5, 8, 0), (5, 9, 0), (4, 9, 0), (3, 9, 0), (2, 9, 0), (1, 9, 0), (0, 9, 0)], 39: [(1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 2, 6), (1, 2, 7), (1, 2, 8), (1, 2, 9), (1, 2, 10), (1, 3, 10), (2, 3, 10), (3, 3, 10), (3, 3, 10), (4, 3, 10), (5, 3, 10), (6, 3, 10), (7, 3, 10), (8, 3, 10), (9, 3, 10), (9, 3, 10), (9, 3, 10)], 41: [(2, 9, 5), (2, 9, 6), (2, 9, 7), (2, 9, 8), (2, 8, 8), (2, 7, 8), (2, 6, 8), (2, 5, 8), (2, 4, 8), (2, 3, 8), (3, 3, 8), (4, 3, 8), (5, 3, 8), (6, 3, 8), (7, 3, 8), (8, 3, 8), (9, 3, 8), (10, 3, 8), (10, 3, 8), (10, 3, 8), (10, 3, 8), (10, 3, 8), (10, 3, 8)], 36: [(1, 3, 3), (1, 3, 4), (1, 3, 5), (1, 3, 6), (1, 3, 7), (1, 3, 8), (1, 3, 9), (1, 3, 10), (1, 4, 10), (1, 5, 10), (1, 6, 10), (1, 7, 10), (1, 8, 10), (1, 9, 10), (1, 10, 10), (2, 10, 10), (3, 10, 10), (4, 10, 10), (4, 10, 10), (4, 10, 10), (4, 10, 10), (4, 10, 10), (4, 10, 10)], 18: [(0, 4, 6), (0, 4, 7), (0, 5, 7), (0, 6, 7), (0, 7, 7), (0, 8, 7), (0, 9, 7), (0, 10, 7), (1, 10, 7), (2, 10, 7), (3, 10, 7), (4, 10, 7), (5, 10, 7), (6, 10, 7), (7, 10, 7), (8, 10, 7), (9, 10, 7), (10, 10, 7), (10, 10, 7), (10, 10, 7), (10, 10, 7), (10, 10, 7), (10, 10, 7)], 38: [(7, 9, 3), (7, 9, 4), (7, 9, 5), (7, 9, 6), (7, 9, 7), (7, 9, 8), (7, 9, 9), (7, 9, 10), (7, 8, 10), (7, 7, 10), (7, 6, 10), (7, 5, 10), (7, 4, 10), (7, 3, 10), (7, 2, 10), (8, 2, 10), (9, 2, 10), (9, 2, 10), (9, 2, 10), (9, 2, 10), (9, 2, 10), (9, 2, 10), (9, 2, 10)], 10: [(6, 9, 2), (6, 9, 3), (6, 9, 4), (6, 9, 5), (6, 9, 6), (6, 9, 7), (6, 8, 7), (6, 7, 7), (6, 6, 7), (6, 5, 7), (6, 4, 7), (6, 3, 7), (6, 2, 7), (6, 1, 7), (5, 1, 7), (4, 1, 7), (3, 1, 7), (3, 1, 7), (3, 1, 7), (3, 1, 7), (3, 1, 7), (3, 1, 7), (3, 1, 7)], 37: [(3, 9, 3), (3, 9, 2), (3, 8, 2), (3, 7, 2), (4, 7, 2), (5, 7, 2), (5, 6, 2), (5, 5, 2), (5, 4, 2), (5, 3, 2), (5, 2, 2), (5, 1, 2), (6, 1, 2), (6, 0, 2), (7, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2), (8, 0, 2)], 27: [(4, 9, 3), (4, 9, 4), (4, 9, 5), (4, 9, 6), (4, 9, 7), (4, 9, 8), (4, 9, 9), (4, 9, 10), (4, 8, 10), (4, 7, 10), (4, 6, 10), (4, 5, 10), (4, 4, 10), (4, 3, 10), (4, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10), (3, 2, 10)], 24: [(8, 3, 6), (8, 3, 7), (8, 3, 8), (8, 3, 9), (8, 3, 10), (8, 4, 10), (7, 4, 10), (6, 4, 10), (5, 4, 10), (4, 4, 10), (3, 4, 10), (3, 4, 10), (3, 5, 10), (3, 6, 10), (3, 7, 10), (3, 8, 10), (3, 9, 10), (3, 9, 10), (3, 9, 10), (3, 9, 10), (3, 9, 10), (3, 9, 10), (3, 9, 10)], 17: [(2, 9, 7), (2, 8, 7), (2, 8, 6), (2, 8, 5), (2, 7, 5), (2, 6, 5), (2, 5, 5), (2, 4, 5), (2, 3, 5), (2, 2, 5), (2, 1, 5), (2, 0, 5), (3, 0, 5), (4, 0, 5), (5, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5), (6, 0, 5)], 16: [(9, 8, 8), (9, 8, 7), (9, 8, 6), (9, 8, 5), (9, 8, 4), (9, 8, 3), (9, 8, 2), (9, 7, 2), (9, 6, 2), (9, 5, 2), (9, 4, 2), (8, 4, 2), (7, 4, 2), (6, 4, 2), (5, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2), (4, 4, 2)], 15: [(2, 8, 2), (2, 8, 3), (2, 8, 4), (3, 8, 4), (3, 8, 5), (3, 7, 5), (3, 6, 5), (3, 5, 5), (3, 4, 5), (3, 3, 5), (3, 2, 5), (4, 2, 5), (5, 2, 5), (6, 2, 5), (7, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5), (8, 2, 5)], 23: [(7, 0, 5), (7, 0, 4), (7, 0, 3), (7, 0, 2), (7, 0, 1), (7, 1, 1), (7, 2, 1), (7, 3, 1), (7, 4, 1), (6, 4, 1), (5, 4, 1), (4, 4, 1), (3, 4, 1), (2, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1), (1, 4, 1)], 13: [(2, 1, 1), (2, 1, 2), (2, 1, 3), (2, 1, 4), (2, 1, 5), (2, 1, 6), (2, 1, 7), (2, 1, 8), (2, 2, 8), (3, 2, 8), (4, 2, 8), (5, 2, 8), (6, 2, 8), (6, 2, 8), (6, 2, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8), (6, 3, 8)], 47: [(6, 8, 4), (6, 8, 3), (6, 8, 2), (6, 7, 2), (6, 6, 2), (6, 5, 2), (6, 4, 2), (6, 3, 2), (6, 2, 2), (6, 1, 2), (6, 0, 2), (5, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2), (4, 0, 2)], 45: [(3, 0, 6), (3, 0, 7), (3, 0, 8), (3, 0, 9), (3, 1, 9), (3, 2, 9), (3, 3, 9), (3, 4, 9), (3, 5, 9), (3, 6, 9), (3, 7, 9), (4, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9), (5, 7, 9)], 21: [(8, 5, 2), (8, 5, 3), (8, 4, 3), (8, 3, 3), (8, 2, 3), (7, 2, 3), (7, 1, 3), (6, 1, 3), (5, 1, 3), (4, 1, 3), (3, 1, 3), (2, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3), (1, 1, 3)], 9: [(9, 1, 0), (9, 1, 1), (8, 1, 1), (8, 2, 1), (8, 3, 1), (8, 4, 1), (8, 5, 1), (8, 6, 1), (8, 7, 1), (8, 8, 1), (8, 9, 1), (8, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1), (7, 10, 1)], 31: [(8, 8, 8), (8, 8, 9), (8, 8, 10), (8, 7, 10), (8, 6, 10), (8, 5, 10), (7, 5, 10), (6, 5, 10), (5, 5, 10), (4, 5, 10), (3, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10), (2, 5, 10)], 5: [(0, 6, 0), (0, 6, 1), (0, 6, 2), (0, 6, 3), (0, 6, 4), (0, 6, 5), (0, 5, 5), (0, 4, 5), (0, 3, 5), (1, 3, 5), (2, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5), (3, 3, 5)], 3: [(7, 1, 0), (7, 1, 1), (7, 1, 2), (7, 1, 3), (8, 1, 3), (8, 1, 4), (8, 1, 5), (8, 1, 6), (8, 1, 7), (8, 1, 8), (8, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9), (9, 1, 9)], 49: [(3, 9, 6), (3, 9, 5), (3, 9, 4), (3, 9, 3), (3, 8, 3), (3, 7, 3), (3, 6, 3), (3, 5, 3), (3, 4, 3), (3, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3), (2, 3, 3)], 40: [(5, 9, 7), (5, 9, 8), (5, 8, 8), (5, 7, 8), (5, 6, 8), (5, 5, 8), (4, 5, 8), (3, 5, 8), (3, 5, 8), (2, 5, 8), (1, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8), (0, 5, 8)], 30: [(4, 0, 3), (4, 1, 3), (4, 2, 3), (4, 3, 3), (4, 4, 3), (4, 5, 3), (4, 6, 3), (5, 6, 3), (6, 6, 3), (7, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3), (8, 6, 3)], 20: [(8, 2, 2), (8, 2, 1), (8, 2, 0), (8, 3, 0), (7, 3, 0), (6, 3, 0), (5, 3, 0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0), (1, 3, 0)], 8: [(6, 7, 8), (6, 7, 7), (6, 7, 6), (6, 7, 5), (6, 7, 4), (5, 7, 4), (4, 7, 4), (3, 7, 4), (2, 7, 4), (1, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4), (0, 7, 4)], 1: [(5, 7, 3), (5, 7, 4), (5, 7, 5), (5, 7, 6), (5, 6, 6), (5, 5, 6), (6, 5, 6), (7, 5, 6), (8, 5, 6), (9, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6), (10, 5, 6)], 50: [(8, 0, 9), (8, 1, 9), (8, 2, 9), (7, 2, 9), (7, 3, 9), (7, 4, 9), (7, 5, 9), (7, 6, 9), (7, 7, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9), (7, 8, 9)], 35: [(6, 5, 3), (6, 5, 4), (6, 5, 5), (6, 5, 6), (6, 5, 7), (6, 5, 8), (6, 5, 9), (6, 6, 9), (6, 6, 9), (7, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9), (8, 6, 9)], 22: [(5, 2, 8), (5, 2, 9), (5, 3, 9), (5, 4, 9), (5, 5, 9), (5, 6, 9), (5, 7, 9), (5, 8, 9), (4, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9), (3, 8, 9)], 19: [(2, 7, 2), (2, 7, 3), (2, 7, 4), (2, 6, 4), (2, 5, 4), (2, 4, 4), (2, 3, 4), (2, 2, 4), (3, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4), (4, 2, 4)], 32: [(4, 2, 9), (4, 2, 10), (4, 1, 10), (5, 1, 10), (6, 1, 10), (7, 1, 10), (8, 1, 10), (9, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10), (10, 1, 10)], 25: [(0, 6, 8), (0, 6, 7), (0, 6, 6), (0, 6, 5), (0, 7, 5), (0, 7, 4), (0, 7, 3), (0, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2), (1, 7, 2)], 11: [(4, 8, 4), (4, 8, 5), (4, 8, 6), (4, 8, 7), (4, 8, 8), (4, 8, 9), (3, 8, 9), (3, 9, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9), (3, 10, 9)], 46: [(7, 1, 7), (7, 1, 6), (7, 1, 5), (7, 1, 4), (7, 2, 4), (7, 3, 4), (7, 3, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3), (7, 4, 3)], 44: [(6, 9, 6), (6, 9, 7), (6, 9, 8), (6, 9, 9), (6, 10, 9), (7, 10, 9), (8, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9), (9, 10, 9)], 33: [(3, 5, 4), (3, 5, 3), (3, 5, 2), (3, 6, 2), (4, 6, 2), (4, 6, 2), (4, 7, 2), (4, 8, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2), (4, 9, 2)], 28: [(5, 5, 0), (5, 5, 1), (5, 6, 1), (5, 7, 1), (5, 8, 1), (4, 8, 1), (3, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1), (2, 8, 1)], 4: [(5, 6, 2), (5, 6, 3), (5, 6, 4), (5, 6, 5), (5, 5, 5), (5, 4, 5), (5, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6), (6, 4, 6)], 2: [(6, 2, 2), (6, 1, 2), (6, 1, 3), (6, 1, 4), (6, 1, 5), (7, 1, 5), (7, 1, 5), (7, 1, 5), (8, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5), (9, 1, 5)], 43: [(6, 2, 3), (6, 3, 3), (6, 3, 2), (6, 3, 1), (6, 4, 1), (7, 4, 1), (7, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1), (8, 4, 1)], 14: [(3, 3, 5), (3, 3, 6), (3, 3, 7), (3, 3, 8), (3, 4, 8), (4, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8), (5, 4, 8)], 48: [(3, 7, 1), (3, 7, 0), (3, 8, 0), (3, 9, 0), (4, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (6, 9, 0), (6, 9, 0), (6, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0), (5, 9, 0)], 26: [(5, 1, 3), (5, 1, 2), (5, 1, 1), (5, 2, 1), (5, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1), (6, 3, 1)], 12: [(9, 2, 0), (9, 2, 1), (9, 2, 2), (9, 2, 3), (9, 3, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3), (9, 4, 3)], 42: [(8, 1, 4), (8, 1, 3), (8, 1, 2), (9, 1, 2), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1), (9, 1, 1)], 7: [(7, 9, 5), (8, 9, 5), (8, 9, 4), (8, 9, 3), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2), (8, 9, 2)], 29: [(1, 9, 2), (1, 8, 2), (1, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 8, 2), (0, 8, 2), (0, 8, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2), (0, 7, 2)], 6: [(2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 2, 2)]}
    paths = path_equalize(agents, paths)
    paths_with_time = {}
    j  = 0
    for agent in paths:
        j += 1
        if j>10:
            break
        paths_with_time[agent] = []
        for i, step in enumerate(paths[agent]):
            paths_with_time[agent].append((i,step[0], step[1], step[2]))
    print(paths_with_time)
    print(paths_with_time)
    # -------------------------------------------------------

    raw_data = paths_with_time

    """
    HERE YOU NEED TO SEND YOU REAL DATA!!
    """
    draw_graph(raw_data)

    add_graph_label()

    draw_gif()


def next_frame():
    try:
        # Move to the next frame
        root.photo.configure(format="gif -index {}".format(root.gif_index))
        root.gif_index += 1
    except tk.TclError:
        root.gif_index = 0
        return next_frame()
    else:
        root.after(100, next_frame) # XXX: Fixed animation speed


def draw_gif():
    '''
    A help function to draw the gif of the graph.
    :return: None
    '''
    global w, h
    px, py = TWO * WIDTH / THREE, HEIGHT / TEN
    root.photo = tk.PhotoImage(file=f'{GRAPH_NAME}{GRAPH_SUFFIX}')
    root.gif_index = 0
    root.lab_draw = tk.Label(root, image=root.photo, borderwidth=TWO, relief=LABEL_STYLE, text=GRAPH_TEXT)
    root.lab_draw.place(x=px, y=py)
    root.after_idle(next_frame)


def add_graph_label():
    '''
    A help function to add a label for the graph.
    :return: None
    '''
    global w, h
    px, py = TWO * WIDTH / THREE, HEIGHT / TEN
    root.lab_draw = tk.Label(root, borderwidth=TWO, relief=LABEL_STYLE, text=GRAPH_TEXT)
    root.lab_draw.place(x=px, y=py)
    root.lab_draw.config(width=w, height=h)


def main():
    '''
    This is the main function to illustrate the main window of control.
    :return: None
    '''
    root.config(bg=BACKGROUND_COLOR)

    _geom = '200x200+0+0'
    root.geometry("{0}x{1}+0+0".format(WIN_WIDTH, WIN_HEIGHT))
    root.bind('<Escape>', toggle_geom)

    root.quadcopters_label = ttk.Label(root, text=QUADCOPTERS_TEXT, font=(FONT_TYPE, FONT_SIZE))
    root.quadcopters_label.grid(column=ZERO, row=ZERO)
    root.quadcopters_label.config(background=BACKGROUND_COLOR)

    add_graph_label()

    px, py = TWO*WIDTH / THREE, FOUR*HEIGHT / FIVE + h
    add_button = tk.Button(root, text=ADD_TEXT, bg=BUTTON_COLOR, command=add_quadcopter)
    add_button.place(x=px, y=py)

    px, py = TWO*WIDTH / THREE, FOUR*HEIGHT / FIVE + TWO*h
    add_button = tk.Button(root, text=DRAW_TEXT, bg=BUTTON_COLOR, command=calc_paths)
    add_button.place(x=px, y=py)

    px, py = TWO*WIDTH / THREE, FOUR*HEIGHT / FIVE + THREE*h
    draw_button = tk.Button(root, text=RESET_TEXT, bg=BUTTON_COLOR, command=reset)
    draw_button.place(x=px, y=py)

    root.mainloop()
    return

# ======================================================================
# the method get list of agents and their paths, and make all of the paths in the same length, by duplicate the last step
def path_equalize(agents, paths, max_pathlen = -1):

    if(max_pathlen < 0):
        max_pathlen = get_max_pathlen(paths)

    for agent in paths:
        path = paths[agent]
        last_step = path[-1]
        for step in range(len(path), max_pathlen):
            path.append( (last_step[0], last_step[1], last_step[2] ) )
        paths[agent] = path
    return paths

def get_max_pathlen(paths):
    max_path_len = 0
    for agent in paths:
        if len(paths[agent]) > max_path_len:
            max_path_len = len(paths[agent])
    return max_path_len

def select_file():
    filetypes = (
        ('json files', '*.json'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    close_canvas(filename)
    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )
# ======================================================================


# if __name__ == "__main__":
#     main()
