from Vialization import *
from World import *
import Search
import fast_search
from random import seed, random, randrange
from random import randint
import math
import time
start_time = time.time()
"""
def get_agent_random_pos():
    agents_pos = []
    for i in range(13):
        agents_random_pos = random_inputs(9, 9, 3)
        agents_pos.append(agents_random_pos)
    return agents_pos
def random_inputs(num_of_cols, num_of_raws,num_of_floors , num_of_agents):
    agents_random_pos = []
    # seed random number generator
    seed(0.9)
    # generate some integers
    num_of_pos = 0
    goal_random_pos = []
    starts_random_pos = []
    while num_of_pos < num_of_agents:
        z_start = randint(0, num_of_floors-1)
        y_start = randint(0, num_of_raws-1)
        x_start = randint(0, num_of_cols-1)
        start_pos = (x_start, y_start, z_start)
        if start_pos not in starts_random_pos:
            starts_random_pos.append(start_pos)
            num_of_pos += 1
    num_of_pos = 0
    while num_of_pos < num_of_agents:
        z_goal = randint(0, num_of_floors-1)
        y_goal = randint(0, num_of_raws-1)
        x_goal = randint(0, num_of_cols-1)
        goal_pos = (x_goal, y_goal, z_goal)
        if goal_pos not in goal_random_pos:
            goal_random_pos.append(goal_pos)
            num_of_pos += 1
    for i in range(num_of_agents):
        agents_random_pos.append(starts_random_pos[i]+goal_random_pos[i])
    return agents_random_pos

def check_paths(agents, paths):
    steps_map = dict()
    # declarate the conflict_db
    conflicts_db = dict()
    # mix the agents list.
    random.shuffle(agents)
    for agent in agents:
        if (agent not in conflicts_db):
            conflicts_db[agent] = set()
            if (paths[agent]):
                pathlen = len(paths[agent])
        # pass on the agent path, and check conflicts
        for time, tstep in enumerate(paths[agent]):
            two_steps = [tstep]
            if (time > 0): two_steps.append(tplusone(paths[agent][time - 1]))
            for step in two_steps:
                # creat a map from all the steps, and for each step save the first agent that belong to the step
                if (step not in steps_map):
                    steps_map[step] = agent
                # in case the step already in the steps map, checking for conflicts
                else:
                    other_agent = steps_map[step]
                    if (step not in conflicts_db[agent] and agent != other_agent):
                        conflicts_db[agent].update({step})
                        conflicts_db[other_agent].update({step})
    return conflicts_db

#gets a step and increase in 1 the time.
def tplusone(step):
    return ( (step[0]+1, step[1], step[2]) )
#the method get list of agents and their paths, and return the max path length
def get_max_pathlen(agents, paths):
    max_pathlen = 0
    for agent in agents:
        pathlen = len(paths[agent])
        max_pathlen = pathlen if pathlen > max_pathlen else max_pathlen
    return max_pathlen"""



#---------------------------main---------------------------------------------------------------------------------------
"""world = World(600, 800, 800)
agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0),(4,2,0,9,2,0)]
agents_pos_2 = [(7, 6, 0, 5, 1, 0), (5, 2, 0, 6, 4, 0), (0, 6, 0, 6, 1, 0), (0, 5, 0, 1, 7, 0), (3, 6, 0, 5, 5, 0), (0,0,0,2,0,1), (3,5,0,9,0,0),(4,2,0,9,2,0), (1,7,0,4,5,1) ]
agent_p = [(6, 5, 0, 2, 2, 0), (0, 7, 0, 4, 7, 0), (4, 6, 0, 0, 0, 0), (4, 4, 0, 3, 5, 0), (8, 3, 0, 8, 6, 0), (5, 4, 0, 3, 4, 0), (3, 6, 0, 3, 2, 0), (8, 6, 0, 2, 5, 0), (8, 5, 0, 2, 0, 0), (3, 5, 0, 0, 2, 0), (3, 1, 0, 3, 7, 0), (1, 1, 0, 1, 8, 0), (3, 8, 0, 4, 5, 0)]
agents_random_pos = random_inputs(9,9,3,13)
print("agents_random_pos: \n", agents_random_pos)

world.add_agents(agents_pos)                                     # add the agents to world
agents = world.get_agents()
paths = Search.path_finding(agents, world)         # get the paths for the agents
print(paths)
#print("conflict_steps; ", conflict_steps)
print("--- %s seconds ---" % (time.time() - start_time))"""


