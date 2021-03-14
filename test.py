from Vialization import *
from World import *
import Search
a = World(600, 800, 800)
agents_pos = [(0,0,0,2,0,1), (9,9,1,2,3,0),(1,7,0,4,5,1), (7,0,0,1,5,0),(3,5,0,9,0,0),(9,0,0,0,9,0)]
#add the agents to world
a.add_agents(agents_pos)
agents = a.get_agents()
agents_current_steps, agents_prev_steps, conflict_steps = Search.find_path(agents, a, 1)         #get the paths for the agents
print(agents_current_steps)
print(agents_prev_steps)
print("conflict_steps; ", conflict_steps)

#----------------------------draw the world-------------------------
vis = Visualize(a)
vis.draw()
vis.canvas.pack(fill=BOTH, expand=True)
vis.root.mainloop()
#----------------------------draw the world-------------------------

