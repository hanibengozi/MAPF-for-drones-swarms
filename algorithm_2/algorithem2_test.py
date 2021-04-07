import algorithm_2.find_path as find_path
import math
import time
from algorithm_2.math_graph import Point3D
start_time = time.time()

# this method get number od casses and agents and size of world, and run the algorithm number of cases for random position
def run_random_cases(num_floors, num_rows, num_cols, num_cases, num_agents):
    count = 0
    count_conflicts = 0
    counter_faild = 0
    result = ""
    run_time = 0

    for i in range(num_cases):
        graph_manager = find_path.GraphManager((num_rows, num_cols, num_floors))
        path_manager = find_path.PathManager(graph_manager)
        agent_manager = find_path.AgentManager(path_manager)
        agents_pos = agent_manager.get_random_agents(num_agents)
        

        agent_manager.create_agents(agents_pos)
        path_list = agent_manager.get_agents_path_list()
        run_time = time.time() - start_time

        if path_list and check_path(path_list):
            if not find_path.TestManager.check_collision(find_path.TestManager,path_list, path_manager.points_manager):
                count += 1
            else:
                count_conflicts += 1
        else:
            counter_faild += 1

    # save results for showing on screen
    result += "For running " + str(num_cases) + " cases\n"
    result += "The number of cases the algorithm returned paths without collisions: " + str(count) + "\n"
    result += "The number of cases the algorithm returned trajectories with collisions: " + str(count_conflicts) + "\n"
    result += "The number of cases that the algorithm did not find paths: " + str(counter_faild) + "\n"
    result += "The time of run is: " + str(run_time) + "  " + str(run_time / num_cases)

    # ------------------printing-----------------------------------------
    #print(result)
    #print(path_list)

    return result

def run_one_case(num_floors, num_rows, num_cols, agents_pos):

    agents_pos = convert_agents_pos(agents_pos)
    graph_manager = find_path.GraphManager((num_rows, num_cols, num_floors))
    path_manager = find_path.PathManager(graph_manager)
    agent_manager = find_path.AgentManager(path_manager)

    agent_manager.create_agents(agents_pos)
    path_list = agent_manager.get_agents_path_list()
    return path_list

def convert_paths(paths_list):
    paths = {}

    if not paths_list:
        return

    for agent_id, path in enumerate(paths_list):
        paths[agent_id + 1] = []
        for step in path:
            paths[agent_id + 1].append((step[1], step[2], step[3]))
    return paths


# convert the agents random position to fit for algorithm 2
def convert_agents_pos(agents_pos):
    random_points = []
    for agent_pos in agents_pos:
        start_pos = Point3D(agent_pos[0], agent_pos[1], agent_pos[2])
        goal_pos = Point3D(agent_pos[2], agent_pos[3], agent_pos[4])
        random_points.append([start_pos, goal_pos])
    return random_points

def check_path(paths):
    for path in paths:
        if not path:
            return False
    return True