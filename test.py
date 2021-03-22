from Vialization import *
from World import *
import Search
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
    # generate goals positions
    while num_of_pos < num_of_agents:
        z_goal = randrange(0, num_of_floors-1)
        y_goal = randrange(0, num_of_raws-1)
        x_goal = randrange(0, num_of_cols-1)
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




    #----------------------------draw the world-------------------------
    # vis = Visualize(world, paths )
    # vis.draw()
    # vis.frame.pack(fill=BOTH, expand=True)
    # vis.root.mainloop()
    #----------------------------draw the world-------------------------

