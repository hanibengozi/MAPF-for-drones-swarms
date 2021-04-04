from world import *
import search
import test_function

# ---------------------------------define the world---------------------------------------

world = World(600,800,800)

# ---------------------------------define the agents pos--------------------------------------
#agents_pos = test_function.random_inputs(6,8,8,50)
#1agents_pos = [(7, 6, 0, 5, 1, 0), (5, 2, 0, 6, 4, 5), (0, 6, 0, 6, 1, 0), (0, 5, 0, 1, 7, 0), (3, 6, 0, 5, 5, 0), (0,0,0,2,0,1), (3,5,0,1,0,0),(4,2,0,5,2,0), (1,7,0,4,5,1) ]
#1agents_pos =  [(6, 0, 3, 1, 3, 3), (2, 1, 4, 6, 3, 3), (4, 3, 0, 6, 0, 2), (2, 6, 3, 3, 4, 0), (3, 3, 4, 4, 2, 1), (1, 4, 3, 2, 1, 5), (5, 0, 0, 0, 0, 5), (2, 3, 3, 5, 3, 4), (0, 4, 2, 3, 0, 3), (1, 0, 3, 7, 4, 4)]
#1agents_pos = [(6, 5, 0, 2, 2, 0), (0, 7, 0, 4, 7, 0), (4, 6, 0, 0, 0, 0), (4, 4, 0, 3, 5, 0), (1, 3, 0, 0, 6, 0), (5, 4, 0, 3, 4, 0), (3, 6, 0, 3, 2, 0), (0, 6, 0, 2, 5, 0), (5, 5, 0, 2, 0, 0), (3, 5, 0, 0, 2, 0), (3, 1, 0, 3, 7, 0), (1, 1, 0, 1, 3, 0), (3, 7, 0, 4, 5, 0)]
#1agents_pos = [(5, 3, 1, 2, 5, 5), (1, 1, 1, 2, 6, 2), (5, 3, 4, 0, 2, 3), (0, 2, 2, 5, 3, 3), (6, 3, 3, 6, 5, 1), (0, 2, 1, 5, 1, 5), (5, 1, 1, 4, 3, 2), (5, 6, 3, 6, 7, 3), (3, 5, 1, 2, 7, 0), (1, 2, 2, 2, 7, 3), (0, 0, 2, 4, 3, 3), (1, 1, 2, 2, 2, 4), (3, 6, 1, 0, 7, 5), (3, 1, 3, 4, 5, 5), (4, 2, 4, 7, 0, 0), (2, 5, 2, 1, 0, 0), (4, 1, 1, 3, 0, 1), (3, 1, 4, 6, 0, 5), (6, 2, 3, 5, 2, 2), (3, 5, 0, 7, 3, 5), (1, 2, 4, 2, 6, 4), (6, 4, 4, 7, 6, 2), (3, 1, 2, 2, 0, 4), (1, 0, 0, 6, 2, 5), (1, 6, 3, 7, 7, 5), (0, 6, 4, 4, 0, 0), (4, 4, 2, 7, 1, 0), (5, 5, 1, 7, 1, 5), (1, 5, 2, 2, 2, 3), (4, 6, 4, 0, 5, 2), (0, 4, 0, 5, 3, 0), (3, 2, 4, 1, 3, 1), (1, 6, 1, 1, 3, 3), (4, 0, 1, 4, 6, 4), (0, 5, 1, 7, 2, 3), (1, 0, 3, 0, 7, 0), (4, 4, 1, 5, 0, 5), (5, 0, 4, 0, 2, 0), (2, 0, 0, 2, 7, 5), (5, 3, 3, 5, 7, 4), (2, 0, 1, 4, 3, 4), (2, 6, 1, 7, 7, 4), (6, 0, 1, 5, 5, 1), (2, 4, 4, 1, 7, 3), (6, 2, 2, 3, 2, 0), (6, 6, 1, 2, 3, 4), (1, 0, 1, 4, 0, 5), (1, 4, 1, 1, 6, 3), (2, 6, 4, 3, 1, 4), (6, 4, 2, 2, 1, 4)]
#1agents_pos = [(1, 4, 0, 1, 1, 3), (3, 2, 2, 1, 3, 2), (3, 3, 1, 3, 0, 2), (2, 1, 4, 5, 3, 5), (6, 4, 3, 3, 4, 4), (6, 5, 0, 4, 6, 5), (3, 0, 4, 0, 2, 4), (0, 2, 0, 6, 2, 4), (3, 3, 0, 4, 4, 4), (5, 4, 4, 0, 6, 2)]
#1agents_pos = [(3, 5, 2, 7, 7, 4), (0, 0, 4, 2, 4, 1), (6, 5, 4, 3, 1, 4), (3, 4, 3, 3, 2, 1), (6, 3, 4, 3, 2, 3), (3, 1, 2, 2, 1, 4), (4, 3, 3, 4, 4, 2), (1, 5, 4, 6, 0, 4), (4, 6, 2, 4, 5, 4), (1, 6, 3, 6, 4, 0), (4, 1, 0, 0, 5, 2), (1, 6, 0, 7, 1, 4), (0, 4, 1, 0, 5, 3), (2, 1, 3, 7, 6, 4), (5, 0, 3, 4, 4, 0), (6, 6, 1, 7, 0, 4), (1, 4, 1, 6, 3, 3), (0, 2, 0, 3, 0, 2), (4, 3, 1, 3, 6, 4), (1, 2, 3, 2, 4, 5), (6, 0, 1, 7, 4, 3), (3, 4, 4, 1, 5, 2), (3, 6, 0, 2, 3, 2), (4, 5, 1, 7, 5, 4), (4, 4, 2, 4, 3, 1), (1, 1, 2, 1, 4, 4), (4, 2, 4, 6, 1, 5), (3, 3, 3, 0, 2, 1), (4, 4, 0, 0, 1, 1), (1, 4, 3, 2, 2, 4), (2, 4, 2, 3, 4, 2), (6, 4, 3, 7, 3, 0), (0, 0, 0, 4, 1, 5), (1, 5, 2, 2, 2, 1), (4, 4, 3, 1, 6, 4), (3, 0, 0, 5, 3, 2), (6, 6, 0, 3, 7, 3), (6, 5, 3, 0, 2, 0), (2, 3, 1, 0, 1, 0), (5, 2, 3, 0, 6, 2), (5, 3, 1, 6, 3, 0), (4, 6, 4, 4, 7, 5), (0, 4, 2, 7, 0, 5), (6, 5, 1, 7, 4, 2), (3, 1, 0, 4, 6, 4), (5, 2, 2, 7, 7, 0), (5, 2, 1, 7, 7, 2), (0, 0, 2, 6, 1, 0), (6, 1, 0, 3, 5, 2), (6, 2, 0, 0, 4, 3)]
#1agents_pos = [(6, 5, 2, 4, 6, 5), (6, 1, 4, 7, 5, 2), (0, 0, 2, 0, 5, 3), (2, 3, 0, 4, 5, 2), (3, 4, 4, 7, 4, 1), (2, 0, 0, 5, 1, 3), (2, 0, 2, 5, 2, 3), (0, 4, 0, 2, 3, 4), (5, 2, 3, 6, 7, 4), (3, 0, 3, 1, 4, 0), (3, 6, 0, 3, 6, 2), (3, 2, 0, 4, 6, 0), (5, 4, 4, 1, 2, 2), (1, 2, 0, 3, 4, 3), (0, 6, 2, 3, 1, 3), (5, 1, 2, 2, 5, 4), (5, 5, 1, 3, 3, 0), (5, 1, 3, 6, 3, 2), (1, 6, 4, 0, 7, 1), (2, 5, 2, 2, 2, 1), (3, 6, 1, 5, 2, 5), (2, 6, 0, 3, 5, 3), (5, 6, 1, 0, 3, 3), (5, 6, 2, 1, 2, 0), (5, 4, 0, 6, 2, 5), (0, 2, 4, 4, 5, 1), (1, 1, 3, 4, 4, 5), (3, 6, 3, 0, 2, 0), (2, 0, 1, 3, 5, 2), (0, 3, 1, 7, 5, 4), (6, 6, 2, 1, 3, 2), (1, 4, 0, 5, 0, 3), (4, 6, 1, 5, 5, 1), (2, 2, 0, 6, 3, 4), (2, 2, 1, 3, 1, 0), (4, 1, 4, 1, 2, 5), (2, 4, 1, 0, 1, 3), (4, 0, 1, 4, 5, 5), (6, 2, 2, 2, 3, 5), (1, 5, 4, 0, 2, 1), (6, 2, 1, 3, 5, 1), (0, 0, 1, 4, 4, 0), (0, 4, 3, 0, 2, 3), (5, 0, 4, 5, 5, 5), (0, 1, 4, 3, 3, 4), (2, 5, 1, 4, 3, 5), (1, 5, 1, 6, 6, 0), (1, 4, 4, 5, 7, 2), (6, 4, 3, 5, 3, 2), (6, 0, 0, 2, 6, 3)]
#1agents_pos = [(5, 6, 3, 6, 5, 4), (1, 3, 1, 4, 0, 3), (0, 2, 0, 7, 4, 1), (1, 2, 2, 4, 6, 0), (3, 3, 4, 2, 5, 0), (3, 2, 1, 7, 4, 2), (5, 0, 1, 1, 2, 4), (3, 6, 2, 1, 1, 4), (0, 0, 1, 1, 5, 0), (5, 2, 3, 0, 2, 5), (4, 3, 1, 0, 7, 4), (5, 2, 2, 7, 4, 5), (5, 2, 1, 6, 6, 0), (2, 0, 4, 5, 7, 4), (0, 1, 0, 1, 1, 2), (2, 4, 0, 6, 3, 2), (4, 4, 4, 6, 4, 0), (4, 0, 1, 6, 7, 4), (1, 0, 4, 3, 3, 2), (1, 6, 4, 1, 6, 2), (1, 4, 0, 3, 3, 0), (1, 0, 1, 0, 6, 0), (0, 4, 3, 5, 7, 0), (2, 4, 3, 1, 7, 5), (3, 6, 0, 6, 1, 3), (6, 5, 0, 4, 3, 3), (5, 2, 0, 1, 1, 3), (0, 5, 3, 2, 7, 2), (3, 2, 4, 5, 3, 1), (6, 0, 0, 4, 3, 5), (1, 3, 4, 0, 7, 0), (2, 4, 1, 4, 7, 1), (5, 4, 3, 6, 4, 5), (5, 0, 3, 4, 1, 0), (3, 5, 4, 4, 5, 3), (1, 4, 1, 3, 4, 1), (6, 6, 3, 7, 2, 5), (0, 6, 1, 4, 3, 0), (1, 2, 1, 1, 4, 4), (2, 3, 1, 1, 4, 0), (3, 0, 2, 3, 4, 4), (2, 3, 3, 5, 6, 5), (2, 3, 2, 2, 6, 4), (3, 3, 0, 1, 5, 2), (4, 6, 3, 7, 2, 4), (0, 5, 0, 2, 3, 4), (6, 5, 3, 2, 5, 2), (2, 1, 2, 5, 4, 3), (6, 1, 0, 7, 6, 3), (5, 0, 0, 6, 0, 5)]
#1agents_pos =  [(4, 4, 0, 0, 6, 3), (2, 1, 2, 1, 4, 5), (1, 1, 0, 0, 5, 2), (1, 1, 2, 5, 6, 4), (3, 4, 0, 1, 3, 2), (3, 4, 4, 5, 2, 4), (3, 5, 3, 4, 4, 5), (2, 5, 4, 3, 3, 5), (6, 4, 2, 7, 7, 0), (1, 5, 0, 4, 0, 1), (2, 6, 3, 2, 0, 0), (4, 6, 3, 0, 2, 4), (2, 5, 1, 4, 5, 0), (2, 2, 3, 5, 1, 2), (4, 3, 1, 6, 4, 3), (4, 3, 2, 2, 7, 2), (5, 6, 4, 2, 5, 0), (6, 5, 1, 3, 3, 4), (0, 1, 0, 3, 7, 0), (5, 3, 1, 4, 1, 4), (5, 6, 1, 2, 3, 2), (4, 5, 2, 5, 7, 0), (0, 6, 1, 7, 2, 0), (4, 0, 1, 3, 6, 5), (6, 4, 4, 0, 5, 4), (3, 1, 0, 0, 3, 0), (5, 4, 0, 1, 5, 1), (6, 4, 3, 5, 0, 5), (1, 0, 1, 0, 3, 3), (1, 4, 4, 7, 3, 4), (0, 3, 2, 1, 7, 2), (3, 3, 4, 0, 0, 3), (6, 5, 0, 4, 5, 5), (5, 3, 4, 1, 3, 3), (0, 0, 1, 2, 7, 1), (1, 3, 2, 7, 2, 2), (4, 2, 0, 6, 0, 3), (5, 1, 2, 7, 1, 2), (6, 5, 3, 1, 6, 0), (2, 0, 3, 3, 0, 1), (5, 0, 4, 7, 3, 2), (4, 4, 4, 2, 6, 0), (1, 6, 2, 3, 7, 3), (1, 3, 1, 5, 5, 4), (3, 3, 3, 1, 2, 3), (5, 2, 4, 2, 5, 4), (6, 2, 1, 4, 7, 5), (4, 1, 3, 5, 3, 4), (3, 6, 1, 1, 0, 5), (5, 4, 2, 2, 5, 2)]
#1agents_pos = [(2, 4, 4, 0, 1, 5), (5, 5, 2, 2, 3, 2), (5, 2, 0, 6, 6, 2), (0, 0, 0, 5, 6, 5), (5, 1, 3, 1, 4, 1), (0, 1, 2, 5, 3, 4), (0, 4, 3, 6, 3, 4), (1, 3, 4, 2, 6, 1), (2, 3, 4, 0, 2, 5), (1, 2, 2, 3, 3, 3), (3, 5, 1, 5, 2, 2), (3, 4, 1, 3, 2, 0), (4, 4, 2, 2, 0, 2), (1, 6, 4, 5, 2, 1), (6, 1, 4, 2, 5, 0), (0, 2, 1, 2, 3, 1), (2, 1, 4, 3, 0, 0), (4, 1, 2, 1, 1, 5), (1, 3, 0, 2, 3, 3), (4, 5, 0, 7, 6, 1), (4, 3, 3, 0, 1, 4), (2, 2, 3, 4, 0, 1), (6, 3, 2, 3, 4, 1), (5, 3, 1, 6, 1, 4), (1, 1, 1, 4, 4, 5), (1, 1, 2, 0, 0, 4), (2, 5, 1, 6, 7, 1), (5, 1, 0, 4, 1, 5), (0, 3, 0, 4, 4, 2), (1, 3, 1, 6, 5, 1), (2, 1, 0, 7, 3, 0), (2, 2, 2, 2, 7, 0), (4, 2, 3, 7, 5, 2), (3, 0, 3, 7, 6, 2), (2, 3, 2, 4, 3, 5), (0, 6, 4, 6, 5, 0), (6, 5, 0, 3, 1, 3), (6, 6, 4, 2, 4, 0), (6, 3, 0, 1, 2, 3), (4, 4, 3, 6, 3, 5), (6, 0, 2, 2, 7, 2), (4, 4, 0, 4, 5, 5), (3, 6, 2, 6, 4, 1), (2, 3, 3, 6, 0, 4), (3, 5, 4, 1, 4, 0), (2, 5, 0, 3, 4, 0), (1, 3, 2, 3, 3, 1), (1, 0, 1, 6, 1, 3), (0, 6, 0, 5, 3, 1), (4, 3, 2, 5, 7, 4)]
#1agents_pos = [(3, 0, 1, 2, 4, 0), (3, 0, 0, 4, 4, 2), (1, 2, 0, 3, 1, 0), (1, 1, 0, 4, 1, 0), (3, 3, 0, 4, 2, 1), (2, 3, 1, 2, 0, 0), (1, 3, 0, 0, 4, 2), (1, 2, 1, 1, 2, 1), (0, 0, 0, 1, 1, 2), (2, 2, 1, 0, 1, 2)]
#agents_pos = [(3,3,0,5,3,0), (4,3,0,2,3,0)]
#1agents_pos = [(2, 0, 0, 3, 1, 0), (2, 0, 1, 1, 2, 2), (2, 2, 1, 0, 3, 0), (0, 2, 0, 3, 0, 2), (0, 0, 0, 2, 3, 0), (0, 1, 0, 3, 2, 0), (0, 2, 1, 3, 3, 2), (1, 0, 1, 0, 0, 0), (1, 1, 1, 1, 1, 0), (2, 1, 1, 0, 2, 0)]
#1agents_pos = [(2, 1, 0, 1, 1, 0), (1, 1, 0, 1, 0, 0), (0, 1, 0, 2, 1, 0), (1, 0, 1, 0, 3, 1), (0, 0, 0, 3, 1, 1), (2, 2, 0, 3, 3, 0), (2, 2, 1, 0, 0, 2), (2, 0, 0, 1, 2, 0), (0, 2, 1, 3, 0, 0), (2, 0, 1, 2, 3, 2)]
#print("the agents:\n", agents_pos)
# ---------------------------------- add the agents to world----------------------------------------

#world.add_agents(agents_pos)
#agents = world.get_agents()

# ----------------------------------find paths with conflicts------------------------------------

#paths_with_conflicts = search.path_finding_with_conflicts(agents)

# ----------------------------------find paths without conflicts----------------------------------

#paths, agents_without_solution = search.path_finding(agents, world)

# ---------------------------------printing the results--------------------------------------------

"""if not test_function.check_conflicts(agents, paths):
    print("the pathsssssssssssss:\n", paths)
    print("yessssssssssssssssssssssssssssssss")
else:
    print("the pathsssssssssssss:\n", paths)
    print("their are conflictssssssssssssssssss")"""


test_function.main(world)
