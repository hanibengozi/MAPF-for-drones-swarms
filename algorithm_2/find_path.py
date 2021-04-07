import algorithm_2.math_graph as math_graph
import random
from algorithm_2.math_graph import Point3D
from datetime import datetime
import math as m
from copy import deepcopy


class GraphManager:
    def __init__(self, matrix_cube_size):
        self.matrix_cube_size = matrix_cube_size

    def get_around_points(self, point):
        points = list()
        points.append(math_graph.Point3D(point.x + 1, point.y, point.z))
        points.append(math_graph.Point3D(point.x - 1, point.y, point.z))
        points.append(math_graph.Point3D(point.x, point.y + 1, point.z))
        points.append(math_graph.Point3D(point.x, point.y - 1, point.z))
        points.append(math_graph.Point3D(point.x, point.y, point.z + 1))
        points.append(math_graph.Point3D(point.x, point.y, point.z - 1))
        points_filtered = self.filter_matrix_points(points)
        return points_filtered

    def random_point(self):
        return Point3D(random.randint(
            0, self.matrix_cube_size[0] - 1), random.randint(0, self.matrix_cube_size[1] - 1),
            random.randint(0, self.matrix_cube_size[2] - 1))

    def get_original_path_length(self, from_point, to_point):
        return abs(from_point.x - to_point.x) + abs(from_point.y - to_point.y) + abs(from_point.z - to_point.z)

    def filter_matrix_points(self, points):
        points_filtered = list()
        for s in points:
            if s.x >= self.matrix_cube_size[0] or s.x < 0:
                continue
            if s.y >= self.matrix_cube_size[1] or s.y < 0:
                continue
            if s.z >= self.matrix_cube_size[2] or s.z < 0:
                continue

            points_filtered.append(s)

        return points_filtered

    def get_steps_to_destination1(self, current_point, to_point, can_stay):
        available_steps = list()
        # put the direction points
        available_steps.append(math_graph.Point3D(
            current_point.x + 1, current_point.y, current_point.z))
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y + 1, current_point.z))
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y, current_point.z + 1))
        available_steps.append(math_graph.Point3D(
            current_point.x - 1, current_point.y, current_point.z))
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y - 1, current_point.z))
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y, current_point.z - 1))
        available_steps_filtered = self.filter_matrix_points(available_steps)
        available_steps_filtered.reverse()
        return available_steps_filtered

    def get_steps_to_destination(self, current_point, to_point, can_stay):
        available_steps = list()
        # put the direction points
        if (current_point.z > to_point.z):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z - 1))
        elif current_point.z < to_point.z:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z + 1))
        if (current_point.y > to_point.y):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y - 1, current_point.z))
        elif current_point.y < to_point.y:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y + 1, current_point.z))
        if (current_point.x > to_point.x):
            available_steps.append(math_graph.Point3D(
                current_point.x - 1, current_point.y, current_point.z))
        elif current_point.x < to_point.x:
            available_steps.append(math_graph.Point3D(
                current_point.x + 1, current_point.y, current_point.z))

        # put the back direction points , add order go back if firsst direction
        if (current_point.z < to_point.z):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z - 1))
        elif current_point.z > to_point.z:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z + 1))
        if (current_point.y < to_point.y):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y - 1, current_point.z))
        elif current_point.y > to_point.y:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y + 1, current_point.z))
        if (current_point.x < to_point.x):
            available_steps.append(math_graph.Point3D(
                current_point.x - 1, current_point.y, current_point.z))
        elif current_point.x > to_point.x:
            available_steps.append(math_graph.Point3D(
                current_point.x + 1, current_point.y, current_point.z))

        if (current_point.z == to_point.z):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z - 1))
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z + 1))
        if (current_point.y == to_point.y):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y - 1, current_point.z))
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y + 1, current_point.z))
        if (current_point.x == to_point.x):
            available_steps.append(math_graph.Point3D(
                current_point.x - 1, current_point.y, current_point.z))
            available_steps.append(math_graph.Point3D(
                current_point.x + 1, current_point.y, current_point.z))

        if can_stay:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z))

        available_steps_filtered = self.filter_matrix_points(available_steps)
        available_steps_filtered.reverse()
        return available_steps_filtered


