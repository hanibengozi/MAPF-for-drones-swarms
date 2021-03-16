import queue

from pip._vendor.msgpack.fallback import xrange


# this method get agent and the world, and return path for each agent without collision
def find_path(agents, world):

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
    return 0

# the method get step, and dict of steps and check that their are no conflict in this step, retuen True in case the step free.
def check_free_step(step, steps):
    if step not in steps:
        return True
    return False

#the method get step, and return the next free step to goal
def get_possible_steps(step, goal, current_steps, prev_steps, world):

    possible_steps = queue.Queue()

    steps = current_steps + list(set(prev_steps) - set(current_steps))    #put the current and prev steps in pne list, without duplicates

    # add to queue all the free steps that are in the right direction.
    for coordinate in range(2, -1, -1):
        if step[coordinate] != goal[coordinate]:                          # check if the coordinate not in the right place already.
            direction = 1 if step[coordinate] < goal[coordinate] else -1  # Sets the direction to the goal, up (=1) or down(=-1)
            next_step = list(step)
            next_step[coordinate] += direction                            # get the next step
            if check_free_step(tuple(next_step), steps):                  # if this step free add to queue
                possible_steps.put(tuple(next_step))

    # add the rest of the steps to queue
    for coordinate in range(2, -1, -1):
        direction = 1 if step[coordinate] < goal[coordinate] else -1      # Sets the direction to the goal, up (=1) or down(=-1)
        next_step = list(step)
        next_step[coordinate] += direction
        if tuple(next_step) not in possible_steps.queue:                  # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), steps):                  # check if this step is free.
                if world.is_valid_pos(tuple(next_step)):                  # check if the step is valid
                    possible_steps.put(tuple(next_step))

        next_step = list(step)                                            # check for step in the opposite direction
        next_step[coordinate] -= direction
        if tuple(next_step) not in possible_steps.queue:                  # check if this next step not already in the queue.
            if check_free_step(tuple(next_step), steps):                  # check if this step is free.
                if world.is_valid_pos(tuple(next_step)):  # check if the step is valid
                    possible_steps.put(tuple(next_step))

    return possible_steps


#def get_next_step(drones, index, current_steps):
#if(index> drones.length)

   #current_steps = copy_curren
  #  return true
# steps = getPossibleSteps(drones[index], current_steps) # get all steps that without collision
# steps.count == 0
#   return false
#  for(step in steps)
#     copy_current_step = current_steps.copy()
#    update_step(step, copy_current_steps)
#    if(getNextStep(array, index++, copy_current_steps))
#       return true

#  return false