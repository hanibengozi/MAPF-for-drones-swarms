import queue
from step_unit import *
from pip._vendor.msgpack.fallback import xrange

# this method get agent and the world, and return path for each agent without collision
"""def find_path(agents, world):

    # ----------------------------initialization------------------------------------------------
    agents_list = agents.copy()
    current_steps = []
    prev_steps = []
    paths = {}
    conflict_steps = {}
    i = 0

    for agent in agents_list:                           # initialize the list of current_steps with start pos
        current_steps.append(world.starts_pos[agent])   # add start pos, for each agent
        paths[agent] = []                               # initialize the value of paths dict to empty list

    #-----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while agents_list:

        conflict_steps[i] = []
        prev_steps = current_steps.copy()                             # update the prev steps list, to the last current steps list

        for agent_index in xrange(len(agents_list) - 1, -1, -1):      # iterate over the list of agent left.
            agent = agents_list[agent_index]                          # get the agent
            goal = world.goals_pos[agent]                             # goal pos, of this agent

            current_step = current_steps[agent - 1]                   # get current step

            paths[agent].append(current_step)                         # update the path for this agent

            if current_step != goal:                                       # in case we didnt arrived to the goal pos, keep loking for the next step
                steps_queue = get_possible_steps(current_step, goal, current_steps, prev_steps, world)
                print("time: ", i, " current step: ", current_step," goal: ", goal, " next_step: ", steps_queue.get())
                current_step = getNextStep(current_step, goal)             # find the next step

                if checkConflict(current_step, current_steps,prev_steps):  # Check if this step conflicts with other steps
                    conflict_steps[i].append(current_step)

                current_steps[agent - 1] = current_step                    # update the current steps list
            else:                                                          # in case we arrived to the goal
                del agents_list[agent_index]                               # remove this agent from list

        print("current\n", current_steps, "\nprev\n", prev_steps)
        i += 1                                                             #Advances the steps in one
    print("the paths:\n", paths)
    return paths, conflict_steps

#the method get step, and return the next step to goal
def getNextStep(step, goal):
    step_x, step_y, step_z = step
    goal_x, goal_y, goal_z = goal

    if step_z != goal_z:            #first arrived to the correct z
        return (step_x, step_y, step_z + 1) if step_z < goal_z else (step_x, step_y, step_z - 1)
    elif step_y != goal_y:         #then to the correct y
        return (step_x, step_y + 1, step_z) if step_y < goal_y else (step_x, step_y - 1, step_z)
    else:                          #finaly to correct x
        return (step_x + 1, step_y, step_z) if step_x < goal_x else (step_x -1 , step_y, step_z)

#the method get step, and currnt step dict, and prev steps dict, and check if this step conflict with the steps on the dicts, return 1 in case their is a conflict and 0 if their not
def checkConflict(step, current_steps, prev_steps):

    if step in current_steps or step in prev_steps:              #in case their a conflict return 1
        return 1
    return 0"""

# the method get step, and dict of steps and check that their are no conflict in this step, retuen True in case the step free.
def check_free_step(step,agent, step_unit):

    # In case the step is in dictionaries then we will check that their value is not equal to that agent
    if step in step_unit.current_steps_list:
        if step_unit.current_steps_list.index(step) != agent.id - 1:         # this step not free
            return False
    if step in step_unit.prev_steps:
        if step_unit.prev_steps.index(step) != agent.id - 1:                 # this step not free
            return False

    return True

