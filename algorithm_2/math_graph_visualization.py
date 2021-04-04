import math
import math_graph
from math_graph import Point
from math_graph import Point3D
import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D

graph = math_graph.TwoDGraph()
graph3d = math_graph.ThreeDGraph()


def draw_points_z_in_radius_of_path(from_point: Point3D, to_point: Point3D, radius):
    fig = plt.figure()
    ax = fig.add_subplot()


    z_values = graph3d.get_Z_values_in_radius_of_path(
        from_point, to_point, radius)
    #print(z_values)

    points = []
    for z in z_values:
        points.append(Point(5, z))

    arr = []
    for p in points:
        arr.append([p.x, p.y])
        # print(p)

    ax.plot(*zip(*arr), marker='o', color='r', ls='')
    #ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    for p in points:
        ax.broken_barh([(p.x, 1)], (p.y, 1), facecolors=color)
    ax.grid(True)


def draw_3d_points_in_radius_of_path(from_point: Point3D, to_point: Point3D, radius, z_radius):
    fig = plt.figure()
    ax3d = fig.add_subplot(111, projection='3d')

    points = graph3d.get_graph_points_in_radius_of_path(
        from_point, to_point, radius, z_radius)
    arr = []
    for p in points:
        arr.append([p.x, p.y, p.z])

    color = np.random.rand(3,)

    ax3d.plot(*zip(*arr), marker='o', color=color, alpha=0.2, ls='')
    ax3d.plot([from_point.x, to_point.x], [from_point.y,
              to_point.y], [from_point.z, to_point.z])

    '''
    color = np.random.rand(3,)
    for p in points:
        ax.broken_barh([(p.x, 1)], (p.y, 1), facecolors=color)
    '''
    ax3d.grid(True)


def draw_point_radius(point, radius):
    fig = plt.figure()
    ax = fig.add_subplot()

    points = graph.get_graph_points_in_radius(point, radius)
    arr = []
    for p in points:
        arr.append([p.x, p.y])

    ax.plot(*zip(*arr), marker='o', color='r', ls='')
    ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    for p in points:
        ax.broken_barh([(p.x, 1)], (p.y, 1), facecolors=color)
    circle1 = plt.Circle((int(point.x) + 0.5, int(point.y) + 0.5),
                         math.ceil(radius) + 0.5, color='blue', alpha=0.3)
    ax.add_patch(circle1)
    ax.broken_barh([(int(point.x), 1)], (int(point.y), 1), facecolors='red')
    ax.grid(True)

#draw_point_radius(Point(5.5,3.3), 2.2)


def draw_point_from_distance(from_point, to_point, distance):
    fig = plt.figure()
    ax = fig.add_subplot()
    point_a = graph.get_next_point_to_destination_from_distance(
        from_point, to_point, distance)
    arr = []
    arr.append([from_point.x, from_point.y])
    arr.append([to_point.x, to_point.y])
    arr.append([point_a.x, point_a.y])

    ax.plot(*zip(*arr), marker='o', color='r', ls='')

    ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    ax.plot([from_point.x, to_point.x], [from_point.y,
            to_point.y], color='red', linewidth=4.0)
    ax.plot([from_point.x, point_a.x], [from_point.y,
            point_a.y], color='black', linewidth=2.0)
    ax.grid(True)

def draw_steps_in_line(from_point, to_point, split):
    fig = plt.figure()
    ax = fig.add_subplot()


    arr = []
    arr.append([from_point.x, from_point.y])
    arr.append([to_point.x, to_point.y])

    di = math.dist(p.to_array(), p2.to_array())/split
    for i in range(1, split + 1):
        point_a = graph.get_next_point_to_destination_from_distance(from_point, to_point, di * i)
        arr.append([point_a.x, point_a.y])
    

    ax.plot(*zip(*arr), marker='o', color='r', ls='')

    ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    ax.plot([from_point.x, to_point.x], [from_point.y,
            to_point.y], color='blue', linewidth=4.0)
    ax.grid(True)

