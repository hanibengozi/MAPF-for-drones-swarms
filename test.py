from world import *
import search
import test_function

# ---------------------------------define the world---------------------------------------

world = World(600,800,800)

# ---------------------------------define the agents pos--------------------------------------
agents_pos = test_function.random_inputs(6,8,8,50)
#agents_pos = [(7, 6, 0, 5, 1, 0), (5, 2, 0, 6, 4, 5), (0, 6, 0, 6, 1, 0), (0, 5, 0, 1, 7, 0), (3, 6, 0, 5, 5, 0), (0,0,0,2,0,1), (3,5,0,1,0,0),(4,2,0,5,2,0), (1,7,0,4,5,1) ]
#agents_pos = [(6, 5, 0, 2, 2, 0), (0, 7, 0, 4, 7, 0), (4, 6, 0, 0, 0, 0), (4, 4, 0, 3, 5, 0), (1, 3, 0, 0, 6, 0), (5, 4, 0, 3, 4, 0), (3, 6, 0, 3, 2, 0), (0, 6, 0, 2, 5, 0), (5, 5, 0, 2, 0, 0), (3, 5, 0, 0, 2, 0), (3, 1, 0, 3, 7, 0), (1, 1, 0, 1, 3, 0), (3, 7, 0, 4, 5, 0)]

# ---------------------------------- add the agents to world----------------------------------------

world.add_agents(agents_pos)
agents = world.get_agents()

# ----------------------------------find paths with conflicts------------------------------------

paths_with_conflicts = search.path_finding_with_conflicts(agents)

# ----------------------------------find paths without conflicts----------------------------------

paths = search.path_finding(agents, world)

# ---------------------------------printing the results--------------------------------------------

print("the agents:\n", agents_pos)
if not test_function.check_conflicts(agents, paths):
    print("the pathsssssssssssss:\n", paths)
    print("yessssssssssssssssssssssssssssssss")
else:
    print("the pathsssssssssssss:\n", paths)
    print("their are conflictssssssssssssssssss")
