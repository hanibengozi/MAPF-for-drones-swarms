import algorithm_1.algoritm1_test as test_1
import algorithm_2.algorithem2_test as test_2
import math

HEIGHT = 100
WIDTH = 100
LENGTH = 100
AGENT_RADIUS = 0.25
SECURITY_DISTANCE = 4
num_floors = math.ceil(HEIGHT / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
num_rows = math.ceil(LENGTH / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
num_cols = math.ceil(WIDTH / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
ALGORITHM_1 = "algorithm 1"
ALGORITHM_2 = "algorithm 2"

# this method run num cases, num agents and get the result from algorithm 1
def run_algorithm_1(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path=0):
    return test_1.run_random_cases(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path)

# this method run num cases, num agents and get the result from algorithm 2
def run_algorithm_2(num_floors, num_rows, num_cols, num_cases, num_agents):
    return test_2.run_random_cases(num_floors, num_rows, num_cols, num_cases, num_agents)

def run_algorithm_1_with_specific_example(height, width, length, agent_radius, security_distance, agents_pos, save_path=0):
    return test_1.run_specific_case(height, width, length, agent_radius, security_distance, agents_pos, save_path)

def run_algorithm_2_with_specific_example(num_floors, num_rows, num_cols, agents_pos):
    paths = test_2.run_one_case(num_floors, num_rows, num_cols, agents_pos)
    if test_2.check_path(paths):
        return paths
    return None

def show_num_cases(num_cases, num_agents, algorithm):

    # in case we choose to run algorithm 1
    if algorithm == ALGORITHM_1:
        return run_algorithm_1(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE, num_cases, num_agents)

    if algorithm == ALGORITHM_2:
        return run_algorithm_2(num_floors, num_cols, num_rows, num_cases, num_agents)

if __name__ == '__main__':
    show_num_cases(1, 50, "algorithm 1")