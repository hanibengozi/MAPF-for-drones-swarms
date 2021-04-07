from tkinter import *
import tkinter as tk
from tkinter import ttk
#from show_paths_step_by_step.Vialization import *
import show_paths.Platform as p
import test_dashboard as test

def show_test_result(result):
    window = Tk()
    window.title("run 1000 cases")

    h = Scrollbar(window, orient=HORIZONTAL)
    h.pack(fill=X, side=BOTTOM, expand=FALSE)

    v = Scrollbar(window, orient=VERTICAL)
    v.pack(fill=Y, side=RIGHT, expand=FALSE)

    canvas = Canvas(window, bd=0, highlightthickness=0, yscrollcommand=v.set, xscrollcommand=h.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

    t = Text(canvas, xscrollcommand=h.set, yscrollcommand=v.set)
    t.insert(END, result)
    t.pack(side=LEFT, fill=BOTH, expand=TRUE)

    h.config(command=canvas.xview)
    v.config(command=canvas.yview)

    window.mainloop()
    return
def show_paths_3d():
    p.main()
    return
def run_tests_btn():
    num_cases = int(root.num_of_cases_entry.get())
    num_agents = int(root.num_of_drones_entry.get())
    alg = root.tkvarq.get()
    result = test.show_num_cases(num_cases, num_agents, alg)
    print(result)
    show_test_result(result)
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

    choose_algo_lbl = ttk.Label(root.run_tests_win, text="in which algorithm would you like to run the cases?")
    choose_algo_lbl.grid(column=0, row=3, padx=20, pady=5)

    options = ["algorithm 1", "algorithm 2"]
    root.tkvarq = StringVar(root.run_tests_win)
    root.tkvarq.set(options[0])
    choose_algo = ttk.OptionMenu(root.run_tests_win, root.tkvarq, *options)
    choose_algo.grid(column=1, row=3, padx=20, pady=5)

     # choose file button
    run_btn = tk.Button(root.run_tests_win, text="run tests",command=run_tests_btn)
    run_btn.grid(column=0, row=6, padx=20, pady=10)
    return





root = tk.Toplevel()
root.title("pathfinding")
root.state("zoomed")

title = Label(root, text = "\nWelcome to Multy Agent Pathfinding Project\n", font = "none 26 bold").pack()
lbl1 = Label(root, text="Run Tests", font = "none 16")
btn1 = Button(root, text="run", command = run_tests, font = "none 16")
lbl3 = Label(root, text="Simulate Paths in 3D Graph", font = "none 16")
btn3 = Button(root, text="run", command = show_paths_3d, font = "none 16")

lbl1.pack()
btn1.pack()
lbl3.pack()
btn3.pack()

root.mainloop()