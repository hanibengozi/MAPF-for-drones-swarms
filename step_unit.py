class StepUnit:
    def __init__(self, time):
        self.time = time
        self.prev_steps = []             # A dictionary that contains all the steps that were occupied in a previous unit of time
        self.current_steps_list = []
        self.dict_occupied = {}
        #self.blocked_steps = {}
        self.conflicts = []              # list of steps that there have a conflict

    # add step to dict occupide
    def add_step_dict_occupied(self, step, agent_id):
        self.dict_occupied[step] = agent_id

    # delete step from dict occupied
    def delete_step_dict_occupied(self, step):
        del self.dict_occupied[step]

    # add the block steps to occupied dict if their not already in
    def add_blockSteps_toOccupied(self, blocked_steps):

        for block_step in blocked_steps:
            if block_step not in self.dict_occupied:
                self.dict_occupied[block_step] = blocked_steps[block_step]


    # add current step to current step list
    def add_current_step_to_list(self, current_step):
        self.current_steps_list.append(current_step)

    # update current step list
    def update_current_step(self, current_step, agent_id):
        if not current_step:
            current_step = self.prev_steps[agent_id - 1]
        self.current_steps_list[agent_id - 1] = current_step

    # set current steps list
    def set_current_steps_list(self, current_steps):
        self.current_steps_list = current_steps.copy()

    # set prev steps
    def set_prev_steps(self, prev_steps):
        self.prev_steps = prev_steps.copy()