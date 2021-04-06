import math
from random import randrange, randint
import algorithm_1.search as search
import time
from algorithm_1.world import *
import json
start_time = time.time()


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

def path_length_ratio(agents, paths, world):
    path_with_conflict = search.path_finding_with_conflicts(agents, world)

    length_paths_with_conflict = []
    length_paths = []

    # calculate the length of the paths without conflicts
    for agent in paths:
        length = 0
        for pos_index in range(1, len(paths[agent])):
            x1, y1, z1 = paths[agent][pos_index]
            x2, y2, z2 = paths[agent][pos_index - 1]
            length += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2)* 1.0) # Linear distance
        length_paths.append(length)

    # calculate the length of the paths with conflicts
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
                    print("curent step: ", current_steps, "time: ", time, "agent ", agent)
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

def run_random_cases(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path=0):

    count = 0
    count_conflicts = 0
    counter_faild = 0
    list_of_faild = []

    for i in range(num_cases):
        world = World(height, width, length, agent_radius, security_distance)
        agents_pos = random_inputs(world.num_floors, world.num_rows, world.num_cols, num_agents)
        world.add_agents(agents_pos)                # add the agents to world
        agents = world.get_agents()
        paths, agents_without_solution = search.path_finding(agents, world)  # get the paths for the agents
        print("--- %s seconds ---" % (time.time() - start_time))
        if paths and not agents_without_solution:
            if not check_conflicts(agents, paths):
                count += 1
                #path_len_ratio = path_length_ratio(agents, world)
                #print("the agents pos:\n", agents_pos, "\nthe paths: \n", paths, "\nSucssiedddddddd\n", "path_len_ratio\n", path_len_ratio)
            else:
                count_conflicts += 1
                #print("their is a conflictssssssssssssssss\n")
        else:
            counter_faild += 1
            list_of_faild.append(i)
            print("the algorithem didnt find paths for this agents_pos\n", agents_pos, "the problematic agents is:\n", agents_without_solution)

        print(paths)
        print("count of sucsses is: ", count, "count of conflictsss: ", count_conflicts, "count of faild: ", counter_faild)
        print("the number example of faild is : ", list_of_faild)

        if save_path:
            with open('../jason_paths/paths.txt', 'w') as json_file:
                json.dump(paths, json_file)

def run_specific_case(height, width, length, agent_radius, security_distance, agents_pos, save_path=0):

    world = World(height, width, length, agent_radius, security_distance)
    world.add_agents(agents_pos)                                         # add the agents to world
    agents = world.get_agents()
    paths, agents_without_solution = search.path_finding(agents, world)  # get the paths for the agents
    print("--- %s seconds ---" % (time.time() - start_time))
    if paths and not agents_without_solution:
        if not check_conflicts(agents, paths):
            print("this case succeeded")
            # path_len_ratio = path_length_ratio(agents, world)
            # print("the agents pos:\n", agents_pos, "\nthe paths: \n", paths, "\nSucssiedddddddd\n", "path_len_ratio\n", path_len_ratio)
        else:
            print("this case return with conflicts")
            # print("their is a conflictssssssssssssssss\n")
    else:
        print("the algorithem didnt find paths for this agents_pos\n")

    print(paths)

    if save_path:                                   # in case we want to save this paths to jason file
        with open('../jason_paths/paths.txt', 'w') as json_file:
            json.dump(paths, json_file)
    print(paths)


if __name__ == '__main__':
    run_random_cases(100, 100, 100, 0.25, 4, 1, 100)