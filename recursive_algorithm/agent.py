
class Agent:
    def __init__(self, id, start_pos, goal_pos, speed=None):
        self.id = id                                  # agent id, from 1...... num_agents
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.speed = speed
        self.current_step = start_pos
        self.change_direction = []
        self.update_change_direction = False
        self.forbidden_step = []
        self.path = []
        self.time_got_to_goal = -1        # save the time when this agent arrived to goal, for restoring paths function.

    def set_forbidden_step(self, forbidden_step):
        self.forbidden_step = forbidden_step

    def set_current_step(self, current_step):
        self.current_step = current_step

    def set_path(self, path):
        self.path = path

    def add_time_cordinate_to_change_direction(self, cordinate_by_time):
        self.change_direction.append(cordinate_by_time)