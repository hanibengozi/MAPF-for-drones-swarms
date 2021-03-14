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
floor_h = FRAME_HEIGHT/num_floors
cell_w = floor_w/num_cols
cell_h = floor_h/num_rows
class Visualize:
    def __init__(self, world_data):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg='white')
        self.canvas.grid()
        self.world = world_data
        world_data.visualize = self
        #self.cell_h, self.cell_w = self.get_cell_size()
        #self.agent_h, self.agent_w = self.get_agent_size(1)
        self.vis_cells = np.zeros((world_data.width, world_data.length, world_data.height), dtype=int)
        self.aindx_obj = dict()
        self.i = -1
        self.agents_steps =  {0: {6: (9, 0, 0), 5: (3, 5, 0), 4: (7, 0, 0), 3: (1, 7, 0), 2: (9, 9, 1), 1: (0, 0, 0)}, 1: {6: (9, 1, 0), 5: (3, 4, 0), 4: (7, 1, 0), 3: (1, 7, 1), 2: (9, 9, 0), 1: (0, 0, 1)}, 2: {6: (9, 2, 0), 5: (3, 3, 0), 4: (7, 2, 0), 3: (1, 6, 1), 2: (9, 8, 0), 1: (1, 0, 1)}, 3: {6: (9, 3, 0), 5: (3, 2, 0), 4: (7, 3, 0), 3: (1, 5, 1), 2: (9, 7, 0), 1: (2, 0, 1)}, 4: {6: (9, 4, 0), 5: (3, 1, 0), 4: (7, 4, 0), 3: (2, 5, 1), 2: (9, 6, 0)}, 5: {6: (9, 5, 0), 5: (3, 0, 0), 4: (7, 5, 0), 3: (3, 5, 1), 2: (9, 5, 0)}, 6: {6: (9, 6, 0), 5: (4, 0, 0), 4: (6, 5, 0), 3: (4, 5, 1), 2: (9, 4, 0)}, 7: {6: (9, 7, 0), 5: (5, 0, 0), 4: (5, 5, 0), 2: (9, 3, 0)}, 8: {6: (9, 8, 0), 5: (6, 0, 0), 4: (4, 5, 0), 2: (8, 3, 0)}, 9: {6: (9, 9, 0), 5: (7, 0, 0), 4: (3, 5, 0), 2: (7, 3, 0)}, 10: {6: (8, 9, 0), 5: (8, 0, 0), 4: (2, 5, 0), 2: (6, 3, 0)}, 11: {6: (7, 9, 0), 5: (9, 0, 0), 4: (1, 5, 0), 2: (5, 3, 0)}, 12: {6: (6, 9, 0), 2: (4, 3, 0)}, 13: {6: (5, 9, 0), 2: (3, 3, 0)}, 14: {6: (4, 9, 0), 2: (2, 3, 0)}, 15: {6: (3, 9, 0)}, 16: {6: (2, 9, 0)}, 17: {6: (1, 9, 0)}, 18: {6: (0, 9, 0)}}
        self.conflicts = [(9, 4, 0)]

    #draw the path for all agents
    def draw(self):
        for i in range(len(self.agents_steps)):
            self.draw_world()
            self.canvas.pack(fill=BOTH, expand=1)



    #draw  one step, for all agents
    def draw_one_step(self):
        if self.i == -1 or self.i > len(self.agents_steps) -1:   #for the first time, when load the world, and when thw steps finish
            self.i += 1
            return

        steps = self.agents_steps[self.i]
        self.i += 1
        self.draw_world()
        self.canvas.pack(fill=BOTH, expand=1)
        self.draw_agents(steps)
        self.canvas.pack(fill=BOTH, expand=1)



    #draw the world, all the floors, each floor like a grid
    def draw_world(self):

        #draw the lines
        for row in range(num_rows*num_floors):
            for col in range(num_cols):
                self.canvas.create_rectangle(FRAME_MARGIN + cell_w * col, FRAME_MARGIN + cell_h * row, FRAME_MARGIN + cell_w * (col+1), FRAME_MARGIN + cell_h * (row+1),outline='blue' )

        # draw the floors (num of floors)
        for row in range(num_floors):
            for col in range(1):
                self.canvas.create_rectangle(FRAME_MARGIN + floor_w * col, FRAME_MARGIN + floor_h * row, FRAME_MARGIN + floor_w * (col+1), FRAME_MARGIN + floor_h * (row+1),outline='red' )
        btn = Button(self.root, text='To the next step!', width=15,height=1, bd='10', command=self.draw_one_step)
        btn.place(x=floor_w/2, y=floor_h*num_floors +FRAME_MARGIN)

    #the function get pos of agent in world, and draw it
    def draw_agent(self, x,y,z, color):
        #if this pos is free
        if (x,y,z) not in self.conflicts:
            self.vis_cells[x][y][z] = self.canvas.create_rectangle(FRAME_MARGIN + x*cell_w, y*cell_h + z*floor_h + FRAME_MARGIN, FRAME_MARGIN + (x +1)*cell_w, (y+1)*cell_h + z*floor_h + FRAME_MARGIN, fill=color)
            self.vis_cells[x][y][z] = 1
        else:
            self.vis_cells[x][y][z] = self.canvas.create_rectangle(FRAME_MARGIN + x * cell_w, y * cell_h + z * floor_h + FRAME_MARGIN, FRAME_MARGIN + (x + 1) * cell_w, (y + 1) * cell_h + z * floor_h + FRAME_MARGIN, fill='red')
        self.canvas.itemconfig(self.vis_cells[x][y][z])

    #the function get position of agent and draw them.
    def draw_agents(self, steps):
        colors = ['purple', 'black', 'pink','green', 'blue','yellow']
        for agent in steps.keys():
            x,y,z = steps[agent]
            self.draw_agent(x,y,z,colors[agent -1])