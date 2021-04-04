from tkinter import *
#from show_paths_step_by_step.Vialization import *
import test
import show_paths.Platform as p
from PIL import Image, ImageTk

class Dashboard(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        # self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        # self.entry = tk.Entry(self)
        self.title = Label(self, text = "\nWelcome to Multy Agent Pathfinding Project\n", font = "none 26 bold").pack()
        self.lbl1 = Label(self, text="Run 1000 random cases with the option to set all sizes and run the test and see the result on the screen.", font = "none 16")
        self.btn1 = Button(self, text="run", command = self.btn1_handler, font = "none 16")
        self.lbl2 = Label(self, text="Running of a comparison of the paths with collisions v.s paths without collisions, with a table of the description of the result and some deviation per drone", font = "none 16")
        self.btn2 = Button(self, text="run", command=self.btn2_handler, font = "none 16")
        self.lbl3 = Label(self, text="See the tracks in the company's visualization code", font = "none 16")
        self.btn3 = Button(self, text="run", command=self.btn3_handler, font = "none 16")
        self.lbl4 = Label(self, text="The vitalization screen that Yehudit made, which is seen in each unit of time for each skimmer current and previous point", font = "none 16")
        self.btn4 = Button(self, text="run", command=self.btn1_handler, font = "none 16")
        self.lbl5 = Label(self, text="validation screen When you press the button another screen opens where there are a lot of buttons, each button shows a different validation test", font = "none 16")
        self.btn5 = Button(self, text="run", command=self.btn1_handler, font = "none 16")

        self.lbl1.pack()
        self.btn1.pack()
        self.lbl2.pack()
        self.btn2.pack()
        self.lbl3.pack()
        self.btn3.pack()
        self.lbl4.pack()
        self.btn4.pack()
        self.lbl5.pack()
        self.btn5.pack()

    def btn1_handler(self):
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

    def btn2_handler(self):
        test.draw_paths_step_by_step()
        return

    def btn3_handler(self):
        p.main()
        return

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = Tk()
    root.title("pathfinding")
    root.state("zoomed")
    Dashboard(root).pack(fill="both", expand=True)
    root.mainloop()
