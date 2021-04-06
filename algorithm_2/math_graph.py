import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        return obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return obj.x != self.x or obj.y != self.y

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    def __hash__(self):
        return hash(str(self))

    def to_array(self):
        return [self.x, self.y]

    def to_string(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())


class Point3D(Point):

    def __init__(self, x, y, z):
        Point.__init__(self, x, y)
        self.z = z

    def get_point_2d(self):
        return Point(self.x, self.y)

    def __eq__(self, obj):
        return Point.__eq__(self, obj) and obj.z == self.z

    def __ne__(self, obj):
        return Point.__ne__(self, obj) or obj.z != self.z

    def to_array(self):
        return [self.x, self.y, self.z]


class TwoDLine:
    def __init__(self, from_point: Point, to_point: Point):
        self.from_point = from_point
        self.to_point = to_point
        self.parrallel_to_Y = from_point.x == to_point.x
        self.parrallel_to_X = from_point.y == to_point.y
        self.m = self.slope()
        print("m:", self.m)
        self.b = self.get_Y_interceptor()
        print("b:", self.b)
        self.min_X = min(from_point.x, to_point.x)
        self.max_X = max(from_point.x, to_point.x)
        self.min_Y = min(from_point.y, to_point.y)
        self.max_Y = max(from_point.y, to_point.y)

    def get_distance(self):
        return math.dist(self.from_point.to_array(), self.to_point.to_array())

    def slope(self):
        xDiff = (self.to_point.x-self.from_point.x)
        m = math.inf if xDiff == 0 else (
            self.to_point.y-self.from_point.y)/xDiff
        return m

    def get_Y_interceptor(self):
        m = self.slope()
        b = self.to_point.y-(m*self.to_point.x)
        return b


