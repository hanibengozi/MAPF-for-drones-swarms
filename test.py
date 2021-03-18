from Vialization import *
from World import *
import Search
import time
start_time = time.time()

world = World(600, 800, 800)
agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0),(4,2,0,9,2,0)]
agents_pos_2 = [(7, 6, 0, 5, 1, 0), (5, 2, 0, 6, 4, 0), (0, 6, 0, 6, 1, 0), (0, 5, 0, 1, 7, 0), (3, 6, 0, 5, 5, 0)]

world.add_agents(agents_pos_2)                                     # add the agents to world
agents = world.get_agents()
paths = Search.path_finding(agents, world)         # get the paths for the agents
print(paths)
#print("conflict_steps; ", conflict_steps)
print("--- %s seconds ---" % (time.time() - start_time))
#-------------------------------------------------------------------




#----------------------------draw the world-------------------------


vis = Visualize(world, paths )
vis.draw()

vis.frame.pack(fill=BOTH, expand=True)
vis.root.mainloop()
#----------------------------draw the world-------------------------

