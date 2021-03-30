class Drone:
    def __init__(self, id, start_pos, goal_pos, speed=None):
        self.id = id                                  # agent id, from 1...... num_agents
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.speed = speed
        self.current_step = start_pos
        self.stay_in_place = [start_pos, 0]
        self.path = []
        self.steps = []

    def set_current_step(self, current_step):
        self.current_step = current_step

    def set_path(self, path):
        self.path = path