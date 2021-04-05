import math
import test_dashboard

def convert_input(agents_start_pos, agents_goal_pos, height, length, width, dron_radius, security_distance):
    start_pos_list = []
    goal_pos_list = []
    for agent in agents_start_pos:
        start_pos_list.append(agents_start_pos[agent][0])
    for agent in agents_goal_pos:
        goal_pos_list.append(agents_goal_pos[agent][0])

    agents_pos = []
    for start_pos, goal_pos in zip(start_pos_list, goal_pos_list):
        start_pos = convert_point(start_pos, height, length, width, dron_radius, security_distance, 1)
        goal_pos = convert_point(goal_pos, height, length, width, dron_radius, security_distance, 1)
        agents_pos.append(start_pos + goal_pos)
    return agents_pos

def convert_point(point, height, length, width, dron_radius, security_distance, input = 0):
    convert_point = []
    if input:
        convert_point.append(convert_coordinate_input(point[0], width, dron_radius, security_distance))
        convert_point.append(convert_coordinate_input(point[1], length, dron_radius, security_distance))
        convert_point.append(convert_coordinate_input(point[2], height, dron_radius, security_distance, 1))
    else:
        convert_point.append(convert_coordinate_output(point[0], width, dron_radius, security_distance))
        convert_point.append(convert_coordinate_output(point[1], length, dron_radius, security_distance))
        convert_point.append(convert_coordinate_output(point[2], height, dron_radius, security_distance, 1))
    return tuple(convert_point)

def convert_coordinate_input(coordinate, length, dron_radius, security_distance, z_coordinate=0):
    if z_coordinate:
        return int(coordinate / (100 * (dron_radius * 2 + security_distance)))
    return int((coordinate + length * 100 / 2) / (100 * (dron_radius * 2 + security_distance)))

def convert_coordinate_output(coordinate, length, dron_radius, security_distance, z_coordinate=0):
    if z_coordinate:
        return int(coordinate * (100 * (dron_radius * 2 + security_distance)) + (100 * (dron_radius * 2 + security_distance)) / 2)
    return int((coordinate * (100 * (dron_radius * 2 + security_distance))) - (length * 100) / 2 + (100 * (dron_radius * 2 + security_distance)) / 2)

def convert_output(paths, agents_start_pos, agents_goal_pos, height, length, width, dron_radius, security_distance):
    convert_path = []
    convert_paths = {}
    i = 0

    # convert the path to the right unit
    for agent in paths:
        agent_id = "D" + str("%03d" % (agent - 1))
        for step in paths[agent]:
            convert_path.append(convert_point(step, height, length, width, dron_radius, security_distance))
        print("before ", convert_path)
        convert_path = add_point_to_path(convert_path, dron_radius, security_distance)
        convert_path.insert(0, agents_start_pos[agent_id][0])
        convert_path.append(agents_goal_pos[agent_id][0])
        convert_paths[agent_id] = convert_path
        convert_path = []
        i += 1

    return convert_paths

def add_point_to_path(path, dron_radius, security_distance):

    additional_points = []
    k = 0
    distance = (dron_radius * 2 + security_distance) * 100
    convert_path =[]
    for index in range(1, len(path)):
        if index != 2:                     # in case we already add 3 steps, Add to the list instead of the index and more 4
            k = 4
        if path[index] == path[index - 1]:  # In case this step passes the same point, add the same point 3 times
            for i in range(5):
                convert_path.append(path[index - 1])
            print("stay in placeeeeeee")
            continue
        for coordinate in range(3):     # Check which coordinate has changed and add 3 steps
            if path[index][coordinate] > path[index - 1][coordinate]:
                convert_path.append(path[index - 1])
                for i in range(1, 4):
                    step = list(path[index - 1])
                    step[coordinate] += int(distance/4) * i
                    convert_path.append(tuple(step))
                convert_path.append(path[index])
                print("move up")

            elif path[index][coordinate] < path[index - 1][coordinate]:
                convert_path.append(path[index - 1])
                for i in range(1, 4):
                    step = list(path[index - 1])
                    step[coordinate] -= int(distance / 4) * i
                    convert_path.append(tuple(step))
                convert_path.append(path[index])
                print("move up")

    return convert_path
