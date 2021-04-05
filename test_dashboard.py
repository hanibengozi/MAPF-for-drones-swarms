import algorithm_1.test_function


def run_algorithm_1(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path=0):
    return algorithm_1.test_function.run_random_cases(height, width, length, agent_radius, security_distance, num_cases, num_agents, save_path)

def run_algorithm_1_with_specific_example(height, width, length, agent_radius, security_distance, agents_pos, save_path=0):
    return algorithm_1.test_function.run_specific_case(height, width, length, agent_radius, security_distance, agents_pos, save_path)