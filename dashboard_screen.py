from tkinter import *
import tkinter as tk
from tkinter import ttk
#from show_paths_step_by_step.Vialization import *
import test
import show_paths.Platform as p
import test_dashboard as test


def btn1_handler(root):

    test_results = test.run_1000_cases()

    window = Tk()
    window.title("run 1000 cases")

    h = Scrollbar(window, orient=HORIZONTAL)
    h.pack(fill=X, side=BOTTOM, expand=FALSE)

    v = Scrollbar(window, orient=VERTICAL)
    v.pack(fill = Y, side = RIGHT, expand = FALSE)

    canvas = Canvas(window, bd=0, highlightthickness=0, yscrollcommand=v.set, xscrollcommand=h.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

    t = Text(canvas, xscrollcommand=h.set, yscrollcommand=v.set)
    t.insert(END, test_results)
    t.pack(side = LEFT, fill = BOTH, expand = TRUE)

    h.config(command=canvas.xview)
    v.config(command=canvas.yview)

    window.mainloop()
    return
def btn2_handler():
    test.draw_paths_step_by_step()
    return
def btn3_handler():
    p.main()
    return
def run_tests_btn():
    num_cases = int(root.num_of_cases_entry.get())
    num_agents = int(root.num_of_drones_entry.get())
    width = int(root.width_entry.get())
    height = int(root.height_entry.get())
    length = int(root.length_entry.get())
    test.run_algorithm_1(height, width, length, 0.25, 2, num_cases, num_agents)
    return
def run_tests():
    root.run_tests_win = tk.Toplevel(root)
    root.run_tests_win.title("run tests")
    root.canvas_run_tests_win = tk.Canvas(root.run_tests_win)

    title_lbl = ttk.Label(root.run_tests_win, text="to run the tests, fill the following:", font = "none 10 bold")
    title_lbl.grid(column=0, row=0, padx=20, pady=5)

    num_of_cases_lbl = ttk.Label(root.run_tests_win, text="how many cases would you like to run?")
    num_of_cases_lbl.grid(column=0, row=1, padx=20, pady=5)

    num_of_cases_entry = tk.IntVar()
    root.num_of_cases_entry = ttk.Entry(root.run_tests_win, width=10, textvariable=num_of_cases_entry)
    root.num_of_cases_entry.grid(column=1, row=1, padx=20, pady=5)

    num_of_drones_lbl = ttk.Label(root.run_tests_win, text="for how many drones would you like to run the cases?")
    num_of_drones_lbl.grid(column=0, row=2, padx=20, pady=5)

    num_of_drones_entry = tk.IntVar()
    root.num_of_drones_entry = ttk.Entry(root.run_tests_win, width=10, textvariable=num_of_drones_entry)
    root.num_of_drones_entry.grid(column=1, row=2, padx=20, pady=5)

    width_lbl = ttk.Label(root.run_tests_win, text="what is the width(x coordinate) size of the world (in meters)?")
    width_lbl.grid(column=0, row=3, padx=20, pady=5)

    width_entry = tk.IntVar()
    root.width_entry = ttk.Entry(root.run_tests_win, width=10, textvariable=width_entry)
    root.width_entry.grid(column=1, row=3, padx=20, pady=5)

    height_lbl = ttk.Label(root.run_tests_win, text="what is the height(y coordinate) size of the world (in meters)?")
    height_lbl.grid(column=0, row=4, padx=20, pady=5)

    height_entry = tk.IntVar()
    root.height_entry = ttk.Entry(root.run_tests_win, width=10, textvariable=height_entry)
    root.height_entry.grid(column=1, row=4, padx=20, pady=5)

    length_lbl = ttk.Label(root.run_tests_win, text="what is the length(z coordinate) size of the world (in meters)?")
    length_lbl.grid(column=0, row=5, padx=20, pady=5)

    length_entry = tk.IntVar()
    root.length_entry = ttk.Entry(root.run_tests_win, width=10, textvariable=length_entry)
    root.length_entry.grid(column=1, row=5, padx=20, pady=5)




    # choose file button
    run_btn = tk.Button(root.run_tests_win, text="run tests",command=run_tests_btn)
    run_btn.grid(column=0, row=6, padx=20, pady=10)

    # Save button
    # save_button = tk.Button(root.add_quadcopter_window, text=SAVE_TEXT, bg=BUTTON_COLOR, command=close_canvas)
    # save_button.grid(column=ZERO, row=FOUR)
    # return


root = tk.Toplevel()
root.title("pathfinding")
root.state("zoomed")

title = Label(root, text = "\nWelcome to Multy Agent Pathfinding Project\n", font = "none 26 bold").pack()
lbl1 = Label(root, text="Run Tests", font = "none 16")
btn1 = Button(root, text="run", command = run_tests, font = "none 16")
#lbl2 = Label(root, text="Show Paths Step by Step", font = "none 16")
#btn2 = Button(root, text="run", command=btn2_handler, font = "none 16")
lbl3 = Label(root, text="Simulate Paths in 3D Graph", font = "none 16")
btn3 = Button(root, text="run", command=btn3_handler, font = "none 16")

lbl1.pack()
btn1.pack()
#lbl2.pack()
#btn2.pack()
lbl3.pack()
btn3.pack()

root.mainloop()