class TwoDGraph:
    def __init__(self):
        pass

    def find_all_points_between2_points(self, from_point: Point, to_point: Point):
        points = set()
        if from_point == to_point:
            points.add(Point(int(from_point.x), int(from_point.y)))
            print("same point:", from_point)
            return points

        line2d = TwoDLine(from_point, to_point)

        if not line2d.parrallel_to_Y and abs(line2d.m) < 1:
            print("loop x")
            #min_X_from_round_y = x = ((int(line2d.min_Y)-line2d.b) / line2d.m) if line2d.m != 0 else 0
            #max_X_from_round_y = x = ((int(line2d.max_Y)-line2d.b) / line2d.m) if line2d.m != 0 else 0
            #min_X = min(min_X_from_round_y, min_X, max_X_from_round_y)
            print("max_X", line2d.max_X)
            #max_X = max(min_X_from_round_y, max_X, max_X_from_round_y)
            print("max_X", line2d.max_X)
            for x in range(int(line2d.min_X), int(line2d.max_X) + 2):
                print("x", x)
                if line2d.parrallel_to_X:
                    y = from_point.y
                else:
                    y = (line2d.m * x) + line2d.b

                if x != int(line2d.max_X) + 1:
                    points.add(Point(int(x), int(y)))
                if x != int(line2d.min_X):
                    points.add(Point(int(x) - 1, int(y)))
                print('find y by x', 'x:', x, 'y:', y)
        if not line2d.parrallel_to_X and (abs(line2d.m) >= 1 or line2d.m == 0):
            print("loop y")
            #min_Y_from_round_x = (line2d.m * int(line2d.min_X)) + line2d.b
            #max_Y_from_round_x = (line2d.m * int(line2d.max_X)) + line2d.b
            #min_Y = min(min_Y_from_round_x, min_Y, max_Y_from_round_x)
            print(line2d.min_Y)
            #max_Y = max(min_Y_from_round_x, max_Y, max_Y_from_round_x)
            print(line2d.max_Y)
            for y in range(int(line2d.min_Y), int(line2d.max_Y + 2)):

                if line2d.parrallel_to_Y:
                    x = from_point.x
                else:
                    x = ((y-line2d.b) / line2d.m) if line2d.m != 0 else 0
                if y != int(line2d.max_Y) + 1:
                    points.add(Point(int(x), int(y)))
                if y != int(line2d.min_Y):
                    points.add(Point(int(x), int(y) - 1))
                print('find x by y', 'x:', x, 'y:', y)
        return points

    def get_graph_points_in_radius(self, point: Point, radius):

        print("for the args: point: %s: radius: %s" % (point, radius))

        radius = math.ceil(radius)
        # get the 4 points on the graph of the square that wrapped the circle of the radius
        topY = int(point.y) + radius
        bottomY = int(point.y) - radius
        leftX = int(point.x) - radius
        rightX = int(point.x) + radius

        print("topY: %s: bottomY: %s, leftX: %s, rightX: %s" %
              (topY, bottomY, leftX, rightX))

        # get all the points in the square
        points = []
        x = leftX
        while x <= rightX:
            y = bottomY
            while y <= topY:
                points.append(Point(x, y))
                y += 1
            x += 1
        return points

    def get_points_in_line_from_distance(self, from_point: Point, m, distance):
        point_a = Point(0, 0)
        point_b = Point(0, 0)
        if m == 0:
            point_a.x = from_point.x + distance
            point_a.y = from_point.y

            point_b.x = from_point.x - distance
            point_b.y = from_point.y
        elif m == math.inf:
            point_a.x = from_point.x
            point_a.y = from_point.y + distance

            point_b.x = from_point.x
            point_b.y = from_point.y - distance
        else:
            dx = distance / math.sqrt(1 + (m * m))
            dy = m * dx
            point_a.x = from_point.x + dx
            point_a.y = from_point.y + dy
            point_b.x = from_point.x - dx
            point_b.y = from_point.y - dy
        return (point_a, point_b)

    def get_next_point_to_destination_from_distance(self, from_point: Point, to_point: Point, distance):
        line2d = TwoDLine(from_point, to_point)

        if line2d.get_distance() <= distance:
            return to_point

        (point_a, point_b) = self.get_points_in_line_from_distance(
            from_point, line2d.m, distance)

        if line2d.m == math.inf and from_point.y < to_point.y:
            point = point_a
        elif line2d.m == 0 and from_point.x < to_point.x:
            point = point_a
        elif line2d.m < 0 and from_point.y > to_point.y:
            point = point_a
        elif line2d.m > 0 and from_point.y < to_point.y:
            point = point_a
        else:
            point = point_b

        return point

    def get_point_from_distance_and_angle(self, angle, from_point: Point, to_point: Point):
        '''
            Finding the x,y coordinates on circle, based on given angle
        '''
        radius = math.dist(from_point.to_array(), to_point.to_array())
        print("radius", radius)
        angle_of_line = math.degrees(math.atan2(
            to_point.y-from_point.y, to_point.x-from_point.x))
        print("angle", angle)
        angle_to_move = angle_of_line + angle
        # center of circle, angle in degree and radius of circle
        center = from_point
        angle_to_move_radians = math.radians(angle_to_move)
        x = center.x + (radius * math.cos(angle_to_move_radians))
        y = center.y + (radius * math.sin(angle_to_move_radians))
        print("new radius", math.dist(from_point.to_array(), [x,y]))
        print("x", x, "y ", y)
        return Point(x, y)

    def get_graph_points_in_radius_of_path(self, from_point: Point, to_point: Point, radius):
        points = self.find_all_points_between2_points(from_point, to_point)
        all_points = []
        for p in points:
            all_points.extend(self.get_graph_points_in_radius(p, radius))
        #print("len", len(all_points))
        all_points = list(dict.fromkeys(all_points))
        #print("len", len(all_points))
        return all_points


class ThreeDGraph(TwoDGraph):
    def __init__(self):
        TwoDGraph.__init__(self)

    def get_Z_values_in_radius_of_path(self, from_point: Point3D, to_point: Point3D, radius):
        Z_values = []
        radius = math.ceil(radius)
        min_Z = int(min(from_point.z, to_point.z)) - radius
        max_Z = int(max(from_point.z, to_point.z)) + radius
        for z in range(min_Z, max_Z + 1):
            Z_values.append(z)
        return Z_values

    def get_graph_points_in_radius_of_path(self, from_point: Point3D, to_point: Point3D, radius, z_radius):
        two_D_points = super().get_graph_points_in_radius_of_path(
            from_point.get_point_2d(), to_point.get_point_2d(), radius)
        Z_points = self.get_Z_values_in_radius_of_path(
            from_point, to_point, z_radius)
        three_D_points_result = []
        for p3d in Z_points:
            for p2d in two_D_points:
                three_D_points_result.append(Point3D(p2d.x, p2d.y, p3d))
        return three_D_points_result

# TODO
# get next point check if greater that the end point, one function that get the two point
# second function get m not need to restrict
# remove the -1 point or if greater that the matric size add to the graph the cube data
# check the threed graph
