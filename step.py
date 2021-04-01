from enum import Enum


class Step:

    class Collision(Enum):
        without_collision = 0
        collides_current = 1
        collides_prev = 2
        collides_fix = 3

    def __init__(self, step, coordinate, deviation, agent, is_goal=0):
        self.step = step                                         # the location of the step on the world
        self.coordinate = coordinate                             # Determine from which coordinate this step came,
                                                                 # 0=x, 1=y, 2=z, -1= for the start step, and if this is the same step
        self.deviation = deviation                               # set if this step deviates from the goal or not,
                                                                 # 0 = goal in the direction to goal, 1= deviates from the goal, 2= deviates from the goal and the coordinate already in place
        self.agent = agent                                       # define which drone in this step
        self.collides_with = self.Collision.without_collision    # in beginning their are no collision
        self.collides_with_fix = None                            # in case this step collides with fix, save the fix step
        self.is_goal = is_goal                                   # in case this step is goal step for this agent.

    def set_collides_with(self, collides_with):                  # set with how this step collides
        self.collides_with = self.Collision(collides_with)

    def set_collides_with_fix(self, fix_step):
        self.collides_with_fix = fix_step