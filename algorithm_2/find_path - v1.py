import math_graph
import random
from math_graph import Point3D
from datetime import datetime

'''
TODO
if we have regular just make it moving and not block all
try to move another drone if we cannot find solution or remove from the list this drone and then try again
add vector fixed busy and without time check set it visited
bug set prev step busy
set prev busy for the first step
write coments
order by max path
priority to step
check deviation with normal path
if the path is not norma and too big in the 2 options then run a third slow algorithm with breadth search instead of depth search
need to add to move the fixed on collision
'''


class FixedPoint:
    def __init__(self, point):
        self.point = point


class AroundFixedPoint:
    def __init__(self, point, fixed_point):
        self.fixed_point = fixed_point
        self.point = point


class PointVertex:
    def __init__(self, parent, time_point):
        self.parent = parent
        self.time_point = time_point


def get_next_possible_steps(matrix_cube_size, time_unit_busy, current_point, to_point, current_time_unit, can_stay):
    available_steps = list()
    d_z = current_point.z > to_point.z if current_point.z - 1 else current_point.z + 1
    b_z = current_point.z < to_point.z if current_point.z - 1 else current_point.z + 1
    s_z = current_point.z

    d_y = current_point.z > to_point.z if current_point.z - 1 else current_point.z + 1
    b_x = current_point.z < to_point.z if current_point.z - 1 else current_point.z + 1
    s_x = current_point.x

    # put the direction points
    if(current_point.z > to_point.z):
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y, current_point.z - 1))
    elif current_point.z < to_point.z:
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y, current_point.z + 1))
    if(current_point.y > to_point.y):
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y - 1, current_point.z))
    elif current_point.y < to_point.y:
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y + 1, current_point.z))
    if(current_point.x > to_point.x):
        available_steps.append(math_graph.Point3D(
            current_point.x - 1, current_point.y, current_point.z))
    elif current_point.x < to_point.x:
        available_steps.append(math_graph.Point3D(
            current_point.x + 1, current_point.y, current_point.z))

    if not can_stay:
        # put the back direction points , add order go back if firsst direction
        if(current_point.z < to_point.z):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z - 1))
        elif current_point.z > to_point.z:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z + 1))
        if(current_point.y < to_point.y):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y - 1, current_point.z))
        elif current_point.y > to_point.y:
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y + 1, current_point.z))
        if(current_point.x < to_point.x):
            available_steps.append(math_graph.Point3D(
                current_point.x - 1, current_point.y, current_point.z))
        elif current_point.x > to_point.x:
            available_steps.append(math_graph.Point3D(
                current_point.x + 1, current_point.y, current_point.z))

    # put the moving from place points
    if not can_stay:
        if(current_point.z == to_point.z):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z - 1))
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y, current_point.z + 1))
        if(current_point.y == to_point.y):
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y - 1, current_point.z))
            available_steps.append(math_graph.Point3D(
                current_point.x, current_point.y + 1, current_point.z))
        if(current_point.x == to_point.x):
            available_steps.append(math_graph.Point3D(
                current_point.x - 1, current_point.y, current_point.z))
            available_steps.append(math_graph.Point3D(
                current_point.x + 1, current_point.y, current_point.z))

    if can_stay:
        available_steps.append(math_graph.Point3D(
            current_point.x, current_point.y, current_point.z))

    available_steps_filtered = list()
    for s in available_steps:
        if s.x >= matrix_cube_size[0] or s.x < 0:
            continue
        if s.y >= matrix_cube_size[1] or s.y < 0:
            continue
        if s.z >= matrix_cube_size[0] or s.z < 0:
            continue
        if (current_time_unit, s.x, s.y, s.z) in time_unit_busy:
            continue

        available_steps_filtered.append(s)

    available_steps_filtered.reverse()
    return available_steps_filtered


def find_path_specific_drone(matrix_cube_size, time_unit_busy, from_point, to_point, can_stay):
    if from_point == to_point:
        return [(0, from_point.x, from_point.y, from_point.z)]

    visited_points_in_time_unit = set()
    path_step_stack = list(
        [PointVertex(None, (0, from_point.x, from_point.y, from_point.z))])
    path = list()
    time = 0
    while(len(path_step_stack) > 0):
        vertex_point = path_step_stack.pop()
        time_point = vertex_point.time_point
        time = time_point[0]
        step = Point3D(time_point[1], time_point[2], time_point[3])
        if step == to_point:
            pointer = vertex_point
            while(True):
                path.append(pointer.time_point)
                pointer = pointer.parent
                if pointer.parent is None:
                    break
            path.reverse()
            return path

        if time_point in visited_points_in_time_unit:
            continue

        visited_points_in_time_unit.add(time_point)

        steps = get_next_possible_steps(
            matrix_cube_size, time_unit_busy, step, to_point, time + 1, can_stay)

        steps_filtered = list()
        for s in steps:
            if (time + 1, s.x, s.y, s.z) in visited_points_in_time_unit:
                continue
            steps_filtered.append(PointVertex(
                vertex_point, (time + 1, s.x, s.y, s.z)))

        path_step_stack.extend(steps_filtered)

    return False


today = datetime.now()
print("Today's date:", today)