class Agent:
    def __init__(self, id, from_point, to_point, path_manager):
        self.id = id
        self.move_fixed_algo = False
        self.path_manager = path_manager
        self.from_point = from_point
        self.to_point = to_point
        self.path = []
        self.path_with_collision = False
        self.original_path_length = self.get_original_path_length()

    def get_original_path_length(self):
        return self.path_manager.get_original_path_length(self.from_point, self.to_point)


class AgentManager:
    def __init__(self, path_manager):
        self.next_id_counter = 0
        self.path_error_counter = 0
        self.cannot_move_fixed_error_counter = 0
        self.success_move = 0
        self.path_manager = path_manager
        self.agents = list()

    def get_agents_path_list(self):
        self.init_agents_path()

        def agent_order_key(a):
            return a.id

        self.agents.sort(key=agent_order_key, reverse=False)
        path = list()
        for a in self.agents:
            # print("path", a.path)
            path.append(a.path)
        return path

    def init_agent_path(self, a):
        a.path = self.path_manager.get_path(
            a.from_point, a.to_point, True, 0, a.id)

        if a.path == False:
            a.path = self.path_manager.get_path(
                a.from_point, a.to_point, True, 5, a.id)
            # print("a.path:", a.path)

        if a.path == False:
            # print("error:", a.from_point, ",", a.to_point)
            self.path_error_counter += 1

    def build_fixed_places(self):
        to_points = list(map(lambda a: (a.id, a.to_point), self.agents))
        from_points = list(map(lambda a: (a.id, a.from_point), self.agents))
        self.path_manager.build_fixed_places(to_points, from_points)

    def init_agent_path_algo_2(self, a):
        a.move_fixed_algo = True
        a.path = self.path_manager.get_path(a.from_point, a.to_point, False, 0, a.id)

    def resolve_agent_path_algo_2(self, a):
        if a.path != False:
            if not self.resolve_path_fixed_collision(a.path, a.id):
                self.cannot_move_fixed_error_counter += 1
                a.path = False
            else:
                self.success_move += 1
                self.path_error_counter -= 1

    def init_agents_path(self):
        def agent_order_key(a):
            return a.get_original_path_length()

        # order by path desc
        self.agents.sort(key=agent_order_key, reverse=True)
        # points = list(a.from_point for a in self.agents)
        # self.path_manager.set_first_points_busy(points)
        self.build_fixed_places()
        for a in self.agents:
            if a.path != False and len(a.path) > 0:
                self.path_manager.update_busy(a.path)

        # get path for each agent
        for a in self.agents:
            if a.path == False or len(a.path) == 0:
                self.init_agent_path(a)
                self.path_manager.update_busy(a.path)
                self.path_manager.update_fixed_places_arrived_time(
                    a.to_point, a.path)

        # update fixed agents collision

        # need to fix bug before using
        '''
        for a in self.agents:
            if a.path == False:
                self.init_agent_path_algo_2(a)
        for a in self.agents:
            if a.path != False and a.move_fixed_algo == True:
                self.resolve_agent_path_algo_2(a)
                self.path_manager.update_busy(a.path)
                self.path_manager.update_fixed_places_arrived_time(a.to_point, a.path)
        '''

    def resolve_path_fixed_collision(self, path, agent_id):
        if path == False:
            return True
        # add if the agent path is already know then we can also check the time
        valid_path = True
        time_moved = list()
        for p in path:
            fixed_point = self.path_manager.get_collision_fixed_point(
                Point3D.get_point_time_tuple(p), p[0], agent_id)
            valid_path = fixed_point is None
            if fixed_point is not None:
                agents_to_move = filter(
                    lambda a: a.id == fixed_point.agent_id, self.agents)
                agent_to_move = list(agents_to_move)[0]
                if agent_to_move.path == False:
                    valid_path = True
                    continue
                path = self.path_manager.move_fixed_point(
                    p[0], agent_to_move.path, fixed_point)
                if path == False:
                    valid_path = False
                    # print("len:", len(fixed_point.around_points_list))
                    # print("cannot move fixed point:", fixed_point, "agent id:", agent_id)
                    break
                else:
                    time_moved.append((p[0], fixed_point, path, agent_to_move))
                    valid_path = True
        if valid_path:
            for fm in time_moved:
                fm[3].path = fm[2]
                fm[1].fixed_moved_set(fm[0])
        return valid_path

    def create_agents(self, agent_points_list):
        # TODO validate points, from point not the same, next point of one no in the prev point
        for a in agent_points_list:
            self.next_id_counter += 1
            a = Agent(self.next_id_counter, a[0], a[1], self.path_manager)
            self.agents.append(a)

    def get_random_agents(self, agents_count):
        from_points = set()
        to_points = set()
        agents = list()
        from_point = None
        to_point = None
        for i in range(0, agents_count):
            while (True):
                from_point = self.path_manager.random_point()
                point_tuple = from_point.to_tuple()
                if point_tuple not in from_points:
                    from_points.add(point_tuple)
                    break

            while (True):
                to_point = self.path_manager.random_point()
                point_tuple = to_point.to_tuple()
                if point_tuple not in to_points:
                    to_points.add(point_tuple)
                    break
            agents.append([from_point, to_point])
        return agents


