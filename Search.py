from pip._vendor.msgpack.fallback import xrange


def find_path(agents, world, vialization=None):

    agents_list = agents.copy()
    current_steps = []
    prev_steps = []
    paths = {}

    agents_current_steps = {}           #optinal for vialization
    agent_prev_steps = {}
    conflict_steps = []

    #initialize the list of current_steps with start pos
    for agent in agents_list:
        current_steps.append(world.starts_pos[agent])   # add start pos, for each agent
        prev_steps.append(world.starts_pos[agent])
        paths[agent] = []                               #initialize the value of paths dict to empty list

    # optinal, for vialization
    i = 0


    #stay in loop, until we find path for evrey agent
    while agents_list:

        # optinal for vialization, intialize the dicts
        agents_current_steps[i] = {}
        agent_prev_steps[i] = {}

        for agent_index in xrange(len(agents_list) - 1, -1, -1):      #iterate over the list of agent left.
            agent = agents_list[agent_index]                          #get the agent
            goal = world.goals_pos[agent]                             #goal pos, of this agent

            current_step = current_steps[agent - 1]
            prev_step = prev_steps[agent - 1]

            paths[agent].append(current_step)                         #update the path for this agent

            # optinal for vialization
            agents_current_steps[i][agent]= current_step            #update the dict of the steps
            agent_prev_steps[i][agent] = prev_step

            if current_step != goal:               #in case we didnt arrived to the goal pos, keep loking for the next step
                prev_steps[agent - 1] = current_step    #update and save the prev step

                current_step = getNextStep(current_step, goal)       #find the next step

                #Check if this step conflicts with other steps
                if checkConflict(current_step, agents_current_steps[i], agent_prev_steps[i]):
                    conflict_steps.append(current_step)

                current_steps[agent - 1] = current_step

            else:                                   #in case we arrived to the goal
                del agents_list[agent_index]           #remove this agent from list


        #Advances the steps in one
        print("current\n", agents_current_steps, "\nprev\n", agent_prev_steps)
        i += 1

    print("the paths:\n", paths)
    if vialization:
        return agents_current_steps, agent_prev_steps, conflict_steps

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

    currentSteps = current_steps.values()
    prevSteps = prev_steps.values()

    if step in currentSteps or step in prevSteps:              #in case their a conflict return 1
        return 1

    return 0