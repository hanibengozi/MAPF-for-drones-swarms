from Vialization import *
from World import *
import Search

a = World(600, 800, 800)
agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0),(4,2,0,9,2,0)]
#add the agents to world
a.add_agents(agents_pos)
agents = a.get_agents()
paths , conflict_steps = Search.find_path(agents, a)         #get the paths for the agents
print(paths)
print("conflict_steps; ", conflict_steps)

#----------------------------draw the world-------------------------


vis = Visualize(a, paths , conflict_steps)
vis.draw()

vis.frame.pack(fill=BOTH, expand=True)
vis.root.mainloop()
#----------------------------draw the world-------------------------

