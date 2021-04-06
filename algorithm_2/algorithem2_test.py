import algorithm_2.find_path
import math
def run_one_case(num_floors, num_rows, num_cols, agent_radius, security_distance, agents_pos):

    graph_manager = algorithm_2.GraphManager((num_rows, num_cols, num_floors))
    path_manager = algorithm_2.PathManager(graph_manager)
    agent_manager = algorithm_2.AgentManager(path_manager)

    agent_manager.create_agents(agents_pos)
    path_list = agent_manager.get_agents_path_list()
    return path_list

def convert_paths(paths_list):
    paths = {}

    for agent_id, path in enumerate(paths_list):
        paths[agent_id + 1] = []
        for step in path:
            paths[agent_id + 1].append((step[1], step[2], step[3]))
    return paths

