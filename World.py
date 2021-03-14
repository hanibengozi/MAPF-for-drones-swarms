import numpy as np

class World:
    def __init__(self, height, width, length):
        self.height = height
        self.width = width
        self.length = length
        self.num_floors = 3
        self.num_rows = 10  #length
        self.num_cols = 10  #width
        self.starts_pos = {}
        self.goals_pos = {}
        self.agents = []
        self.num_agents = 0
        #self.floors = dict()
        #self.cells = np.zeros((length, width), dtype=int)

    #the functuon get list of agents position(start & end), end add them to world
    def add_agents(self,agents_pos):
        if agents_pos:
            for (start_x,start_y, start_z, goal_x,goal_y, goal_z) in agents_pos:
                # check the validation of the position
                if self.is_valid_pos((start_x,start_y, start_z)) and self.is_valid_pos((goal_x,goal_y, goal_z)):
                    self.num_agents += 1
                    self.starts_pos[self.num_agents] = (start_x,start_y, start_z)
                    self.goals_pos[self.num_agents] = (goal_x,goal_y, goal_z)
                    self.agents.append(self.num_agents)
                else:
                    raise Exception('Failure! invalid position of agent')
                    return False

    #get position of agent in world, and return if the position is valid
    def is_valid_pos(self, agent_pos):
        x,y,z = agent_pos
        if x < 0 or x > self.num_cols - 1 or y < 0 or y > self.num_rows - 1 or z < 0 or z > self.num_floors -1:
            return False
        else:
            return True

    # returns a list with the numbers 1 to number of agents.
    def get_agents(self):
        return self.agents