class PathManager:
    def __init__(self, graph_manager):
        self.points_manager = PointsManager(graph_manager)
        self.graph_manager = graph_manager

    def set_first_points_busy(self, points):
        self.points_manager.set_first_points_busy(points)

    def update_fixed_places_arrived_time(self, fixed_point, path):
        if path != False:
            self.points_manager.update_fixed_places_arrived_time(
                fixed_point, len(path) - 1)

    def move_fixed_point(self, time, path_array, fixed_point):
        return self.points_manager.move_fixed_point(time, path_array, fixed_point)

    def get_collision_fixed_point(self, point, time, agent_id):
        return self.points_manager.get_collision_fixed_point(point, time, agent_id)

    def build_fixed_places(self, to_points, from_points):
        self.points_manager.build_fixed_places(to_points, from_points)

    def random_point(self):
        return self.graph_manager.random_point()

    def remove_busy(self, points):
        self.points_manager.remove_busy(points)

    def get_original_path_length(self, from_point, to_point):
        return self.graph_manager.get_original_path_length(from_point, to_point)

    def update_busy(self, path):
        if path != False:
            self.points_manager.update_busy(path)

    def set_all_busy(self, max_time):
        self.points_manager.set_all_busy(
            max_time, self.graph_manager.matrix_cube_size[0], self.graph_manager.matrix_cube_size[1],
            self.graph_manager.matrix_cube_size[2])

    def get_path(self, from_point, to_point, check_fixed_collision, wait_time, agent_id):
        if from_point == to_point:
            return [(0, from_point.x, from_point.y, from_point.z)]
        can_stay = wait_time > 0
        visited_points = set()
        visited_points_in_time_unit = set()
        path_step_stack = list(
            [PointVertex(None, from_point, (0, from_point.x, from_point.y, from_point.z))])
        path = list()
        time = 0
        while (len(path_step_stack) > 0):
            vertex_point = path_step_stack.pop()
            time_point = vertex_point.time_point
            time = time_point[0]
            step = vertex_point.point

            if not check_fixed_collision:
                visited_points_in_time_unit.add(time_point)
                if self.points_manager.is_time_unit_busy(time_point):
                    continue

            if step == to_point:

                pointer = vertex_point
                while (True):
                    path.append(pointer.time_point)
                    if pointer.parent is None:
                        break
                    pointer = pointer.parent

                path.reverse()
                return path

            visited_points.add(step.to_tuple())

            steps = self.graph_manager.get_steps_to_destination(
                step, to_point, can_stay)

            steps_filtered = list()
            for s in steps:

                if self.points_manager.is_first_point_busy(time + 1, s.to_tuple(), agent_id):
                    continue

                if check_fixed_collision:
                    if not can_stay:
                        if s.to_tuple() in visited_points:
                            continue

                    if can_stay:
                        if s.to_tuple() in visited_points and not (
                                s == step and not self.check_wait_time(vertex_point, wait_time)):
                            continue

                    if self.points_manager.is_fixed_point_busy(time + 1, s.to_tuple(), agent_id):
                        continue

                    if self.points_manager.is_time_unit_busy((time + 1, s.x, s.y, s.z)):
                        continue
                else:
                    if (time + 1, s.x, s.y, s.z) in visited_points_in_time_unit:
                        continue
                    if can_stay and self.check_wait_time(vertex_point, wait_time):
                        continue

                steps_filtered.append(PointVertex(
                    vertex_point, s, (time + 1, s.x, s.y, s.z)))

            path_step_stack.extend(steps_filtered)

        return False

    def check_wait_time(self, point_vertex, time):
        same_point = 0
        current_point = point_vertex
        for i in range(0, time):
            if current_point.parent is not None and current_point.parent.point == current_point.point:
                same_point += 1
            if current_point.parent is not None:
                current_point = current_point.parent
            else:
                break
        return time == same_point


