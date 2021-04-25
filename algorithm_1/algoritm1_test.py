import math
from random import randrange, randint
import algorithm_1.search as search
import time
from algorithm_1.world import *
import json
start_time = time.time()
from global_variable import *


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

# this method get paths and return true in case all the agents arrived to goal
def all_arrive_to_goal(paths, agents):
    for agent in agents:
        if paths[agent.id][-1] != agent.goal_pos:
            return False
    return True

def convert_path_to_list(paths):

    sorted(paths)


# this method get number od casses and agents and size of world, and run the algorithm number of cases for random position
def run_random_cases(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path=0):

    count = 0
    count_conflicts = 0
    counter_faild = 0
    list_of_faild = []
    result = ""
    run_time = 0

    for i in range(num_cases):

        world = World(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE)
        agents_pos = random_inputs(world.num_floors, world.num_rows, world.num_cols, num_agents)
        world.add_agents(agents_pos)                # add the agents to world
        agents = world.get_agents()
        paths, agents_without_solution = search.path_finding(agents, world)  # get the paths for the agents
        run_time = time.time() - start_time

        if paths and not agents_without_solution and all_arrive_to_goal(paths, agents):
            if not check_conflicts(agents, paths):
                count += 1
            else:
                count_conflicts += 1
        else:
            counter_faild += 1
            list_of_faild.append(i)

    # save results for showing on screen
    result += "For running " + str(num_cases) + " cases\n"
    result += "The number of cases the algorithm returned paths without collisions: " + str(count) + "\n"
    result += "The number of cases the algorithm returned trajectories with collisions: " + str(count_conflicts) + "\n"
    result += "The number of cases that the algorithm did not find paths: " + str(counter_faild) + "\n"
    result += "The time of run is: " + str(run_time) + " " + str(run_time / num_cases) + "\n"

    #------------------printing-----------------------------------------
    #print(paths)
    #print(result)

    # in case we want to save this paths in jason file
    if save_path:
        with open('../jason_paths/paths.txt', 'w') as json_file:
            json.dump(paths, json_file)

    return result

def run_specific_case(height, width, length, agent_radius, security_distance, agents_pos, save_path=0):

    result = ""
    world = World(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE)
    world.add_agents(agents_pos)                                         # add the agents to world
    agents = world.get_agents()
    paths, agents_without_solution = search.path_finding(agents, world)  # get the paths for the agents
    result += "this run time of this case is: " + str(time.time() - start_time)
    print("--- %s seconds ---" % (time.time() - start_time))
    if paths and not agents_without_solution:
        if not all_arrive_to_goal(paths, agents):
            result += "failed! not all agent arrive to goal" + "\n"
            print("failed! not all agent arrive to goal")
        if not check_conflicts(agents, paths):
            result += "This case success!" + "\n"
            print("this case succeeded")
        else:
            result += "This case return with conflicts!" + "\n"
            print("this case return with conflicts")
    else:
        result += "The algorithm didnt find paths for this agents_pos!" + "\n"
        print("the algorithem didnt find paths for this agents_pos\n")

    result += "The paths:\n" + str(paths)
    print(paths)

    # in case we want to save this paths to jason file
    if save_path:
        with open('../jason_paths/paths.txt', 'w') as json_file:
            json.dump(paths, json_file)

    return paths

def run_one_case(height, width, length, agent_radius, security_distance, agents_pos, save_path=0):

    world = World(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE)
    world.add_agents(agents_pos)                                          # add the agents to world
    agents = world.get_agents()
    paths, agents_without_solution = search.path_finding(agents, world)   # get the paths for the agents
    return paths, agents_without_solution


if __name__ == '__main__':
    run_random_cases(100, 100, 100, 0.25, 4, 1000, 100)

    #agents_pos = [(9, 9, 13, 8, 9, 15), (10, 10, 18, 8, 9, 18), (10, 10, 19, 8, 9, 20), (12, 12, 19, 11, 11, 21), (13, 12, 19, 12, 11, 20), (14, 13, 20, 15, 13, 20), (7, 8, 17, 5, 7, 16), (9, 9, 20, 7, 8, 20), (10, 10, 20, 8, 9, 21), (11, 11, 20, 10, 10, 19), (12, 11, 20, 10, 10, 21), (13, 12, 20, 14, 13, 20), (14, 13, 18, 15, 14, 18), (8, 9, 14, 5, 7, 14), (7, 8, 20, 5, 7, 19), (7, 8, 18, 5, 7, 20), (12, 11, 18, 12, 11, 19), (11, 11, 16, 13, 12, 16), (11, 11, 14, 12, 11, 16), (14, 13, 16, 15, 14, 16), (10, 10, 13, 10, 10, 14), (9, 10, 12, 7, 8, 12), (11, 11, 11, 11, 11, 14), (11, 11, 14, 10, 10, 15), (11, 11, 13, 12, 11, 15), (14, 13, 17, 15, 14, 17), (13, 13, 14, 15, 14, 15), (8, 8, 16, 5, 7, 15), (9, 9, 19, 8, 9, 17), (9, 10, 18, 8, 9, 16), (10, 10, 12, 8, 9, 14), (11, 11, 18, 12, 11, 18), (12, 12, 18, 13, 12, 18), (13, 12, 13, 15, 13, 14), (10, 10, 17, 10, 10, 17), (11, 11, 16, 11, 11, 17), (11, 11, 15, 12, 11, 17), (11, 11, 12, 14, 13, 14), (12, 11, 17, 13, 12, 17), (12, 12, 12, 13, 12, 15)]
    #print(run_specific_case(100,100,100,0.25,4,agents_pos))

    # 24: [(12, 11, 14), (12, 11, 15), (12, 10, 15), (11, 10, 15), (10, 10, 15), (10, 10, 15), (10, 10, 15), (10, 10, 15),
    #      (10, 10, 15), (10, 10, 15)]