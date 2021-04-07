from matplotlib import pylab

import algorithm_1.algoritm1_test as test_1
import algorithm_2.algorithem2_test as test_2
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
    path_1, broblem_drones = test_1.run_one_case(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS, SECURITY_DISTANCE, agents_pos.copy())
    run_time_1 = time.time() - start_time

    start_time = time.time()
    path_2 = test_2.run_one_case(num_floors, num_rows, num_cols, agents_pos.copy())
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
    pylab.clf()

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

def compare_2_algorithm(paths_1, broblem_cases, paths_2):

    if paths_1 and not broblem_cases:             # in case algorithm 1 return paths
        if paths_2:                               # in case algorithm 2 return paths
            # compare with algorithm 1 test function
            paths_2_dict = test_2.convert_paths(paths_2)
            #if test_1.check_conflicts()

            # compare with algorithm 2 test function

        else:
            print("algorithm 2 did not find path for this case")
    else:
        print("algorithm 1 did not find path for this case")


def main():
    run_time_1 = run_time_2 = 0
    success_1 = success_2 = 0
    max_path_len_1 = max_path_len_2 = 0
    run_time_y1 = []
    run_time_y2 = []
    max_path_len_1_list = []
    max_path_len_2_list = []
    x = [ i for i in range(50, 101, 10)]
    for num_of_agents in x:
        run_time_1 = run_time_2 = 0
        success_1 = success_2 = 0
        max_path_len_1 = max_path_len_2 = 0

        for i in range(NUM_CASES):
            agents_pos = test_1.random_inputs(num_floors, num_cols, num_rows, num_of_agents)
            # find the paths for the agents pos, from each algorithm
            path_1, broblem_drones = test_1.run_one_case(HEIGHT, WIDTH, LENGTH, AGENT_RADIUS,SECURITY_DISTANCE, agents_pos.copy())
            path_2 = test_2.run_one_case(num_floors, num_rows, num_cols, agents_pos.copy())

            if path_1 and not broblem_drones:
                success_1 += 1
                max_path_len_1 += test_1.get_max_pathlen(path_1)

            if test_2.check_path(path_2):
                success_2 += 1
                path_2_dict = test_2.convert_paths(path_2)
                #print(path_2_dict)
                max_path_len_2 += test_1.get_max_pathlen(path_2_dict)
            else:
                print("in this agent pos their are problem in algorithm 2\n", agents_pos)

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
    print(max_path_len_1_list, max_path_len_2_list)
    draw_graph_run_time(x, run_time_y1, x, run_time_y2)
    draw_graph_pathlen(x, max_path_len_1_list, x, max_path_len_2_list)

if __name__ == '__main__':
    main()