#---------------------------check_paths----------------------------------------
"""list_agent_id = []
for agent in agents:
    list_agent_id.append(agent.id)
max_path_len = get_max_pathlen(list_agent_id, paths)
paths_equalize = path_equalize(list_agent_id,paths,max_path_len)
print(paths_equalize)
conflicts = check_paths(list_agent_id, paths_equalize)
if conflicts:
    print("their is a conflictttttttttttttttttttttttttttttttttttttttttttt")
    print(conflicts)
else:
    print("yessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")"""



#----------------------------draw the world-------------------------


"""vis = Visualize(world, paths )
vis.draw()

vis.frame.pack(fill=BOTH, expand=True)
vis.root.mainloop()"""
#----------------------------draw the world-------------------------"""



#generates random start and gaol positions for each agent.
def random_inputs(num_of_floors, num_of_raws, num_of_cols, num_of_agents):
    agents_random_pos = []
    # seed random number generator
    #seed(1)
    num_of_pos = 0
    goal_random_pos = []
    starts_random_pos = []
    #generate starts positions
    while num_of_pos < num_of_agents:
        z_start = randrange(0, num_of_floors-1)
        y_start = randrange(0, num_of_raws-1)
        x_start = randrange(0, num_of_cols-1)
        start_pos = (x_start, y_start, z_start)
        if start_pos not in starts_random_pos:
            starts_random_pos.append(start_pos)
            num_of_pos += 1
    num_of_pos = 0
    while num_of_pos < num_of_agents:
        z_goal = randint(0, num_of_floors-1)
        y_goal = randint(0, num_of_raws-1)
        x_goal = randint(0, num_of_cols-1)
        goal_pos = (x_goal, y_goal, z_goal)
        if goal_pos not in goal_random_pos:
            goal_random_pos.append(goal_pos)
            num_of_pos += 1
    for i in range(num_of_agents):
        agents_random_pos.append(starts_random_pos[i]+goal_random_pos[i])
    return agents_random_pos

def path_length_ratio(agents, world):
    path_with_conflict = Search.path_finding_with_conflicts(agents, world)

    length_paths_with_conflict = []
    length_paths = []
    # calculate the length of the paths with conflicts
    for agent in paths:
        length = 0
        for pos_index in range(1, len(paths[agent])):
            x1, y1, z1 = paths[agent][pos_index]
            x2, y2, z2 = paths[agent][pos_index - 1]
            length += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2)* 1.0) # Linear distance
        length_paths.append(length)
    for agent in path_with_conflict:
        length = 0
        for pos_index in range(1, len(path_with_conflict[agent])):
            x1, y1, z1 = path_with_conflict[agent][pos_index]
            x2, y2, z2 = path_with_conflict[agent][pos_index - 1]
            length += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2)* 1.0) # Linear distance
        length_paths_with_conflict.append(length)
    print(length_paths_with_conflict)
    print(length_paths)
    for length in range(len(length_paths)):
        length_paths[length] = length_paths[length] - length_paths_with_conflict[length]
    return length_paths

def check_conflicts(agents, paths):
    max_path_len = get_max_pathlen(paths)
    paths = path_equalize(agents, paths)
    time = 0
    current_steps = []
    while time < max_path_len:
        for agent in paths:
            if time < len(paths[agent]):
                step = paths[agent][time]
                if step not in current_steps:
                    current_steps.append(step)
                else:
                    print("curent step: ", current_steps, "time: ", time)
                    return True
                if time > 0:
                    step = paths[agent][time - 1]
                    if step not in current_steps:
                        current_steps.append(step)
                    elif step != paths[agent][time]:
                        print("curent step: ", current_steps, "time: ", time)
                        return True
        current_steps = []
        time += 1

    return False

def get_max_pathlen(paths):
    max_path_len = 0
    for agent in paths:
        if len(paths[agent]) > max_path_len:
            max_path_len = len(paths[agent])
    return max_path_len

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