class PointsManager:
    def __init__(self, graph_manager):
        self.graph_manager = graph_manager
        self.time_unit_busy = set()
        self.from_points = {}
        self.fixed_points = {}
        self.fixed_around_points = {}

    def update_fixed_places_arrived_time(self, fixed_point, time):
        self.fixed_points[fixed_point.to_tuple()].arrived_time = time

    def move_fixed_point(self, time, path_array, fixed_point):
        return fixed_point.move_free_place(time, path_array, fixed_point, self)

    def get_collision_fixed_point(self, point, time, agent_id):
        fixed_point = None
        if point.to_tuple() in self.fixed_points:
            p = self.fixed_points[point.to_tuple()]
            if p.agent_id != agent_id:
                if p.arrived_time == -1 or time >= p.arrived_time + 3:
                    fixed_point = p
        return fixed_point

    def build_fixed_places(self, points, from_points):
        # TODO important add that if a fixed point have shared around points with other fixed, then keep the first or who have the less
        # check how to do all permutations that everyone have at least 3 places
        for p in from_points:
            self.from_points[p[1].to_tuple()] = p[0]
        list_of_fixed = list()
        fixed_points = set(p[1].to_tuple() for p in points)
        for fp in points:
            around_points = self.graph_manager.get_around_points(fp[1])
            # TODO allow to keep fix point and move also the second fixed
            around_points = list(
                filter(lambda a: a.to_tuple() not in fixed_points, around_points))
            around_points_list = list()
            for ap in around_points:
                around_fixed_point = AroundFixedPoint(ap)
                around_points_list.append(around_fixed_point)
            fix_point = FixedPoint(fp[0], fp[1], around_points_list)
            list_of_fixed.append(fix_point)

        # sort by original around points
        def fixed_points_order_key(a):
            return len(a.around_points_list)

        # remove shared around points
        list_of_fixed.sort(key=fixed_points_order_key, reverse=False)
        all_around_points = set()
        for fp in list_of_fixed:
            for ap in fp.around_points_list:
                if ap.point.to_tuple() in all_around_points:
                    ap.belongs_to_other_fixed = True
                else:
                    all_around_points.add(ap.point.to_tuple())

        for fp in list_of_fixed:
            fp.around_points_list = list(
                filter(lambda a: a.belongs_to_other_fixed == False, fp.around_points_list))

        list_of_fixed.sort(key=fixed_points_order_key, reverse=False)

        for fp in list_of_fixed:
            self.fixed_points[fp.point.to_tuple()] = fp
            for ap in fp.around_points_list:
                self.fixed_around_points[ap.point.to_tuple()] = ap

    def remove_busy(self, points):
        if points != False:
            for p in points:
                self.time_unit_busy.discard(p)

    def set_all_busy(self, max_time, max_x, max_y, max_z):
        for t in range(1, max_time):
            for x in range(0, max_x):
                for y in range(0, max_y):
                    for z in range(0, max_z):
                        time_point_vector = (t, x, y, z)
                        self.time_unit_busy.add(time_point_vector)

    def set_first_points_busy(self, points):
        for p in points:
            time_point_vector = (0, p.x, p.y, p.z)
            self.time_unit_busy.add(time_point_vector)

    def update_busy(self, path):
        if (path is not False):
            for i in range(0, len(path)):
                # add time_unit_busy in the fixed around fields
                self.time_unit_busy.add(path[i])
                '''
                if i > 0:
                    time_point_vector = (
                        path[i][0], path[i-1][1], path[i-1][2], path[i-1][3])
                    self.time_unit_busy.add(time_point_vector)
                    '''
            last_time = path[len(path) - 1][0]
            for i in range(1, 3):
                time_point_vector = (
                    last_time + i, path[last_time][1], path[last_time][2], path[last_time][3])
                self.time_unit_busy.add(time_point_vector)

    def is_first_point_busy(self, time, point, agent_id):
        if time == 1:
            if point in self.from_points:
                if self.from_points[point] != agent_id:
                    return True
        return False

    def is_fixed_point_busy(self, time, point, agent_id):
        if point in self.fixed_points:
            if self.fixed_points[point].agent_id != agent_id:
                if self.fixed_points[point].arrived_time == -1 or time >= self.fixed_points[point].arrived_time - 1:
                    return True
        return False

    def is_time_unit_busy(self, time_unit_point):
        if time_unit_point[0] > 0:
            prev_time = (time_unit_point[0] - 1, time_unit_point[1], time_unit_point[2], time_unit_point[3])

            if prev_time in self.time_unit_busy:
                return True

        next_time = (time_unit_point[0] + 1, time_unit_point[1], time_unit_point[2], time_unit_point[3])
        if next_time in self.time_unit_busy:
            return True

        return time_unit_point in self.time_unit_busy


