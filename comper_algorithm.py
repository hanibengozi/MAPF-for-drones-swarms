import algorithm_1.algoritm1_test
import algorithm_2.algorithem2_test
import matplotlib.pyplot as plt
import numpy as np
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
NUM_CASES = 1



def compare_run_time(agents_pos):

    start_time = time.time()
    path_1, broblem_drones = algorithm_1.algoritm1_test.run_one_case(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE, agents_pos.copy())
    run_time_1 = time.time() - start_time

    start_time = time.time()
    path_2 = algorithm_2.algorithem2_test.run_one_case(num_floors, num_rows, num_cols, agents_pos.copy())
    run_time_2 = time.time() - start_time

    return run_time_1, run_time_2

def draw_graph_run_time(x1, y1, x2, y2):

    # plotting the line 1 points
    plt.plot(x1, y1, label="algorithm 1")


    # plotting the line 2 points
    plt.plot(x2, y2, label="algorithm 2")
    # naming the x axis
    plt.xlabel('x - num of drones')
    # naming the y axis
    plt.ylabel('y - run time')
    # giving a title to my graph
    plt.title('Compare the rum time between the two algorithms:')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.savefig("run_time_graph.png")

def draw_graph_pathlen(x1, y1, x2, y2):

    # plotting the line 1 points
    plt.plot(x1, y1, label="algorithm 1")

    # plotting the line 2 points
    plt.plot(x2, y2, label="algorithm 2")
    # naming the x axis
    plt.xlabel('x - num of drones')
    # naming the y axis
    plt.ylabel('y - max path len')
    # giving a title to my graph
    plt.title('Compare the max path length between the two algorithms:')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.savefig("pathlen_graph.png")


def main():
    run_time_1 = run_time_2 = 0
    success_1 = success_2 = 0
    max_path_len_1 = max_path_len_2 = 0
    run_time_y1 = []
    run_time_y2 = []
    max_path_len_1_list = []
    max_path_len_2_list = []
    x = [ i for i in range(50, 101, 25)]
    for num_of_agents in x:
        run_time_1 = run_time_2 = 0
        success_1 = success_2 = 0

        for i in range(NUM_CASES):
            agents_pos = algorithm_1.algoritm1_test.random_inputs(num_floors, num_cols, num_rows, num_of_agents)
            # find the paths for the agents pos, from each algorithm
            path_1, broblem_drones = algorithm_1.algoritm1_test.run_one_case(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS,SECURITY_DISTANCE, agents_pos.copy())
            path_2 = algorithm_2.algorithem2_test.run_one_case(num_floors, num_rows, num_cols, agents_pos.copy())

            if path_1 and not broblem_drones:
                success_1 += 1
                max_path_len_1 += algorithm_1.algoritm1_test.get_max_pathlen(path_1)

            if algorithm_2.algorithem2_test.check_path(path_2):
                success_2 += 1
                path_2_dict = algorithm_2.algorithem2_test.convert_paths(path_2)
                print(path_2_dict)
                max_path_len_2 += algorithm_1.algoritm1_test.get_max_pathlen(path_2_dict)

            # find time run of each algorithm for this cases
            time_1, time_2 = compare_run_time(agents_pos)
            run_time_1 += time_1
            run_time_2 += time_2


        if success_1 != NUM_CASES:
            print("algorithem 1 dont foundt paths for all caccess")
        if success_2 != NUM_CASES:
            print("algorithem 2 dont foundt paths for all caccess")


        run_time_y1.append(run_time_1)
        run_time_y2.append(run_time_2)
        # find what is the average max path len of each algorithm
        max_path_len_1_list.append(max_path_len_1 / NUM_CASES)
        max_path_len_2_list.append(max_path_len_2 / NUM_CASES)


    # draw graph
    print(x, run_time_y1, run_time_y2)
    draw_graph_run_time(x, run_time_y1, x, run_time_y2)
    draw_graph_pathlen(x, max_path_len_1_list, x, max_path_len_2_list)

if __name__ == '__main__':
    main()