def main():

    count = 0
    for i in range(1000):
        world = World(600, 800, 800)
        agents_pos = random_inputs(6, 8, 8, 50)
        world.add_agents(agents_pos)                # add the agents to world
        agents = world.get_agents()
        paths = Search.path_finding(agents, world)  # get the paths for the agents
        if paths:
            if not check_conflicts(agents, paths):
                count += 1
                #path_len_ratio = path_length_ratio(agents, world)
                #print("the agents pos:\n", agents_pos, "\nthe paths: \n", paths, "\nSucssiedddddddd\n", "path_len_ratio\n", path_len_ratio)
            else:
                print("their is a conflictssssssssssssssss\n")
        else:
            print("the algorithem didnt find paths for this agents_pos\n")


#main()

world = World(600, 800, 800)
agents_pos = random_inputs(3,8,8,13)
print(agents_pos)
world.add_agents(agents_pos)                # add the agents to world
agents = world.get_agents()
paths_with_collision = Search.path_finding_with_conflicts(agents, world)
max_path_len_with_collision = get_max_pathlen(paths_with_collision)
paths = Search.path_finding(agents, world)  # get the paths for the agents
print("--- %s seconds ---" % (time.time() - start_time))
print(paths)
if not check_conflicts(agents, paths):
    print("okkkkkkkkkkkkkkkkkkkkkkkkk")
vis = Visualize(world, paths )
vis.draw()

vis.frame.pack(fill=BOTH, expand=True)
vis.root.mainloop()



"""world = World(600, 800, 800)
agents_pos = random_inputs(6,8,8,50)
print("agents pos: \n", agents_pos)
world.add_agents(agents_pos)                # add the agents to world
agents = world.get_agents()
paths = Search.path_finding(agents, world)  # get the paths for the agents
print("--- %s seconds ---" % (time.time() - start_time))
print("paths\n", paths)
if paths:
    if not check_conflicts(agents, paths):
        print("okkkkkkkkkkkkkkkkkkkkk")
        path_len_ratio = path_length_ratio(agents, world)
        print(path_len_ratio)
    else:
        print("not okkkkkkkkkkkkkkk")"""

"""world = World(600, 800, 800)
agents_pos = [(0, 2, 0, 2, 0, 0), (1, 0, 0, 7, 1, 2), (3, 6, 2, 6, 5, 5), (1, 6, 2, 4, 3, 2), (2, 6, 0, 0, 2, 4), (0, 4, 2, 1, 6, 2), (4, 0, 1, 0, 2, 0), (4, 6, 4, 0, 1, 2), (6, 2, 3, 6, 5, 3), (5, 0, 0, 3, 4, 1), (6, 3, 2, 3, 2, 0), (1, 6, 4, 2, 3, 4), (0, 4, 4, 7, 0, 0), (2, 0, 3, 1, 1, 4), (2, 6, 1, 2, 4, 1), (5, 0, 2, 1, 5, 2), (2, 4, 1, 6, 3, 4), (6, 0, 0, 5, 7, 1), (4, 1, 3, 4, 1, 1), (6, 2, 1, 7, 4, 1), (1, 3, 2, 1, 4, 4), (0, 1, 3, 3, 0, 4), (4, 5, 2, 1, 5, 4), (6, 5, 2, 4, 3, 5), (3, 5, 0, 0, 2, 1), (3, 3, 4, 3, 2, 4), (0, 3, 2, 1, 6, 5), (3, 6, 0, 7, 5, 4), (6, 2, 4, 3, 1, 3), (0, 4, 0, 2, 3, 1), (5, 1, 0, 4, 7, 5), (5, 5, 4, 5, 0, 0), (4, 3, 3, 3, 6, 0), (5, 5, 2, 0, 1, 3), (1, 4, 3, 7, 7, 3), (1, 5, 3, 5, 2, 3), (5, 5, 1, 5, 1, 2), (0, 3, 0, 6, 4, 4), (6, 3, 0, 4, 6, 1), (0, 0, 2, 7, 7, 4), (6, 1, 3, 1, 1, 0), (1, 5, 1, 0, 2, 5), (0, 2, 1, 1, 0, 2), (2, 6, 2, 4, 1, 3), (1, 2, 3, 5, 4, 0), (6, 4, 1, 1, 2, 4), (2, 1, 0, 7, 3, 5), (4, 3, 4, 7, 1, 1), (4, 4, 4, 2, 2, 5), (3, 4, 0, 2, 4, 3)]
world.add_agents(agents_pos)                # add the agents to world
agents = world.get_agents()
paths = Search.path_finding(agents, world)  # get the paths for the agents"""
