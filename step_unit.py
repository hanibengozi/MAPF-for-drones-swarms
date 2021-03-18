class StepUnit:
    def __init__(self, time):
        self.time = time
        self.prev_steps = []             # A dictionary that contains all the steps that were occupied in a previous unit of time
        self.current_steps_list = []
        self.conflicts = []              # list of steps that there have a conflict


    # add current step to current step list
    def add_current_step_to_list(self, current_step):
        self.current_steps_list.append(current_step)

    # update current step list
    def update_current_step(self, current_step, agent_id):
        self.current_steps_list[agent_id - 1] = current_step

    # set current steps list
    def set_current_steps_list(self, current_steps):
        self.current_steps_list = current_steps.copy()

    # set prev steps
    def set_prev_steps(self, prev_steps):
        self.prev_steps = prev_steps.copy()