def run_maze():
    matrix_cube_size = (3, 3, 3)
    time_unit_busy = set()
    for t in range(1, 50):
        for x in range(0, matrix_cube_size[0]):
            for y in range(0, matrix_cube_size[1]):
                for z in range(0, matrix_cube_size[2]):
                    time_point_vector = (t, x, y, z)
                    time_unit_busy.add(time_point_vector)
    print((1, 1, 0, 0) in time_unit_busy)
    time_unit_busy.remove((1, 1, 0, 0))
    print((1, 1, 0, 0) in time_unit_busy)
    time_unit_busy.remove((2, 0, 0, 0))
    time_unit_busy.remove((3, 0, 1, 0))
    time_unit_busy.remove((4, 0, 1, 1))
    time_unit_busy.remove((5, 0, 1, 2))
    from_point = Point3D(1, 1, 0)
    to_point = Point3D(0, 1, 2)
    path = find_path_specific_drone(
        matrix_cube_size, time_unit_busy, from_point, to_point, False)

    print(path)


def run_maze_2():
    matrix_cube_size = (3, 3, 3)
    time_unit_busy = set()
    for t in range(1, 50):
        for x in range(0, matrix_cube_size[0]):
            for y in range(0, matrix_cube_size[1]):
                for z in range(0, matrix_cube_size[2]):
                    time_point_vector = (t, x, y, z)
                    time_unit_busy.add(time_point_vector)
    time_unit_busy.remove((1, 1, 0, 0))
    time_unit_busy.remove((2, 1, 0, 1))
    print((2, 1, 0, 1) in time_unit_busy)
    time_unit_busy.remove((3, 1, 0, 2))
    time_unit_busy.remove((2, 0, 0, 0))
    time_unit_busy.remove((3, 0, 1, 0))
    time_unit_busy.remove((4, 0, 1, 1))
    time_unit_busy.remove((5, 0, 1, 2))
    from_point = Point3D(1, 1, 0)
    to_point = Point3D(0, 1, 2)
    path = find_path_specific_drone(
        matrix_cube_size, time_unit_busy, from_point, to_point, False)

    print(path)


def run_cases(drones_count, cases_num):
    #matrix_cube_size = (100, 100, 60)
    matrix_cube_size = (8, 8, 6)
    case_error = 0
    case_fix_buzy_error = 0
    case_stay_error = 0
    for j in range(0, cases_num):
        error_count = 0
        error_stay_count = 0
        path_list = []
        time_unit_busy = set()
        fix_busy = {}
        before_time = datetime.now()
        print("before_time:", before_time)
        for i in range(0, drones_count):

            from_point = Point3D(random.randint(
                0, 7), random.randint(0, 7), random.randint(0, 5))
            print("from_point:", from_point)
            if (0, from_point.x, from_point.y, from_point.z) in time_unit_busy:
                print("invalid from point ", from_point)
                continue
            to_point = Point3D(random.randint(
                0, 7), random.randint(0, 7), random.randint(0, 5))
            if (to_point.x, to_point.y, to_point.z) in fix_busy:
                print("invalid to point; ", to_point)
                continue
            path = find_path_specific_drone(matrix_cube_size,
                                            time_unit_busy, from_point, to_point, False)
            #print("from_point", from_point)
            #print("to_point", to_point)
            #print("path_list", path)

            stay = False
            if path == False:
                error_count += 1
                stay = True
                print("move", path)
                path = find_path_specific_drone(matrix_cube_size,
                                                time_unit_busy, from_point, to_point, True)

            if path == False:
                if stay:
                    error_stay_count += 1
                print("stay", path)
                pass
                #print("time_unit_busy:", time_unit_busy)
                #print("from_point", from_point, to_point)
            else:
                if stay:
                    print("stay success", path)
                path_list.append(path)

            if path != False:
                for i in range(0, len(path)):
                    # add time_unit_busy in the fixed around fields
                    time_unit_busy.add(path[i])
                    if i > 0:
                        time_point_vector = (
                            path[i][0], path[i-1][1], path[i-1][2], path[i-1][3])
                        time_unit_busy.add(time_point_vector)
                last_time = path[len(path) - 1][0]
                #print("last_time", last_time)
                time_point_vector = path[len(path) - 1]
                print("path", path)
                for p in path:
                    if (p[1], p[2], p[3]) in fix_busy:
                        if (p[0] >= fix_busy[(p[1], p[2], p[3])][0]):
                            case_fix_buzy_error += 1

                fix_busy[(to_point.x, to_point.y, to_point.z)
                         ] = time_point_vector
                # for i in range(last_time, last_time + 1000):
                #    time_point_vector = (i, path[len(path) - 1][1], path[len(path) - 1][2], path[len(path) - 1][3])
                #    time_unit_busy.add(time_point_vector)
        # for all the drones path if in fixed drone then get one point around that available from the prev time
        # current time and 2 next time total of 4 unit time and change the place of this drone
        after_time = datetime.now()
        print("after_time:", after_time)
        print("diff_time:", after_time - before_time)
        if error_count != drones_count:
            case_error += error_count
            case_stay_error += error_stay_count
            print("error_stay_count", error_stay_count)
            print("count", error_count)
        ''' 
        for i in range(0, len(path_list)):
            path_i = path_list[i]
            for j in range(i + 1, len(path_list)):
                path_j = path_list[j]
                for pi in range(0, len(path_i)):
                    for pj in range(0, len(path_j)):
                        #print(path_j)
                        if path_i[pi] == path_j[pj]:
                            print ("path_i", path_i)
                            print ("path_j", path_j)
                            print("time_unit_busy", path_i[pi] in time_unit_busy)  
                            print("same point", path_i[pi], path_j[pj])
           '''
    print("case_error", case_error)
    print("case_stay_error", case_stay_error)
    print("case_fix_buzy_error", case_fix_buzy_error)


'''
for t in time_unit_busy:
    if t[0] > 1000:
        print("found")
'''

# run_maze()
# run_maze_2()
run_cases(100, 1000)
