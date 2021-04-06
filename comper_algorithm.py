import algorithm_1.algoritm1_test
import algorithm_2.algorithem2_test
import time
import math

HEIGHT = 100
WIDTH = 100
LENGTH = 100
AGENT_RADIUS = 0.25
SECURITY_DISTANCE = 4
num_floors = math.ceil(HEIGHT / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
num_rows = math.ceil(LENGTH / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
num_cols = math.ceil(WIDTH / (AGENT_RADIUS * 2 + SECURITY_DISTANCE))
ALGORITHM_1 = 1
ALGORITHM_2 = 2

def compare_run_time(agents_pos):

    start_time = time.time()
    paths_1, problematic_agents = algorithm_1.algoritm1_test.run_one_case(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE, agents_pos)
    run_time_1 = time.time() - start_time

    start_time = time.time()
    paths_2 = algorithm_2.algorithem2_test.run_one_case(num_floors, num_rows, num_cols, AGENT_RADIUS, SECURITY_DISTANCE, agents_pos)
    run_time_2 = time.time() - start_time

    return run_time_1, run_time_2


def main(num_of_cases, num_of_agents):
    run_time_1 = 0
    run_time_2 = 0
    for i in range(num_of_cases):
        agents_pos = algorithm_1.algoritm1_test.random_inputs(num_floors, num_cols, num_rows, num_of_agents)

        run_time_1 += compare_run_time(agents_pos)[0]
        run_time_2 += compare_run_time(agents_pos)[1]

    if algorithm_1 < algorithm_2:
        algorithm = ALGORITHM_1
    elif algorithm_2 < algorithm_1:
        algorithm = ALGORITHM_2
    else:
        algorithm = ALGORITHM_1, ALGORITHM_2

    print("the algorithm with the best run time is: ",algorithm, run_time_1, run_time_2)

if __name__ == '__main__':
    main(1,50)

