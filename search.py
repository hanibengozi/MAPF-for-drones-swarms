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
    time_unit = TimeUnit(0, None)                      # Initialize the first time step

    # sort the agents according to the length of the paths with conflicts
    paths_with_conflicts = path_finding_with_conflicts(agents)
    paths_len_with_conflicts = general_functions.get_path_len(paths_with_conflicts)
    general_functions.sort_agents(agents, paths_len_with_conflicts)

    for agent in agents:                              # initialize the list of current_steps with start pos
        if agent.start_pos == agent.goal_pos:         # in case start pos == goal pos, define goal pos for this step
            is_goal = 1

        # define step, step = start pos, coordinate = -1, deviation = 0, and if this goal pos
        step = Step(agent.start_pos, -1, 0, agent.id, is_goal)
        time_unit.add_current_step(step)              # add start pos step, to the current step list, for each agent
        time_unit.add_prev_step(step)                 # add start pos step, to the prev step list, for each agent
        paths[agent.id] = [agent.start_pos]           # initialize the value of paths dict to the start pos

    # -----------------------------stay in loop, until we find path for evrey agent-----------------------------
    while not general_functions.got_to_goal(agents, paths):     # loop until all the agents got to goal

        counter = 0
        for agent in agents:                                    # iterate on agents, for each agent find next step.
            new_step = general_functions.get_next_step(agent, time_unit, world)   # get next step

            if new_step:                                                          # their is next step for this agent
                print("this agent: ", agent.id, " find next step in time: ", time_unit.time, " the next step is: ",new_step.step)

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
        current_steps = []                                                        # reset the current steps temp for next time

    return paths