def draw_all_points_in_circle(angle, from_point: Point, to_point: Point, all):
    fig, ax = plt.subplots()
    radius = math.dist(from_point.to_array(), to_point.to_array())
    arr = []
    arr.append([from_point.x, from_point.y])
    arr.append([to_point.x, to_point.y])
    color = np.random.rand(3,)
    ax.plot([from_point.x, to_point.x], [from_point.y, to_point.y], color='blue', linewidth = 5)

    newAngle = angle
    while((newAngle <  360 and all) or (newAngle == angle and not all)):
        print("newAngle", newAngle)
        point = graph.get_point_from_distance_and_angle(newAngle, from_point, to_point)
        arr.append([point.x, point.y])
        ax.plot([from_point.x, point.x], [from_point.y, point.y])
        newAngle+=angle

    ax.plot(*zip(*arr), marker='o', color='r', ls='')
    ax.plot([0, 1], [0, 1])
    circle1 = plt.Circle(from_point.to_array(), radius, color='green', alpha=0.2)
    ax.add_patch(circle1)
    #ax.plot([int(from_point.x), int(to_point.x)],[int(from_point.y), int(to_point.y)])
    ax.grid(True)

def draw_points(from_point, to_point):
    fig, ax = plt.subplots()
    points = graph.find_all_points_between2_points(from_point, to_point)
    arr = []
    for p in points:
        arr.append([p.x, p.y])
        # print(p)

    ax.plot(*zip(*arr), marker='o', color='r', ls='')
    ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    for p in points:
        ax.broken_barh([(p.x, 1)], (p.y, 1), facecolors=color)
        #print(([from_point.x, to_point.x],[from_point.y, to_point.y]))
    ax.plot([from_point.x, to_point.x], [from_point.y, to_point.y])
    #ax.plot([int(from_point.x), int(to_point.x)],[int(from_point.y), int(to_point.y)])
    ax.grid(True)


def draw_points_in_radius_of_path(from_point, to_point, radius):
    fig, ax = plt.subplots()
    points = graph.get_graph_points_in_radius_of_path(
        from_point, to_point, radius)
    arr = []
    for p in points:
        arr.append([p.x, p.y])
        # print(p)

    #ax.plot(*zip(*arr), marker='o', color='r', ls='')
    ax.plot([0, 1], [0, 1])
    color = np.random.rand(3,)
    for p in points:
        ax.broken_barh([(p.x, 1)], (p.y, 1), facecolors=color)
        #print(([from_point.x, to_point.x],[from_point.y, to_point.y]))
    ax.plot([from_point.x, to_point.x], [from_point.y, to_point.y])
    #ax.plot([int(from_point.x), int(to_point.x)],[int(from_point.y), int(to_point.y)])
    ax.grid(True)


# draw_points_in_radius_of_path(Point(6,7), Point(2,5), 3)
#draw_points(Point(6,7), Point(2,5))

# draw_points(Point(6,7), Point(2,5))
# same points
# draw_points(Point(1, 2), Point(1, 2))
# same int points when float
# draw_points(Point(1.5, 2.3), Point(1.7, 2.5))
# same x
# draw_points(Point(1, 3), Point(1, 7))
# same y
# draw_points(Point(2.5, 4), Point(9, 4))
# same floats when min y calculated from min x after round  is smaller of min y
# draw_points(Point(0.5, 2), Point(2, 8))
# draw_points(Point(0.5, 2), Point(6, 12))

# same float when min x calculated from min y after round  is smaller of min x
#draw_points(Point(2, 0.5), Point(8, 2))

# same float when max y calculated from max x after round  is smaller of max y
# draw_points(Point(1, 2), Point(2.5, 8))
# same with x
# draw_points(Point(2, 1), Point(8, 2.5))

# draw_points(Point(0, 2), Point(6, 12))
# draw_points(Point(1, 2), Point(6, 12))

# draw_points(Point(6,5), Point(2,7))
# m -1
# draw_points(Point(1,2), Point(2,1))
# draw_points(Point(1,4), Point(2,2))

