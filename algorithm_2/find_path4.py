import math_graph
import random
from math_graph import Point3D
from datetime import datetime

'''
if make normal path then if we block with fixed move the fixed else wait order by time waiting if the fixed cannot move
then solve the collision of the other to wait to this drone

or solve with normal fixed oject with all the end poitn then on colisino with moving just wait

put the firxt point on the busy also for th eprev of the next point
try to create the cude to 10 part and calculte fixed path for the all 10 part and all the drones path are fixed in there
TODO
add vector fixed busy and without time check set it visited
bug set prev step busy
set prev busy for the first step
write coments
order by max path
priority to step
check deviation with normal path
if the path is not norma and too big in the 2 options then run a third slow algorithm with breadth search instead of depth search
m

''' 

def get_next_possible_steps(matrix_cube_size, fix_busy, time_unit_busy, current_point, to_point, current_time_unit):
    available_steps = list()
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

    available_steps_filtered = list()
    for s in available_steps:
        if s.x >= matrix_cube_size[0] or s.x < 0:
            continue
        if s.y >= matrix_cube_size[1] or s.y < 0:
            continue
        if s.z >= matrix_cube_size[0] or s.z < 0:
            continue

        available_steps_filtered.append(s)

    return available_steps_filtered


def find_path_specific_drone(matrix_cube_size, fix_busy, time_unit_busy, from_point, to_point):
    if from_point == to_point:
        return [(0, from_point.x, from_point.y, from_point.z)]

    visited_points_in_time_unit = set()
    visited_points_fixed = set()

    path_step_stack = list([from_point])
    path = list()
    time = 0
    while(len(path_step_stack) > 0):
        step = path_step_stack.pop()
       
        time_point = (time, step.x, step.y, step.z)

        if step == to_point:
            time += 1
            path.append(time_point)
            return path
       
        if (step.x, step.y, step.z) in visited_points_fixed:
            continue

        if time_point in visited_points_in_time_unit:
            continue

        visited_points_in_time_unit.add(time_point)

        steps = get_next_possible_steps(matrix_cube_size, fix_busy, time_unit_busy, step, to_point, time + 1)
        
        steps_filtered = list()
        meet_busy = False
        for s in steps:
            
            if (s.x, s.y, s.z) in fix_busy:
                meet_busy = True
                continue
            if (time + 1, s.x, s.y, s.z) in time_unit_busy:
                continue
            if (s.x, s.y, s.z) in visited_points_fixed:
                continue
            if (time + 1, s.x, s.y, s.z) in visited_points_in_time_unit:
                continue
            steps_filtered.append(s)
            
        steps_filtered.reverse()

        if meet_busy == True:
           visited_points_fixed.add((step.x, step.y, step.z))   

        #for s in steps:
        #    print(s.to_string())
        if len(steps_filtered) > 0:
            time += 1
            path.append(time_point)

        path_step_stack.extend(steps_filtered)

    return False



today = datetime.now()
print("Today's date:", today)

def run_maze():
    matrix_cube_size = (3, 3, 3)
    time_unit_busy = set()
    fix_busy = set()
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
    path = find_path_specific_drone(matrix_cube_size, fix_busy, time_unit_busy, from_point, to_point)
    
    print(path)


def run_cases(drones_count, cases_num):    
    #matrix_cube_size = (100, 100, 60)
    matrix_cube_size = (8, 8, 6)                  
    case_error = 0
    for j in range(0, cases_num):
        count = 0
        path_list = []
        time_unit_busy = set()
        fix_busy = set()
        before_time = datetime.now()
        print("before_time:", before_time)
        for i in range(0, drones_count):
            from_point = Point3D(random.randint(0,7), random.randint(0,7), random.randint(0,5))
            to_point = Point3D(random.randint(0,7), random.randint(0,7), random.randint(0,5))
            path = find_path_specific_drone(matrix_cube_size, fix_busy,
            time_unit_busy, from_point, to_point)
            print("from_point", from_point)
            print("to_point", to_point)
            print("path_list", path)
            path_list.append(path)

            if path == False:
                pass
                #print("time_unit_busy:", time_unit_busy)
                #print("from_point", from_point, to_point)
            else:
                count += 1

            if path != False:
                for i in range(0, len(path)):
                    time_unit_busy.add(path[i])
                    if i > 0:
                        time_point_vector = (path[i][0], path[i-1][1], path[i-1][2], path[i-1][3])
                        time_unit_busy.add(time_point_vector)
                last_time = path[len(path) - 1][0]
                #print("last_time", last_time)
                time_point_vector = path[len(path) - 1]
                fix_busy.add((to_point.x, to_point.y, to_point.z))
                #for i in range(last_time, last_time + 1000):
                #    time_point_vector = (i, path[len(path) - 1][1], path[len(path) - 1][2], path[len(path) - 1][3])
                #    time_unit_busy.add(time_point_vector)

        after_time = datetime.now()
        print("after_time:", after_time)

        if count != drones_count:
            case_error += 1
            print("count", count)

    print("case_error", case_error)

'''
for t in time_unit_busy:
    if t[0] > 1000:
        print("found")

for i in range(0, len(path_list)):
    path_i = path_list[i]
    for j in range(i + 1, len(path_list)):
        path_j = path_list[j]
        for pi in range(0, len(path_i)):
            for pj in range(0, len(path_j)):
                if path_i[pi] == path_j[pj]: 
                    print("same point", path_i[pi], path_j[pj])

'''

#run_maze()
run_cases(50, 1)
