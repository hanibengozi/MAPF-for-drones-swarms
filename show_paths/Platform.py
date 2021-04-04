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
from algorithm_1.world import *
import algorithm_1.search as search
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
            print("befor converting data\n",data)
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
    print("the convert data\n", input_data)
    world.add_agents(input_data)  # add the agents to world
    agents = world.get_agents()
    paths, agents_without_solution = search.path_finding(agents, world)  # get the paths for the agents
    print(paths)
    # paths = path_equalize(agents, paths)
    paths_with_time = {}
    for agent in paths:
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

#if __name__ == "__main__":
    #main()