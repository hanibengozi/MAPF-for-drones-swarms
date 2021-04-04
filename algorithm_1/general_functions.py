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
        next_step[coordinate] += direction                 # up, or right

        if tuple(next_step) == agent.goal_pos:             # define if this step is goal
            is_goal = 1                                    # define if this agent in goal more than one time.

        if world.is_valid_pos(tuple(next_step)):           # if this step valid, add to steps list
            next_step = Step(tuple(next_step), coordinate, without_deviation, agent, is_goal)
            steps.append(next_step)

        next_step = list(agent.current_step)
        next_step[coordinate] -= direction                 # down, or left

        if tuple(next_step) == agent.goal_pos:             # define if this step is goal
            is_goal = 1

        if world.is_valid_pos(tuple(next_step)):           # if this step valid, add to steps list
            next_step = Step(tuple(next_step), coordinate, with_deviation, agent, is_goal)
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
    fix_agent_goal_pos = fix_step.agent.goal_pos
    if fix_step.step != agent.goal_pos:
        fix_step.agent.goal_pos = agent.goal_pos                       # to get all steps with deviation according to agent goal

    steps = get_all_steps(fix_step.agent, world)                   # get all steps (nighbors for fix step)

    for s in steps:
        if check_free_step(s, time_unit, time_unit.prev_time_unit.current_steps):    # if the nighbors dont collides with steps in prev time
            if check_free_step(s, time_unit, time_unit.current_steps):
                if s.collides_with != s.Collision.collides_fix:  # and this step not collides with fix
                    if s.deviation:
                        free_step_to_fix_step = s                   # save this step

    fix_step.agent.goal_pos = fix_agent_goal_pos                # update back the goal pos for fix agent

    if free_step_to_fix_step:                                 # in case we find free step to fix step
        time_unit.update = [fix_step, free_step_to_fix_step] # define to update the changes
        return True
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
        if check_free_step(step, time_unit, time_unit.current_steps):             # if this step not collides with current steps

            #if agent.update_change_direction and step.deviation != 0:      # for provide next time to choose step, that make infinity loop.
                #agent.change_direction.append((time_unit.time + 1, step.coordinate))

            #if (time_unit.time, step.coordinate) in agent.change_direction: # in case this step make infinity loop, countiue
                #continue

            #if step.step in agent.forbidden_steps:
                #continue

            # in case i take the same step, stay in place. count how many times in the same place
            if step.step == agent.stay_in_place[0]:
                agent.stay_in_place[1] += 1
                #if step.step != agent.goal_pos and agent.stay_in_place[1] > 2:
                    #continue
            else:
                agent.stay_in_place = [step.step, 1]

            # treatment when the step collides with fix step
            if step.collides_with == step.Collision.collides_fix:
                if not move_fix_step(step, agent, time_unit, world):   # in case we move the fix step, choose this step for this agent
                    continue                                      # in case we cant move the fix step, choose another step for this agent
        else:
            continue
        return step

    return None         # in case we their are no next steps

# this method get step, and return list of possible free next steps, that not collides with fix and prev steps.
# sort them by priority, first without deviation, second all the coordinate that not in right place already, then the rest
# every category sort firs z, then y, then x
def get_possible_steps(agent, time_unit, world):
    sorted_steps = []
    agent.update_change_direction = False

    steps = get_all_steps(agent, world)          # get all possible valid next steps for the step.

    if agent.current_step == agent.goal_pos:     # in case this agent already in goal
        step = Step(agent.current_step, -1, 0, agent, 2)
        sorted_steps.append(step)

    # pass on all the steps, and take first the steps without deviation
    for step in steps:
        if not step.deviation:                                # in case this step without deviation, deviation = 0
            if check_free_step(step, time_unit, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)

    # enter the the same step, in case we want to stay in place
    step = Step(agent.current_step, -1, 0, agent)
    sorted_steps.append(step)

    # pass on all the steps, and take second the steps with deviation that the coordinate not in right place yet.
    for step in steps:
        if step.deviation == 2:
            if check_free_step(step, time_unit, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)

    # take all the rest of steps
    for step in steps:
        if step not in sorted_steps and step.deviation:
            if check_free_step(step, time_unit, time_unit.prev_steps):   # check collision with prev (prev + fix) steps list
                sorted_steps.append(step)

    return sorted_steps

# the method get step, and dict of steps and check that their are no conflict in this step, retuen True in case the step free.
def check_free_step(step, time_unit, steps_list):

    # In case the step is in dictionaries then we will check that their value is not equal to that agent
    for s in steps_list:
        if step.step == s.step:
            if step.agent.id != s.agent.id:
                # in case this step not collides with fix steps or in the case the agents are not waiting for each other
                if s.is_goal <= 1 and not in_step_in_time_forbidden(step.agent, s.agent, s, time_unit):
                    time_unit.step_in_time_forbidden.append(((step.agent.id, s.agent.id), time_unit.time))
                    return False
                else:                     # in case this step collides with fix step, return this step and update for late checking
                    step.collides_with = step.Collision.collides_fix
                    step.collides_with_fix = s
                    return True

    return True

# this method get 2 agents, and return if they collides between each other more than one time
def in_step_in_time_forbidden(agent, agent_collides, agent_collides_step, time_unit):

    if agent_collides_step.step != agent_collides.current_step:  # in case the agents collides in current and prev
        return False

    if ((agent.id , agent_collides.id), time_unit.time - 1) in time_unit.step_in_time_forbidden:
        if ((agent_collides.id , agent.id), time_unit.time - 1) in time_unit.step_in_time_forbidden:
            if ((agent_collides.id , agent.id), time_unit.time) in time_unit.step_in_time_forbidden:
                return True
    return False

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

# the method return true when all the agents arrived to goal, or when the algorithm found paths for anyone who succeeded
# the method return True, and list of agents that the algorithm cant fount path for them.
def got_to_goal(agents_list, paths):

    agents_without_solution = []

    for agent in agents_list:

        if len(paths[agent.id]) > len(agents_list) * 2:  # the len of agent path is too long - infinity loop
            agents_without_solution.append(agent)

        # there agent that didnt arrived to goal yet.
        if agent.current_step != agent.goal_pos and len(paths[agent.id]) <= len(agents_list) * 2:
            return False, []

    return True, agents_without_solution

# this method check for each agent how many time he stay in place, if is more than 4, sort the agents
# By who stays in the place the longest
def sort_agents_by_time_of_stay_in_place(agents):
    agents_len_by_stay_in_place = {}
    flag = 0

    # get the length of how many time each agent stay in place
    for agent in reversed(agents):
        if agent.stay_in_place[0] != agent.goal_pos:
            agents_len_by_stay_in_place[agent] = agent.stay_in_place[1]
            if agent.stay_in_place[1] > 1:                           # in case of a least one of the agent stay in place
                flag = 1                                             # define that we need to sort the array
        else:
            agents_len_by_stay_in_place[agent] = 0                   # if agent in goal, put him in the end of list

    if flag:
        sort_agents(agents, agents_len_by_stay_in_place)

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