from Vialization import *
from World import *
import Search
from random import seed, random
from random import randint

import time
from random import randrange


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


for i in range(5):
    start_time = time.time()
    world = World(600, 800, 800)
    agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0),(4,2,0,9,2,0)]
    agents_pos_2 = random_inputs(3,10,10,20)
    #print(agents_pos_2)
    world.add_agents(agents_pos_2)                                     # add the agents to world
    agents = world.get_agents()
    paths = Search.path_finding(agents, world)         # get the paths for the agents
    #print(paths)
    #print("conflict_steps; ", conflict_steps)
    print("--- %s seconds ---" % (time.time() - start_time))
#-------------------------------------------------------------------
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
    return max_pathlen

# the method get list of agents and their paths, and make all of the paths in the same length, by duplicate the last step
def path_equalize(agents, paths, max_pathlen = -1):

    if(max_pathlen < 0):
        max_pathlen = get_max_pathlen(agents, paths)

    for agent in agents:
        path = paths[agent]
        last_step = path[-1]
        for step in range(len(path), max_pathlen):
            path.append( (last_step[0], last_step[1], last_step[2] ) )
        paths[agent] = path
    return paths




#---------------------------main---------------------------------------------------------------------------------------
world = World(600, 800, 800)
agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0),(4,2,0,9,2,0)]
agents_pos_2 = [(7, 6, 0, 5, 1, 0), (5, 2, 0, 6, 4, 0), (0, 6, 0, 6, 1, 0), (0, 5, 0, 1, 7, 0), (3, 6, 0, 5, 5, 0), (0,0,0,2,0,1), (3,5,0,9,0,0),(4,2,0,9,2,0), (1,7,0,4,5,1) ]
agent_p = [(6, 5, 0, 2, 2, 0), (0, 7, 0, 4, 7, 0), (4, 6, 0, 0, 0, 0), (4, 4, 0, 3, 5, 0), (8, 3, 0, 8, 6, 0), (5, 4, 0, 3, 4, 0), (3, 6, 0, 3, 2, 0), (8, 6, 0, 2, 5, 0), (8, 5, 0, 2, 0, 0), (3, 5, 0, 0, 2, 0), (3, 1, 0, 3, 7, 0), (1, 1, 0, 1, 8, 0), (3, 8, 0, 4, 5, 0)]
agents_random_pos = random_inputs(9,9,3,13)
print("agents_random_pos: \n", agents_random_pos)

world.add_agents(agents_pos_2)                                     # add the agents to world
agents = world.get_agents()
paths = Search.path_finding(agents, world)         # get the paths for the agents
print(paths)
#print("conflict_steps; ", conflict_steps)
print("--- %s seconds ---" % (time.time() - start_time))


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
    # vis = Visualize(world, paths )
    # vis.draw()
    # vis.frame.pack(fill=BOTH, expand=True)
    # vis.root.mainloop()
    #----------------------------draw the world-------------------------