# m slope is > 0 and  abs m  is < 1
# draw_points(Point(5,2), Point(7,3))

# m slope is > 0 and  abs m  is > 1
# draw_points(Point(0, 2), Point(6, 12))

# m slope is > 0 and  abs m  is == 1
#draw_points(Point(2,10), Point(10,18))

# m slope is < 0 and  abs m  is == -1
#draw_points(Point(2,18), Point(10,10))


#draw_points(Point(2.3,18.5), Point(10.5,10.7))

# m slope is < 0 and  abs m  is < 1
#draw_points(Point(2,6), Point(10,4))

# m slope is < 0 and  abs m  is < 1
#draw_points(Point(5,3), Point(7,2))

# m slope is < 0 and  abs m  is < 1
#draw_points(Point(10,5), Point(15,2))

# m slope is < 0 and  abs m  is > 1
#draw_points(Point(2,15), Point(10,4))

# m slope is < 0 and  abs m  is > 1
#draw_points(Point(3,5), Point(2,7))
# m slope is < 0 and  abs m  is > 1
#draw_points(Point(2,5), Point(3,7))

#draw_points(Point(2,5), Point(3,3))

#draw_points(Point(5,4), Point(2,6))

#draw_points(Point(7,2), Point(5,3))

#ax.set_ylim(0, 100)
#ax.set_xlim(0, 100)
#ax.set_xlabel('seconds since start')
#ax.set_yticks([0, 100])
#ax.set_yticklabels(['Bill', 'Jim'])

p = Point(3.7648821797261838, 8.307569343634487)
p2 = Point(13.347209553338212, 13.474203192585769)
p = Point(random.randint(3, 15), random.randint(3, 15))
p2 = Point(random.randint(3, 15), random.randint(3, 15))
p = Point(random.uniform(3, 15), random.uniform(3, 15))
p2 = Point(random.uniform(3, 15), random.uniform(3, 15))
#print("p", p)
#print("p2", p2)
#draw_points( p, p2)

radius = random.uniform(5, 7)
radius = random.uniform(2, 3)
#print("radius", radius)
#draw_points_in_radius_of_path(p, p2, radius)
#draw_points(p, p2)

# ax.set_xlim([0,100])
# ax.set_ylim([0,100])

Z1 = random.uniform(3, 15)
Z2 = random.uniform(3, 15)
p3d = Point3D(random.uniform(3, 15), random.uniform(
    3, 15), Z1)
p3d2 = Point3D(random.uniform(3, 15), random.uniform(
    3, 15), Z2)

Z1 = random.randint(3, 5)
Z2 = random.randint(1, 5)
p3d = Point3D(random.randint(1, 3), random.randint(
    3, 5), Z1)
p3d2 = Point3D(random.randint(8, 12), random.randint(
    3, 5), Z1)
draw_3d_points_in_radius_of_path(p3d, p3d2, radius, radius)

Z1 = random.randint(3, 5)
Z2 = random.randint(1, 5)
rx = random.randint(1, 5)
ry = random.randint(3, 15)
p3d = Point3D(rx, ry, Z1)
p3d2 = Point3D(rx, ry, Z2)

#print("p3d", p3d)
#print("p3d2", p3d2)
draw_points_z_in_radius_of_path(p3d, p3d2, radius)
#draw_3d_points_in_radius_of_path(p3d, p3d2, radius, radius)

p = Point(random.uniform(3, 15), random.uniform(3, 15))
p2 = Point(random.uniform(3, 15), random.uniform(3, 15))
di = random.uniform(1, 3)
draw_point_from_distance(p, p2, di)
#draw_point_from_distance(Point(3, 5), Point(3, 8), 2)
#draw_point_from_distance(Point(4, 5), Point(7, 5), 2)

#draw_steps_in_line(p, p2, 5)

#print("p", p, "p2", p2, "di", di)

draw_all_points_in_circle(-30, p, p2, False)
draw_all_points_in_circle(30, p, p2, True)

plt.ylabel('some numbers')
plt.show()
