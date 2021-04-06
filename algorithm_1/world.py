import numpy as np
from algorithm_1.drone import *
import math

class World:
    def __init__(self, height, width, length, agent_radius, security_distance):
        self.height = height
        self.width = width
        self.length = length
        self.num_floors = math.ceil(height / (agent_radius * 2 + security_distance))
        self.num_rows = math.ceil(length / (agent_radius * 2 + security_distance))         # length
        self.num_cols = math.ceil(width / (agent_radius * 2 + security_distance))          # width
        self.agents = []                              # list of agent object

    #the functuon get list of agents position(start & end), end add them to world
    def add_agents(self, agents_pos):
        start_pos = []
        goal_pos = []
        self.agents = agents_pos
        if agents_pos:
            for agent_id, (start_x,start_y, start_z, goal_x,goal_y, goal_z) in enumerate(agents_pos):

                # check the validation of the position
                if self.is_valid_pos((start_x,start_y, start_z)) and self.is_valid_pos((goal_x,goal_y, goal_z)):
                    self.agents[agent_id] = Drone(agent_id + 1, (start_x, start_y, start_z),(goal_x, goal_y, goal_z))
                else:
                    raise Exception('Failure! invalid position of agent')
                    return False

                # check that their are not equals start  and goal pos
                if (start_x,start_y, start_z) not in start_pos:
                    start_pos.append((start_x,start_y, start_z))
                else:
                    print("start",(start_x,start_y, start_z))
                    # raise Exception('Failure! their are conflicts in drones start position')
                    # return False
                if (goal_x,goal_y, goal_z) not in goal_pos:
                    goal_pos.append((goal_x,goal_y, goal_z))
                else:
                    print("goal", (goal_x,goal_y, goal_z))
                    raise Exception('Failure! their are conflicts in drones goals position')
                    return False

    #get position of agent in world, and return if the position is valid
    def is_valid_pos(self, agent_pos):
        x, y, z = agent_pos
        if x < 0 or x > self.num_cols - 1 or y < 0 or y > self.num_rows - 1 or z < 0 or z > self.num_floors -1:
            return False
        else:
            return True

    # returns a list with the numbers 1 to number of agents.
    def get_agents(self):
        return self.agents