class FixedPoint:
    def __init__(self, agent_id, point, around_points_list):
        self.agent_id = agent_id
        self.point = point
        self.time_moved = set()
        self.around_points_list = around_points_list
        for ap in self.around_points_list:
            ap.set_fixed_point(self)
        self.arrived_time = -1

    def set_arrived_time(self, arrived_time):
        self.arrived_time = arrived_time

    def fixed_moved_set(self, time):
        for i in range(time - 6, time + 5):
            self.time_moved.add(i)

    def move_free_place(self, time, path_array, fixed_point, points_manager):
        move_point = None
        path = False
        if time in self.time_moved:
            return False
        for p in self.around_points_list:
            if not p.is_busy(time, points_manager):
                move_point = p
                break
        if move_point is not None:
            path = move_point.choose_moving_point(time, deepcopy(path_array), points_manager)
        return path


class AroundFixedPoint:
    def __init__(self, point):
        self.point = point
        self.belongs_to_other_fixed = False

    def set_fixed_point(self, fixed_point):
        self.fixed_point = fixed_point

    # define if the fixed point can move to this free points or not
    def is_busy(self, time, points_manager):
        available = True
        for t in range(time - 1, time + 3):
            if points_manager.is_time_unit_busy((t, self.point.x, self.point.y, self.point.z)):
                available = False
                break
        return not available

    # move the fixed drone to this point to let another drone use the place
    # check if we can move again if another drone have a collision
    def choose_moving_point(self, time, path_array, points_manager):
        # check that the path is really updated
        last_time_point = path_array[len(path_array) - 1]
        last_point = (last_time_point[1],
                      last_time_point[2], last_time_point[3])
        original_length = len(path_array)
        for i in range(original_length, time + 3):
            path_array.append(
                (i, last_time_point[1], last_time_point[2], last_time_point[3]))

        prev_place = path_array[time]
        path_array[time - 1] = (time - 1, self.point.x,
                                self.point.y, self.point.z)
        path_array[time] = (time, self.point.x, self.point.y, self.point.z)
        path_array[time + 1] = (time + 1, self.point.x,
                                self.point.y, self.point.z)
        path_array[time + 2] = prev_place
        return path_array


class PointVertex:
    def __init__(self, parent, point, time_point):
        self.parent = parent
        self.point = point
        self.time_point = time_point


