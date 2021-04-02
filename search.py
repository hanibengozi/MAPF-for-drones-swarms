import general_functions
from time_unit import *
from step import *
from pip._vendor.msgpack.fallback import xrange

# this method find paths for all agents, with conflicts
def path_finding_with_conflicts(agents):
    # ----------------------------initialization------------------------------------------------
    agents_list = agents.copy()    # copy of agent list, for not destroy the original list
    paths = {}                     # a dictionary of the paths, for each agent the path
    current_steps = []

    for agent in agents_list:  # initialize the list of current_steps with start pos
        current_steps.append(agent.start_pos) # add start pos, for each agent
        paths[agent] = [agent.start_pos]  # initialize the value of paths dict to the start pos

    # -----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while agents_list:

        while agents_list:
            for agent_index in xrange(len(agents_list) - 1, -1, -1):  # iterate over the list of agent left.
                agent = agents_list[agent_index]                      # get the agent
                current_step = current_steps[agent.id - 1]
                next_step = general_functions.get_next_step_with_collision(current_step, agent.goal_pos)
                current_steps[agent.id -1] = next_step
                paths[agent].append(next_step)

                if next_step == agent.goal_pos:
                    del agents_list[agent_index]                      # remove agent from agents list

    return paths

# this method find paths for all agents without conflicts
def path_finding(agents, world):

    # ----------------------------initialization------------------------------------------------
    paths = {}                                         # a dictionary of the paths, for each agent the path
    current_steps = []
    is_goal = 0
    time_unit = TimeUnit(1, None)                      # Initialize the first time step

    # sort the agents according to the length of the paths with conflicts
    paths_with_conflicts = path_finding_with_conflicts(agents)
    paths_len_with_conflicts = general_functions.get_path_len(paths_with_conflicts)
    general_functions.sort_agents(agents, paths_len_with_conflicts)

    for agent in agents:                              # initialize the list of current_steps with start pos
        if agent.start_pos == agent.goal_pos:         # in case start pos == goal pos, define goal pos for this step
            is_goal = 1

        # define step, step = start pos, coordinate = -1, deviation = 0, and if this goal pos
        step = Step(agent.start_pos, -1, 0, agent, is_goal)
        time_unit.add_current_step(step)              # add start pos step, to the current step list, for each agent
        time_unit.add_prev_step(step)                 # add start pos step, to the prev step list, for each agent
        paths[agent.id] = [agent.start_pos]           # initialize the value of paths dict to the start pos

    # -----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while not general_functions.got_to_goal(agents, paths):     # loop until all the agents got to goal

        counter = 0
        for agent in agents:                                    # iterate on agents, for each agent find next step.

            if time_unit.time != len(paths[agent.id]):      # in case of fix step movment, dont find next step until the rigth time.
                add = 1
                step = Step(paths[agent.id][time_unit.time], -1, 2, agent)
                time_unit.add_current_step(step) # update the step for the agent that waiting to return to his goal.
                agent.current_step = step.step
                for current_step in current_steps:
                    if current_step.step == step.step and current_step.agent == step.agent:
                        add = 0
                if add:
                    current_steps.append(step)
                print("this agent: ", agent.id, " find next step in time: ", time_unit.time, " the next step is: ", step.step, " is goal: ", step.is_goal, agent.stay_in_place)
                continue

            new_step = general_functions.get_next_step(agent, time_unit, world)   # get next step

            if new_step:                                                          # their is next step for this agent
                print("this agent: ", agent.id, " find next step in time: ", time_unit.time, " the next step is: ", new_step.step, " is goal: ", new_step.is_goal, agent.stay_in_place)

                update_movment_of_fix(agents, paths, current_steps, time_unit)                   # in case we move fix step, make some updates
                time_unit.add_current_step(new_step)                              # add this step to current steps
                agent.current_step = new_step.step                                # update the current step for this agent
                paths[agent.id].append(new_step.step)                             # update the path for this agent
                current_steps.append(new_step)                                    # save the current step in list, for the update the prev steps in next time

                if new_step.step == agent.goal_pos:
                    time_unit.add_fix_step(new_step.step)                              # add this step to fix steps
                    print("agent: ", agent.id, "arrive to goal!")
                    counter += 1

            else:                                                                 # in case, this agent stuck
                print("agent: ", agent.id, " stuckkkkkkkkkkkkk!!!!!!!!!!")
                return paths
        # לבדוק האם צריך למיין לפי מי שנשאר הרבה זמן במקום ולמיין
        general_functions.sort_agents_by_time_of_stay_in_place(agents)
        # לשאול את דבורה האם להשאיר במקום זה צריך להיות בעדיפות יותר מאשר סטייה כי אם אין לי אופציות בלי סטייה אז הוא כל הזמן נשאר במקום
        # לטפל בכל האופציות של להוזיז קבוע וכו
        print("the number of agents that didnt arrived to goal is: ", len(agents) - counter)
        time_unit = TimeUnit(time_unit.time + 1, time_unit)                       # Advances the steps in one
        time_unit.set_prev_steps(current_steps)                                   # update the prev steps for next time
        time_unit.set_current_steps(current_steps)                                # update the current steps with prev steps for next time
        time_unit.step_in_time_forbidden = time_unit.prev_time_unit.step_in_time_forbidden.copy()
        current_steps = []                                                        # reset the current steps temp for next time

    return paths

def update_movment_of_fix(agents, paths, current_steps, time_unit):

    # check if need to make changes
    if time_unit.update:
        fix_step_agent = time_unit.update[0].agent.id

        # update the path for fix step
        for time in range(time_unit.time - 1, time_unit.time + 2):
            if time < len(paths[fix_step_agent]):
                paths[fix_step_agent][time] = time_unit.update[1].step    # update the path with free new step, in prev
            else:
                paths[fix_step_agent].append(time_unit.update[1].step)   # update the path with free new step, in current next

        # after move the fix step, delete this fix step from fix steps list
        time_unit.remove_fix_step(time_unit.update[0])
        time_unit.remove_step_current(time_unit.update[0])

        for step in current_steps:
            if step.step == time_unit.update[0].step and step.agent == time_unit.update[0].agent:
                current_steps.remove(step)

        """if time_unit.update[0] in current_steps:
            current_steps.remove(time_unit.update[0])"""

        # update current steps list with the free next step -  That the fixed agent moves there.
        time_unit.add_current_step(time_unit.update[1])
        current_steps.append(time_unit.update[1])
