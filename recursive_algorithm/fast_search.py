from step_unit import *
import queue
# the method return true when all the agents arrived to goal
def got_to_goal(agents_list, paths, max_len_path_with_collision):
    if len(paths[1]) > max_len_path_with_collision * 3:
        restoring_paths(paths)
        return True

    for agent in agents_list:
        if agent.current_step != agent.goal_pos:
            return False

    return True

def path_finding(agents, world, max_len_path_with_collision):
    # ----------------------------initialization------------------------------------------------
    paths = {}                    # a dictionary of the paths, for each agent the path
    step_unit = StepUnit(0)       # Initialize the first time step
    counter = 0

    for agent in agents:                                     # initialize the list of current_steps with start pos
        step_unit.add_current_step_to_list(agent.start_pos)  # add start pos, for each agent
        paths[agent.id] = [agent.start_pos]                  # initialize the value of paths dict to the start pos

    # -----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while not got_to_goal(agents, paths, max_len_path_with_collision):  # loop until all the agents got to goal

        step_unit.set_prev_steps(step_unit.current_steps_list)  # update the prev steps list, to the last current steps list
        counter = 0
        for agent in agents:             # iterate on agents, for each agent find next step.
            new_step = get_next_step(agent, step_unit, world, 0, 5)# get next step

            if new_step:
                step_unit.add_step_dict_occupied(new_step, agent)  # update the current step, for check collision
                step_unit.update_current_step(new_step, agent.id)  # update the current steps
                agent.current_step = new_step
                paths[agent.id].append(new_step)
                if new_step == agent.goal_pos:
                    print("agent: ", agent.id, "arrive to goal!")
                    agent.time_got_to_goal = step_unit.time
                    counter += 1

            else:                                                   # in case, their no solution
                print("their are no solution for this agents")
                return paths
        print("the number of agents that didnt arrived to goal is: ", len(agents) - counter)
        current_steps = step_unit.current_steps_list
        step_unit = StepUnit(step_unit.time + 1)                        # Advances the steps in one
        step_unit.set_current_steps_list(current_steps)      # update the current steps for the new tim
    return paths

def get_next_step(agent, step_unit, world, counter, counterMax, forbiden_step = None):

    steps = get_possible_steps(agent, step_unit, world)

    for step, coordinate in steps.queue:                                # pass on steps, and search for free step
        if forbiden_step and forbiden_step == step:         # for collides agent dont choose the step that make collision.
            continue

        if step not in step_unit.dict_occupied:

            if agent.update_change_direction:      # for provide next time to choose step, that make infinity loop.
                agent.change_direction.append((step_unit.time + 1, coordinate))

            return step

    print("---------------------------------------------------------------------------------------------------------")
    if counter > counterMax:            # In order not to go too far back in recursion
        return None

    for step, coordinate in steps.queue:           # iterate the steps, and for each step send the collides agent to get_next step
        agent_collides = step_unit.dict_occupied[step]    # get the collides agent
        if get_next_step(agent, step_unit, world, counter + 1, counterMax, step):
            print("this agent: ", agent.id, " find next step after moving: ", agent_collides.id," in time: ", step_unit.time, " the next step is: ", step)
            return step
        else:
            print("this agent: ", agent.id, " didnt find next step after moving: ", agent_collides.id," in time: ", step_unit.time, " the trying step is: ", step)
            continue

    return None
#the method get step, and return the next free step to goal
def get_possible_steps(agent, step_unit, world):

    possible_steps = queue.Queue()
    agent.update_change_direction = False
    # add to queue all the free steps that are in the right direction.
    for coordinate in range(2,-1,-1):
        if agent.current_step[coordinate] != agent.goal_pos[coordinate]:          # check if the coordinate not in the right place already.
            direction = 1 if agent.current_step[coordinate] < agent.goal_pos[coordinate] else -1  # Sets the direction to the goal, up (=1) or down(=-1)
            next_step = list(agent.current_step)
            next_step[coordinate] += direction                               # get the next step
            if check_free_step(tuple(next_step), agent, step_unit):          # if this step free add to queue
                if (step_unit.time, coordinate) in agent.change_direction:
                    continue
                if tuple(next_step) == agent.goal_pos:                       # in case the next step equal to goal, put it in the top of the queue.
                    possible_steps.queue.appendleft([tuple(next_step), coordinate])        # add to queue the step and deviation
                else:
                    possible_steps.put([tuple(next_step), coordinate])                     # add to queue the step and deviation
            else:
                agent.update_change_direction = True

    # add the rest of the steps to queue
    for coordinate in range(2,-1,-1):
        direction = 1 if agent.current_step[coordinate] < agent.goal_pos[coordinate] else -1   # Sets the direction to the goal, up (=1) or down(=-1)
        next_step = list(agent.current_step)
        next_step[coordinate] += direction
        if not in_queue(possible_steps, tuple(next_step)):                   # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), agent, step_unit):         # check if this step is free.
                if (step_unit.time, coordinate) in agent.change_direction:
                    continue
                if world.is_valid_pos(tuple(next_step)):                    # check if the step is valid
                    if tuple(next_step) == agent.goal_pos:                  # in case the next step equal to goal, put it in the top of the queue.
                        possible_steps.queue.appendleft([tuple(next_step), coordinate])
                    else:
                        possible_steps.put([tuple(next_step), coordinate])                # append to the queue.
            else:
                agent.update_change_direction = True


        next_step = list(agent.current_step)                                # check for step in the opposite direction
        next_step[coordinate] -= direction
        if not in_queue(possible_steps, tuple(next_step)):                  # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), agent, step_unit):         # check if this step is free.
                if (step_unit.time, coordinate) in agent.change_direction:  # check if this step make infinity loop
                    continue
                if world.is_valid_pos(tuple(next_step)):                    # check if the step is valid
                    if tuple(next_step) == agent.goal_pos:                  # in case the next step equal to goal, put it in the top of the queue.
                        possible_steps.queue.appendleft([tuple(next_step), coordinate])
                    else:
                        possible_steps.put([tuple(next_step), coordinate])           # append to the queue.
            else:
                agent.update_change_direction = True

    if agent.current_step == agent.goal_pos:                           # for agent that already in goal.
        possible_steps.queue.appendleft([agent.current_step, -1])

    return possible_steps

# the method get step, and dict of steps and check that their are no conflict in this step, retuen True in case the step free.
def check_free_step(step, agent, step_unit):

    # In case the step is in dictionaries then we will check that their value is not equal to that agent
    if step in step_unit.prev_steps:
        if step_unit.prev_steps.index(step) != agent.id - 1:      # this step not free
            return False

    return True

# the method get queue and step, and check if the step already in queue
def in_queue(possible_steps, new_step):

    for step, coordinate in possible_steps.queue:
        if step == new_step:
            return True
    return False

"""def restoring_paths(paths):
    max_path_len = 0
    for agent in paths.keys():
        if agent.time_got_to_goal > max_path_len:
            max_path_len = agent.time_got_to_goal"""

    #for agent in paths:
       # paths[agent] = paths[agent][]