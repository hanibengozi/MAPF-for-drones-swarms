from step import *



# this function get step, and return all the possible valid next steps for this step (neighbors)
# this method get also the world, for checking validation of the return next step.
# the method return list of all steps, each step from type Step, that include the pos, and the coordinate and if this step with deviation or not.
def get_all_steps(agent, world):
    steps = []
    is_goal = 0

    for coordinate in range(2,-1,-1):
        direction = 1 if agent.current_step[coordinate] < agent.goal_pos[coordinate] else -1  # Sets the direction to the goal, up (=1) or down(=-1)

        with_deviation = 1  # define that this step with deviation from goal
        without_deviation = 0  # define that this step without deviation

        if agent.current_step[coordinate] == agent.goal_pos[coordinate]: # in case this coordinate already in place, both movement are with deviation
            with_deviation = 2
            without_deviation = 2

        next_step = list(agent.current_step)
        next_step[coordinate] += direction                  # up, or right

        if tuple(next_step) == agent.goal_pos:             # define if this step is goal
            is_goal = 1

        if world.is_valid_pos(tuple(next_step)):            # if this step valid, add to steps list
            next_step = Step(tuple(next_step), coordinate, without_deviation, agent.id, is_goal)
            steps.append(next_step)

        next_step = list(agent.current_step)
        next_step[coordinate] -= direction                  # down, or left

        if tuple(next_step) == agent.goal_pos:             # define if this step is goal
            is_goal = 1

        if world.is_valid_pos(tuple(next_step)):            # if this step valid, add to steps list
            next_step = Step(tuple(next_step), coordinate, with_deviation, agent.id, is_goal)
            steps.append(next_step)
    return steps

# the method get step, and return the next step to goal
# for the method that find paths with collision
def get_next_step_with_collision(step, goal):
    step_x, step_y, step_z = step
    goal_x, goal_y, goal_z = goal

    if step_z != goal_z:         # first arrived to the correct z
        return (step_x, step_y, step_z + 1) if step_z < goal_z else (step_x, step_y, step_z - 1)
    elif step_y != goal_y:       # then to the correct y
        return (step_x, step_y + 1, step_z) if step_y < goal_y else (step_x, step_y - 1, step_z)
    else:                        # finaly to correct x
        return (step_x + 1, step_y, step_z) if step_x < goal_x else (step_x - 1, step_y, step_z)

# this method  trying to move fix step, in case of succses update that this agent need to return back to goal
def move_fix_step(step, agent, time_unit, world):

    # 1. למצוא מקום פנוי מאחד השכנים שלו, עבור הצעד הקבוע
    # trying to find free next step, for fix step to move
    fix_step = step.collides_with_fix
    free_step_to_fix_step = None
    steps = get_all_steps(fix_step, world)                   # get all steps (nighbors for fix step)
    for s in steps:
        if check_free_step(s, time_unit.prev_time_unit.current_steps):    # if the nighbors dont collides with steps in prev time
            if s.collides_with != s.Collision.collides_fix:  # and this step not collides with fix
                free_steps_to_fix_step = s                   # save this step

    if free_step_to_fix_step:                                # in case we find free step to fix step
        # update the fix step path
        # update for fix step to go back next time
        # update in this time that fix agent not in place, remove this agent from fix steps in this time
    else:                                                    # in case we didnt find free step to fix step
        return False

    # 2. לבדוק שבזמן אחורה הצעד הפנוי ריק
    # אם כן לעדכן צעד זה במסלול של הקבוע, לעדכן לו שהוא צריך לחזור למקום, ולהחזיר את הצעד שפיניתי עבור הרחפן שרצה לעבור שם
    # אם לא לבדוק האם יש לי עוד שכן פנוי, ואם אין אז לעקוף על הצעד הקבוע הזה, ו
    # this method get agent that contain all possible steps, and return the next step, that not collides with another agent.
    # the method return the step with the highest priority
