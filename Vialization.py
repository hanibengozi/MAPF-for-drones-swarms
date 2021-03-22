from World import *
from tkinter import *
import numpy as np

FRAME_WIDTH = 600
FRAME_HEIGHT = 600
FRAME_MARGIN = 10
CELL_MARGIN = 5
num_floors = 3
num_cols = 10
num_rows = 10
floor_w = FRAME_WIDTH
floor_h = FRAME_HEIGHT / num_floors
cell_w = floor_w/num_cols
cell_h = floor_h/num_rows



#scroll Frame class
class ScrollableFrame(Frame):
    def __init__(self, parent, minimal_canvas_size, *args, **kw):
        '''
        Constructor
        '''

        Frame.__init__(self, parent, *args, **kw)

        self.minimal_canvas_size = minimal_canvas_size

        # create a vertical scrollbar
        vscrollbar = Scrollbar(self, orient = VERTICAL)
        vscrollbar.pack(fill = Y, side = RIGHT, expand = FALSE)

        # create a horizontal scrollbar
        hscrollbar = Scrollbar(self, orient = HORIZONTAL)
        hscrollbar.pack(fill = X, side = BOTTOM, expand = FALSE)

        #Create a canvas object and associate the scrollbars with it
        self.canvas = Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set)
        self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)

        #Associate scrollbars with canvas view
        vscrollbar.config(command = self.canvas.yview)
        hscrollbar.config(command = self.canvas.xview)


        # set the view to 0,0 at initialization

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvas.config(scrollregion='0 0 %s %s' % self.minimal_canvas_size)

        # create an interior frame to be created inside the canvas

        self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (max(interior.winfo_reqwidth(), self.minimal_canvas_size[0]), max(interior.winfo_reqheight(), self.minimal_canvas_size[1]))
            self.canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width = interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

