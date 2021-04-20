
# this class describe time unit, that in this time all the agents try to move one step to goal, without collision
# this class contain dictionaries that contain all the info that we need in this time unit.

class TimeUnit:
    def __init__(self, time, prev_time_unit):
        self.time = time
        self.prev_steps = []                        # contain only the prev step
        self.current_steps = []                     # contain all the steps in this time, prev, fix and current
        self.fix_steps = []                         # contain the fix steps
        self.prev_time_unit = prev_time_unit
        self.step_in_time_forbidden = []
        self.update = None

    # this method add current step to the current step list
    def add_current_step(self, current_step):
        # in case we add the same step for drone, d`ont add twice
        if current_step not in self.current_steps:
            self.current_steps.append(current_step)

    # this method add prev step to the prev step list
    def add_prev_step(self, prev_step):
        self.prev_steps.append(prev_step)

    # this method add fix step to the fix step list
    def add_fix_step(self, fix_step):
        if fix_step not in self.fix_steps:
            self.fix_steps.append(fix_step)

    # this method get fix step and take it off the list
    def remove_fix_step(self, fix_step):
        if fix_step in self.fix_steps:
            self.fix_steps.remove(fix_step)

    # this method get fix step and take it off the list
    def remove_step_current(self, step):
        for current_step in self.current_steps:
            if current_step.step == step.step and current_step.agent == step.agent:
                self.current_steps.remove(current_step)

    def set_prev_steps(self, prev_steps):
        self.prev_steps = prev_steps.copy()

    def set_current_steps(self, current_steps):
        self.current_steps = current_steps.copy()