def get_next_step(agent, time_unit, world):

    steps = get_possible_steps(agent, time_unit, world)     # get all possible steps

    for step in steps:
        if check_free_step(step, time_unit.current_steps):             # if this step not collides with current steps

            # in case i take the same step, stay in place. and it not the goal, count how many times in the same place
            if step.coordinate == -1 and step.step != agent.goal_pos:
                if step.step == agent.stay_in_place[0]:
                    agent.stay_in_place[1] += 1
                    print("agent: ", agent.id, "stay in place: ", step.step)
                else:
                    agent.stay_in_place = [step.step, 0]

            # treatment when the step collides with fix step
            if step.collides_with == step.Collision.collides_fix:
                if not move_fix_step(step, agent, time_unit, world):         # in case we move the fix step, choose this step for this agent
                    continue                                      # in case we cant move the fix step, choose another step for this agent

            return step

    return None         # in case we their are no next steps

# this method get step, and return list of possible free next steps, that not collides with fix and prev steps.
# sort them by priority, first without deviation, second all the coordinate that not in right place already, then the rest
# every category sort firs z, then y, then x
def get_possible_steps(agent, time_unit, world):
    sorted_steps = []

    steps = get_all_steps(agent, world)          # get all possible valid next steps for the step.

    if agent.current_step == agent.goal_pos:     # in case this agent already in goal
        step = Step(agent.current_step, -1, 0, agent.id, 1)
        sorted_steps.append(step)

    # pass on all the steps, and take first the steps without deviation
    for step in steps:
        if not step.deviation:                               # in case this step without deviation, deviation = 0
            if check_free_step(step, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)

    # enter the the same step, in case we want to stay in place
    step = Step(agent.current_step, -1, 0, agent.id)
    sorted_steps.append(step)
    return sorted_steps

    # pass on all the steps, and take second the steps with deviation that the coordinate not in right place yet.
    for step in steps:
        if step.deviation == 1:
            if check_free_step(step, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)


    # take all the rest of steps
    for step in steps:
        if step not in sorted_steps:
            if check_free_step(step, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)


# the method get step, and dict of steps and check that their are no conflict in this step, retuen True in case the step free.
def check_free_step(step, steps_list):

    # In case the step is in dictionaries then we will check that their value is not equal to that agent
    for s in steps_list:
        if step.step == s.step:
            if step.agent != s.agent:
                if not s.is_goal:         # in case this step not collides with fix steps, Other treatment for fix steps
                    return False
                else:                     # in case this step collides with fix step, return this step and update for late checking
                    step.collides_with = step.Collision.collides_fix
                    step.collides_with_fix = s
                    return True

    return True

# this method get dict of paths, and return for each path his length
# return dict, the key- agent id, the value- length of path for this agent
def get_path_len(paths):
    len_paths = {}

    for agent in paths:
        len_paths[agent] = len(paths[agent])

    return len_paths

# this method get list of agents, and sort the array, according to the length of their path with conflicts
# this method chang the given list of the agents
def sort_agents(agents, paths_len_with_conflicts):

    # sort the dict of the path len
    sorted_path_len = dict(sorted(paths_len_with_conflicts.items(), key=lambda item: item[1]))
    i = 0

    for agent in sorted_path_len:
        agents[i] = agent
        i += 1

    agents.reverse()
# the method return true when all the agents arrived to goal
def got_to_goal(agents_list, paths):

    for agent in agents_list:
        if agent.current_step != agent.goal_pos:
            return False

    return True

# this method check for each agent how many time he stay in place, if is more than 4, sort the agents
# By who stays in the place the longest
def sort_agents_by_time_of_stay_in_place(agents):
    agents_len_by_stay_in_place = {}
    flag = 0

    for agent in agents:                               # get the length of how many time each agent stay in place
        agents_len_by_stay_in_place[agent] = agent.stay_in_place[1]
        if agent.stay_in_place[1] > 8:                    # in case of a least one of the agent stay in place more than 4 times
            flag = 1                                   # sort the array

    if flag:
        sort_agents(agents, agents_len_by_stay_in_place)

        for agent in agents:        # After sorting, reset the time of saty in place for each drone.
            agent.stay_in_place[1] = 0



# this method get list of agents, from type object dron, and return list of their id`s
def get_agents_id(agents):
    agents_id = []
    for agent in agents:
        agents_id.append(agent.id)
    return agents_id

# this method get dict of paths that the key is object dron, and return the path by id- dron id
def get_paths_by_id(paths):
    paths_by_agent_id = {}

    for agent in paths:
        paths_by_agent_id[agent.id] = paths[agent]

    return paths_by_agent_id