#the canvas class
class Visualize:
    def __init__(self, world_data, paths, conflicts_steps=None):
        self.root = Tk()

        minimal_canvas_size = (FRAME_WIDTH, FRAME_HEIGHT)

        # create frame (gray window)
        self.frame = ScrollableFrame(self.root, minimal_canvas_size)
        self.frame.pack(fill=BOTH, expand=YES)

        self.world = world_data
        world_data.visualize = self
        self.i = -1
        self.agents_path = paths
        self.conflicts = conflicts_steps
        self.get_max_path_len()          # get the num steps
        self.set_gaols_pos()
        # self.cell_h, self.cell_w = self.get_cell_size()
        # self.agent_h, self.agent_w = self.get_agent_size(1)
        self.vis_cells = np.zeros((world_data.width, world_data.length, world_data.height), dtype=int)
        #self.aindx_obj = dict()

    def set_gaols_pos(self):
        self.goals = []
        for agent_id in self.agents_path:
            self.goals.append(self.agents_path[agent_id][-1])

    def get_max_path_len(self):
        max_pathlen = 0
        for agent in self.agents_path.keys():
            if len(self.agents_path[agent]) > max_pathlen:
                max_pathlen = len(self.agents_path[agent])
        self.num_steps = max_pathlen

    def get_currentStep(self):
        current_steps = []
        goal_steps = {}
        for agent in self.agents_path:
            if len(self.agents_path[agent]) > self.i:
                current_steps.append(self.agents_path[agent][self.i])
            else:
                current_steps.append(None)
                goal_steps[agent] = self.agents_path[agent][-1]

        return current_steps, goal_steps

    def get_prevStep(self):
        prev_steps = []
        if self.i:
            for agent in self.agents_path:
                if len(self.agents_path[agent]) > self.i:
                    prev_steps.append(self.agents_path[agent][self.i - 1])
                else:
                    prev_steps.append(None)
        return prev_steps

    # draw the path for all agents
    def draw(self):
        for i in range(self.num_steps):
            self.draw_world()
            self.frame.pack(fill=BOTH, expand=1)

    #draw  one step, for all agents
    def draw_one_step(self):
        if self.i == -1 or self.i > self.num_steps:   #for the first time, when load the world, and when thw steps finish
            self.i += 1
            return

        current_steps, goal_steps = self.get_currentStep()
        prev_steps = self.get_prevStep()
        self.frame.canvas.delete("all")
        self.draw_world()
        self.draw_agents(current_steps, prev_steps, goal_steps)
        self.frame.pack(fill=BOTH, expand=1)
        self.i += 1

    #draw the world, all the floors, each floor like a grid
    def draw_world(self):

        #draw the lines
        for row in range(num_rows*num_floors):
            for col in range(num_cols):
                self.frame.canvas.create_rectangle(FRAME_MARGIN + cell_w * col, FRAME_MARGIN + cell_h * row, FRAME_MARGIN + cell_w * (col+1), FRAME_MARGIN + cell_h * (row+1),outline='blue' )

        # draw the floors (num of floors)
        for row in range(num_floors):
            for col in range(1):
                self.frame.canvas.create_rectangle(FRAME_MARGIN + floor_w * col, FRAME_MARGIN + floor_h * row, FRAME_MARGIN + floor_w * (col+1), FRAME_MARGIN + floor_h * (row+1),outline='red' )
        btn = Button(self.root, text='To the next step!', width=15,height=1, bd='10', command=self.draw_one_step)
        btn.place(x=floor_w/2, y=floor_h*num_floors +FRAME_MARGIN)

    #the function get pos of agent in world, and draw it
    def draw_agent(self, x,y,z, color, goal=0):
        """if goal:
            self.vis_cells[x][y][z] = self.frame.canvas.create_rectangle(FRAME_MARGIN + x * cell_w, y * cell_h + z * floor_h + FRAME_MARGIN, FRAME_MARGIN + (x + 1) * cell_w, (y + 1) * cell_h + z * floor_h + FRAME_MARGIN, width=3, outline=color, fill='white')
            self.frame.canvas.itemconfig(self.vis_cells[x][y][z])
            return"""

        if not self.i or not self.conflicts:                                         # for the first step
            self.vis_cells[x][y][z] = self.frame.canvas.create_rectangle(FRAME_MARGIN + x * cell_w,y * cell_h + z * floor_h + FRAME_MARGIN,FRAME_MARGIN + (x + 1) * cell_w,(y + 1) * cell_h + z * floor_h + FRAME_MARGIN,fill=color)
            self.vis_cells[x][y][z] = 1
            return
        if self.conflicts and (x,y,z) not in self.conflicts[self.i - 1]:          # if this pos is without conflicts
            self.vis_cells[x][y][z] = self.frame.canvas.create_rectangle(FRAME_MARGIN + x*cell_w, y*cell_h + z*floor_h + FRAME_MARGIN, FRAME_MARGIN + (x +1)*cell_w, (y+1)*cell_h + z*floor_h + FRAME_MARGIN, fill=color)
            self.vis_cells[x][y][z] = 1
        else:
            self.vis_cells[x][y][z] = self.frame.canvas.create_rectangle(FRAME_MARGIN + x * cell_w, y * cell_h + z * floor_h + FRAME_MARGIN, FRAME_MARGIN + (x + 1) * cell_w, (y + 1) * cell_h + z * floor_h + FRAME_MARGIN, fill='red')


        self.frame.canvas.itemconfig(self.vis_cells[x][y][z])

    #the function get position of agent and draw them. if type==1 this is current steps else is preve steps
    def draw_agents(self, current_steps, preve_steps, goal_steps):
        colors_current = ['purple', 'black', 'pink', 'green', 'blue', 'yellow', 'orange', '#663300', '#ff0066', '#476b6b', '#4dff4d', '#999999', '#33ccff', '#666699']
        colors_prev = ['#e600e6', '#808080', '#ffccd5', '#4dff4d', '#8080ff', '#ffff80', '#ffd280', '#cc6600', '#ff80b3', '#85adad', '#99ff99', '#cccccc', '#99e6ff', '#b3b3cc']

        for i, step in enumerate(current_steps):
            if step:
                x,y,z = step
                self.draw_agent(x,y,z,colors_current[i])
        if preve_steps:
            for i, step in enumerate(preve_steps):
                if step:
                    x,y,z = step
                    self.draw_agent(x,y,z,colors_prev[i])
        if goal_steps:
            for agent in goal_steps:
                if goal_steps[agent]:
                    x,y,z = goal_steps[agent]
                    self.draw_agent(x,y,z,colors_current[agent - 1])

        """for goal_pos in self.goals:
            x,y,z = goal_pos
            self.draw_agent(x, y, z, colors_current[self.goals.index(goal_pos)], 1)"""