#the method get step, and return the next free step to goal
def get_possible_steps(agent, step_unit, world):

    possible_steps = queue.Queue()

    # add to queue all the free steps that are in the right direction.
    for coordinate in range(2, -1, -1):
        if agent.current_step[coordinate] != agent.goal_pos[coordinate]:                              # check if the coordinate not in the right place already.
            direction = 1 if agent.current_step[coordinate] < agent.goal_pos[coordinate] else -1  # Sets the direction to the goal, up (=1) or down(=-1)
            next_step = list(agent.current_step)
            next_step[coordinate] += direction                                                    # get the next step
            if check_free_step(tuple(next_step), agent, step_unit):                                # if this step free add to queue
                possible_steps.put(tuple(next_step))

    # add the rest of the steps to queue
    for coordinate in range(2, -1, -1):
        direction = 1 if agent.current_step[coordinate] < agent.goal_pos[coordinate] else -1      # Sets the direction to the goal, up (=1) or down(=-1)
        next_step = list(agent.current_step)
        next_step[coordinate] += direction
        if tuple(next_step) not in possible_steps.queue:                                          # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), agent, step_unit):                                # check if this step is free.
                if world.is_valid_pos(tuple(next_step)):                                          # check if the step is valid
                    possible_steps.put(tuple(next_step))

        next_step = list(agent.current_step)                                            # check for step in the opposite direction
        next_step[coordinate] -= direction
        if tuple(next_step) not in possible_steps.queue:                                # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), agent, step_unit):                      # check if this step is free.
                if world.is_valid_pos(tuple(next_step)):                                # check if the step is valid
                    possible_steps.put(tuple(next_step))

    return possible_steps

# this method return one step for all agents, without collision.
def get_next_step(agents, index, step_unit, world):

    if index >= len(agents):                                     # Stop conditions, in case we found a step for all the agents.
        return True

    steps = get_possible_steps(agents[index], step_unit, world)  # get all steps that without collision

    if not steps:                                                # in case their are no free next step.
        return False

    for step in steps.queue:                                     # pass on all possible steps, until we found free step for all.

        if infinite_loop_test(agents[index].path, step):         # End Case, In case we have reached an infinite loop, we will move on to the next step
            continue

        step_unit.update_current_step(step, agents[index].id)    # update the current steps
        index += 1
        if get_next_step(agents, index, step_unit, world):       # get free step for the next agent.
            return True

    return False

# the method get step, and path of agent, and checks if the drone can go this step or it will cause an endless loop
def infinite_loop_test(path, step):                    # return true in case their is endless loop

    if len(path) > 4:
        if step in path[len(path) - 4:]:
            return True
    elif step in path:
        return True
    return False

def path_finding(agents, world):

    # ----------------------------initialization------------------------------------------------
    agents_list = agents.copy()                        # copy of agent list, for not destroy the original list
    paths = {}                                         # a dictionary of the paths, for each agent the path
    step_unit = StepUnit(0)                            # Initialize the first time step

    for agent in agents_list:                                   # initialize the list of current_steps with start pos
        step_unit.add_current_step_to_list(agent.start_pos)     # add start pos, for each agent
        paths[agent.id] = [agent.start_pos]                     # initialize the value of paths dict to the start pos

    # -----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while agents_list:

        step_unit.set_prev_steps(step_unit.current_steps_list)     # update the prev steps list, to the last current steps list

        # call for method that try to find free step for all agents
        if get_next_step(agents_list, 0, step_unit, world):                # we fount step for all agents
            #print("current\n", step_unit.current_steps_list, "\nprev\n", step_unit.prev_steps)
            current_steps = step_unit.current_steps_list
            step_unit = StepUnit(step_unit.time + 1)                       # Advances the steps in one
            step_unit.set_current_steps_list(current_steps)                # update the current steps for the new time

            for agent_index in xrange(len(agents_list) - 1, -1, -1):       # iterate over the list of agent left.
                agent = agents_list[agent_index]                           # get the agent
                paths[agent.id].append(current_steps[agent.id - 1])        # update paths dict
                agent.set_path(paths[agent.id])                            # update the path for agent
                agent.set_current_step(current_steps[agent.id - 1])        # update the current step for this agent

                if current_steps[agent.id - 1] == agent.goal_pos:          # in case this agent arrived to goal
                    del agents_list[agent_index]                           # remove agent from agents list
        else:
            print("we didnt find free step for all the agents")
            return

    return paths