class TestManager:
    def __init__(self):
        pass

    def check_path_deviation(self, agents):
        count_path = sum(
            1 if a.path is not False else 0 for a in agents)
        sum_path_length = sum(
            len(a.path) if a.path is not False else 0 for a in agents)
        sum_original_path_length = sum(
            a.original_path_length if a.path is not False else 0 for a in agents)
        print("sum_path_length:", sum_path_length)
        print("sum_original_path_length:", sum_original_path_length)
        print("sum difference:", sum_path_length - sum_original_path_length)

        max_path_length = max(
            len(a.path) if a.path is not False else 0 for a in agents)
        max_original_path_length = max(
            a.original_path_length if a.path is not False else 0 for a in agents)
        print("max_path_length:", max_path_length)
        print("max_original_path_length:", max_original_path_length)
        print("max difference:", max_path_length - max_original_path_length)
        # return (sum_path_length - sum_original_path_length)/count_path
        return max_path_length - max_original_path_length

    def check_collision(self, p_list, points_manager):
        path_list = deepcopy(p_list)
        max_path_length = max(
            len(x) if x is not False else 0 for x in path_list)
        for path in path_list:
            if path != False:
                time_unit = path[len(path) - 1]
                for i in range(len(path), max_path_length):
                    new_time_unit = (
                        i, time_unit[1], time_unit[2], time_unit[3])
                    path.append(new_time_unit)
            # print("max_path_length:", max_path_length)
            # print("path:", path)
        collision_path_counter = 0
        collision_counter = 0
        time_units = {}
        path_id = 0
        for path in path_list:
            path_id += 1
            collision = 0
            for i in range(0, max_path_length):
                if path == False:
                    continue
                collision_agent = False
                if path[i] in time_units and time_units[path[i]] != path_id:
                    collision_agent = time_units[path[i]]
                if (path[i][0] - 1, path[i][1], path[i][2], path[i][3]) in time_units and time_units[
                    (path[i][0] - 1, path[i][1], path[i][2], path[i][3])] != path_id:
                    collision_agent = time_units[(path[i][0] - 1, path[i][1], path[i][2], path[i][3])]
                if (path[i][0] + 1, path[i][1], path[i][2], path[i][3]) in time_units and time_units[
                    path[i][0] + 1, path[i][1], path[i][2], path[i][3]] != path_id:
                    collision_agent = time_units[(path[i][0] + 1, path[i][1], path[i][2], path[i][3])]
                # assert (path[i] in time_units) == False
                if collision_agent is not False:
                    print("time_units[path[i]]  -1 ]:", collision_agent)
                    print("path:", path)
                    print("path collision:", path_list[collision_agent])
                    print("path[i]:", path[i])
                    collision += 1
                else:
                    '''
                    if i > 0:
                        time_units[(path[i][0], path[i-1][1],
                                    path[i-1][2], path[i-1][3])] = path_id
                    '''
                    time_units[path[i]] = path_id
            if collision > 0:
                collision_counter += collision
                collision_path_counter += 1
        print("collision_counter:", collision_counter)
        print("collision_path_counter:", collision_path_counter)
        return collision_counter

    def run_case(self, agent_manager, drones_count):
        random_points = agent_manager.get_random_agents(drones_count)
        agent_manager.create_agents(random_points)
        path_list = agent_manager.get_agents_path_list()
        # print(path_list)
        return path_list

    def run_cases(self, drones_count, cases_num):
        case_error = 0
        case_move_error = 0
        total_case_error = 0
        total_deviation = 0
        total_collision = 0
        case_success_move = 0
        graph_manager = GraphManager((23, 23, 23))
        for j in range(0, cases_num):
            # print("j:", j)
            path_manager = PathManager(graph_manager)
            agent_manager = AgentManager(path_manager)
            before_time = datetime.now()
            # print("before_time:", before_time)
            path_list = self.run_case(agent_manager, drones_count)
            for path in path_list:
                if not path:
                    print("kaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            total_collision += self.check_collision(path_list, path_manager.points_manager)
            total_deviation += self.check_path_deviation(agent_manager.agents)
            after_time = datetime.now()
            # print("after_time:", after_time)
            # print("diff_time:", after_time - before_time)
            if agent_manager.path_error_counter > 0 or agent_manager.cannot_move_fixed_error_counter > 0:
                total_case_error += 1
            case_success_move += agent_manager.success_move
            case_error += agent_manager.path_error_counter
            case_move_error += agent_manager.cannot_move_fixed_error_counter


        print("------------all cases--------------------")
        print("average total_deviation:", total_deviation / cases_num)
        print("total_collision:", total_collision)
        print("total_case_error:", total_case_error)
        print("case_error:", case_error)
        print("case_move_error:", case_move_error)
        print("case_success_move:", case_success_move)


#test_manager = TestManager()
# test_manager.run_maze()
# test_manager.run_maze_2()
# test_manager.run_maze_3()
# test_manager.run_maze_4()
# for i in range(10, 101, 10):
#     test_manager.run_cases(i, 100)
# run_cases(200, 1)