agents_start_pos = {'D000': [(-937, -749, 6000)], 'D001': [(-156, -124, 8400)], 'D002': [(-312, -249, 8800)], 'D003': [(546, 437, 8800)], 'D004': [(937, 749, 8700)], 'D005':[(1484, 1186, 9200)], 'D006': [(-1405, -1124, 7800)], 'D007': [(-937, -749, 9200)], 'D008': [(-468, -374, 9200)], 'D009': [(0, 0, 9200)], 'D010': [(468, 374, 9200)], 'D011': [(937, 749, 9200)], 'D012': [(1484, 1186, 8500)], 'D013': [(-1171, -936, 6600)], 'D014': [(-1484, -1186, 9200)], 'D015': [(-1484, -1186,8500)], 'D016': [(468, 374, 8300)], 'D017': [(390, 312, 7200)], 'D018': [(390, 312, 6600)], 'D019': [(1327, 1061, 7200)], 'D020': [(-78, -62, 6000)], 'D021': [(-624, -499, 5400)], 'D022': [(0, 0, 5000)], 'D023': [(0, 0, 6500)], 'D024': [(312, 249, 6100)], 'D025': [(1405, 1124, 7800)], 'D026': [(1171, 936, 6600)], 'D027': [(-1327, -1061, 7200)], 'D028': [(-702, -562, 8800)], 'D029': [(-546, -437, 8300)], 'D030': [(-156, -124, 5500)], 'D031': [(156, 124, 8100)],'D032': [(781, 624, 8100)], 'D033': [(937, 749, 6000)], 'D034': [(-234, -187, 7900)], 'D035': [(0, 0, 7500)], 'D036': [(0, 0, 7000)], 'D037': [(234, 187,5500)], 'D038': [(468, 374, 7700)], 'D039': [(624, 499, 5400)]}
agents_goal_pos = {'D000': [(-1272, -862, 7000)], 'D001': [(-1272, -862, 8500)], 'D002': [(-1272, -862, 9000)], 'D003': [(41, 28, 9726)], 'D004': [(455, 308, 9426)], 'D005':[(1779, 1206, 9000)], 'D006': [(-2317, -1571, 7550)], 'D007': [(-1686, -1143, 9200)], 'D008': [(-1272, -862, 9600)], 'D009': [(-455, -308, 8992)], 'D010':[(-372, -252, 9626)], 'D011': [(1365, 926, 9000)], 'D012': [(2027, 1375, 8500)], 'D013': [(-2317, -1571, 6650)], 'D014': [(-2482, -1683, 8700)], 'D015': [(-2400, -1627, 9200)], 'D016': [(455, 308, 8892)], 'D017': [(1117, 757, 7500)], 'D018': [(455, 308, 7292)], 'D019': [(2027, 1375, 7500)], 'D020': [(-372, -252, 6592)], 'D021': [(-1407, -954, 5800)], 'D022': [(41, 28, 6492)], 'D023': [(-455, -308, 7192)], 'D024': [(455, 308, 6792)], 'D025': [(2027, 1375, 8000)], 'D026': [(2027, 1375, 7000)], 'D027': [(-2317, -1571, 7100)], 'D028': [(-1272, -862, 8000)], 'D029': [(-1272, -862, 7500)], 'D030': [(-1272, -862, 6500)], 'D031': [(455, 308, 8392)], 'D032': [(1117, 757, 8500)], 'D033': [(1779, 1206, 6500)], 'D034': [(-206, -140, 8092)], 'D035': [(206, 140, 8092)], 'D036':[(455, 308, 7792)], 'D037': [(1365, 926, 6500)], 'D038': [(1117, 757, 8000)], 'D039': [(1117, 757, 7000)]}
agents_pos = convert_input(agents_start_pos, agents_goal_pos, 100, 100, 100, 0.25, 4)
paths = test_dashboard.run_algorithm_1_with_specific_example(100, 100, 100, 0.25, 4, agents_pos)
print(convert_output(paths, agents_start_pos, agents_goal_pos, 100, 100, 100, 0.25, 4))

